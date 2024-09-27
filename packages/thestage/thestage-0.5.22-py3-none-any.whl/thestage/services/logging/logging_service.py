import asyncio
from _signal import SIGINT
from asyncio import CancelledError, Task
from typing import Optional, Dict

import aioconsole
import typer
from click.exceptions import Exit
from httpx import ReadTimeout
from requests.exceptions import ChunkedEncodingError
from thestage_core.entities.config_entity import ConfigEntity
from urllib3.exceptions import ReadTimeoutError

from thestage.services.clients.thestage_api.dtos.enums.task_status import TaskStatus
from thestage.services.clients.thestage_api.dtos.task_controller.task_view_response import TaskViewResponse
from thestage.services.logging.dto.log_message import LogMessage
from thestage.services.logging.dto.log_type import LogType
from thestage.i18n.translation import __
from thestage.services.abstract_service import AbstractService
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.helpers.error_handler import error_handler
from thestage.services.clients.thestage_api.api_client import TheStageApiClient
from thestage.services.config_provider.config_provider import ConfigProvider
from rich import print

is_logs_streaming = False


class LoggingService(AbstractService):
    __thestage_api_client: TheStageApiClient = None

    def __init__(
            self,
            thestage_api_client: TheStageApiClient,
            config_provider: ConfigProvider,
    ):
        super(LoggingService, self).__init__(
            config_provider=config_provider
        )
        self.__thestage_api_client = thestage_api_client

    @error_handler()
    def stream_container_logs(self, config: ConfigEntity, container: DockerContainerDto):
        typer.echo(__(
            f"Log stream for docker container '%container_slug%' started",
            {
                'container_slug': container.slug,
            }
        ))
        typer.echo(__("Press CTRL+C to stop"))
        try:
            for log_json in self.__thestage_api_client.get_container_log_stream(
                    token=config.main.thestage_auth_token,
                    container_id=container.id
            ):
                self.__print_log_line(log_json)
        except ChunkedEncodingError as e1:  # handling server timeout
            typer.echo(__('Log stream disconnected (1)'))
            raise typer.Exit(1)

        typer.echo(__('Log stream disconnected'))


    @error_handler()
    def stream_task_logs_with_controls(self, config: ConfigEntity, task_id: int):
        asyncio.run(
            self.__stream_task_logs_with_controls_async(
                config=config,
                task_id=task_id
            )
        )


    @error_handler()
    async def __stream_task_logs_with_controls_async(self, config: ConfigEntity, task_id: int):
        task_view_response: Optional[TaskViewResponse] = self.__thestage_api_client.get_task(
            token=config.main.thestage_auth_token,
            task_id=task_id,
        )

        task_status_map: Dict[str, str] = self.__thestage_api_client.get_task_localized_status_map(
            token=config.main.thestage_auth_token,
        )

        task = task_view_response.task

        if task:
            if task.frontend_status.status_key not in [TaskStatus.RUNNING, TaskStatus.SCHEDULED]:
                typer.echo(__("Task must be in status: '%required_status%'. Task %task_id% status: '%status%'", {
                    'task_id': str(task.id),
                    'status': task.frontend_status.status_translation,
                    'required_status': task_status_map.get(TaskStatus.RUNNING) or TaskStatus.RUNNING
                }))
                raise typer.Exit(1)
        else:
            typer.echo(__("Task with ID %task_id% was not found", {'task_id': task.id}))
            raise typer.Exit(1)

        typer.echo(__(
            f"Log stream for task %task_id% started",
            {
                'task_id': str(task.id),
            }
        ))

        typer.echo(__("CTRL+C to interrupt the task. CTRL+D to disconnect from log stream."))

        print_logs_task = asyncio.create_task(self.print_task_logs(config.main.thestage_auth_token, task.id))
        input_task = asyncio.create_task(self.read_log_stream_input())

        def sigint_handler():
            input_task.cancel()

        loop = asyncio.get_event_loop()
        for signal_item in [SIGINT]:  # SIGINT == CTRL+C
            loop.add_signal_handler(signal_item, sigint_handler)

        done, pending = await asyncio.wait([print_logs_task, input_task], return_when=asyncio.FIRST_COMPLETED)

        if input_task in done:
            print_logs_task.cancel()
            if not input_task.result():  # result is only expected if ctrl+D triggered EOFError
                typer.echo(f"\rTask {task_id} will be canceled")
                self.__thestage_api_client.stop_task_on_instance(
                    token=config.main.thestage_auth_token,
                    task_id=task.id,
                )


    async def read_log_stream_input(self):
        try:
            while True:
                input1 = await aioconsole.ainput()
        except EOFError:
            typer.echo(__("\rExited from task log stream"))
            return True
        except CancelledError:  # Always appears if async task is canceled and leaves huge traces
            pass


    async def print_task_logs(self, token: str, task_id: int):
        try:
            async for log_json in self.__thestage_api_client.get_task_log_stream_httpx(
                    token=token,
                    task_id=task_id
            ):
                self.__print_log_line(log_json)
            typer.echo(__('Log stream disconnected'))
        except ChunkedEncodingError as e1:  # handling server timeout
            typer.echo(__('Log stream: disconnected from server'))
        except ReadTimeout as e2:  # happens if internet is turned off during stream
            typer.echo(f"Log stream: disconnected from server (possible connectivity issue). Try 'thestage project task logs {task_id}' to reconnect.")


    @staticmethod
    def __print_log_line(log_message_raw_json: str):
        line_color: str = "grey78"

        log_obj = LogMessage.model_validate_json(log_message_raw_json)
        if not log_obj.logType and log_obj.message == 'ping':
            return

        if log_obj.logType == LogType.STDERR.value:
            line_color = "red"
        if log_obj.message:
            print(f'[{line_color}][not bold]{log_obj.message}[/not bold][/{line_color}]')

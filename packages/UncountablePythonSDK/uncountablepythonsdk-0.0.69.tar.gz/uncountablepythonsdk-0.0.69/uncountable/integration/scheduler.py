import multiprocessing
import subprocess
import sys
import time
from dataclasses import dataclass

from opentelemetry.trace import get_current_span

from uncountable.integration.entrypoint import main as cron_target
from uncountable.integration.telemetry import Logger

SHUTDOWN_TIMEOUT_SECS = 30


@dataclass(kw_only=True)
class ProcessInfo:
    name: str
    process: multiprocessing.Process | subprocess.Popen[bytes]

    @property
    def is_alive(self) -> bool:
        match self.process:
            case multiprocessing.Process():
                return self.process.is_alive()
            case subprocess.Popen():
                return self.process.poll() is None

    @property
    def pid(self) -> int | None:
        return self.process.pid


def handle_shutdown(logger: Logger, processes: list[ProcessInfo]) -> None:
    logger.log_info("received shutdown command, shutting down sub-processes")
    for proc_info in processes:
        if proc_info.is_alive:
            proc_info.process.terminate()

    shutdown_start = time.time()
    still_living_processes = processes
    while (
        time.time() - shutdown_start < SHUTDOWN_TIMEOUT_SECS
        and len(still_living_processes) > 0
    ):
        current_loop_processes = [*still_living_processes]
        logger.log_info(
            "waiting for sub-processes to shut down",
            attributes={
                "still_living_processes": [
                    proc_info.name for proc_info in still_living_processes
                ]
            },
        )
        still_living_processes = []
        for proc_info in current_loop_processes:
            if not proc_info.is_alive:
                logger.log_info(f"{proc_info.name} shut down successfully")
            else:
                still_living_processes.append(proc_info)
        time.sleep(1)

    for proc_info in still_living_processes:
        logger.log_warning(
            f"{proc_info.name} failed to shut down after {SHUTDOWN_TIMEOUT_SECS} seconds, forcefully terminating"
        )
        proc_info.process.kill()


def check_process_health(logger: Logger, processes: list[ProcessInfo]) -> None:
    for proc_info in processes:
        if not proc_info.is_alive:
            logger.log_error(
                f"process {proc_info.name} shut down unexpectedly! shutting down scheduler"
            )
            handle_shutdown(logger, processes)
            sys.exit(1)


def main() -> None:
    logger = Logger(get_current_span())
    processes: list[ProcessInfo] = []

    def add_process(process: ProcessInfo) -> None:
        processes.append(process)
        logger.log_info(f"started process {process.name}")

    cron_process = multiprocessing.Process(target=cron_target, args={"blocking": True})
    cron_process.start()
    add_process(ProcessInfo(name="cron server", process=cron_process))

    uwsgi_process = subprocess.Popen([
        "/app/env/bin/uwsgi",
        "-H",
        "/app/env",
        "--die-on-term",
    ])
    add_process(ProcessInfo(name="uwsgi", process=uwsgi_process))

    try:
        while True:
            check_process_health(logger, processes=processes)
            time.sleep(1)
    except KeyboardInterrupt:
        handle_shutdown(logger, processes=processes)


main()

import os
from datetime import datetime
from rich.console import Console
from rich.traceback import install

LOGS_PATH = "./logs"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    def __init__(self, task_name=None):
        if not os.path.exists(LOGS_PATH):
            os.makedirs(LOGS_PATH)

        self.console = Console()
        install(console=self.console)

        date = datetime.now().strftime("%Y-%m-%d_%H")
        file_name = f"{date}_log.log" if not task_name else f"{date}_{task_name}.log"
        log_file = os.path.join(LOGS_PATH, file_name)

        self.file_console = Console(file=open(log_file, "a", encoding="utf-8"))

    def log(self, message, level="INFO"):
        formatted = f"[{level}] {message}"
        self.console.print(formatted)
        self.file_console.print(formatted)

    def info(self, message):
        self.log(message, "INFO")

    def warning(self, message):
        self.log(message, "WARNING")

    def error(self, message):
        self.log(message, "ERROR")

    def success(self, message):
        self.log(message, "SUCCESS")

    def debug(self, message):
        self.log(message, "DEBUG")

    def flush(self):
        self.console.print()
        self.file_console.print()

    def close(self):
        if self.file_console and not self.file_console.file.closed:
            self.file_console.file.close()

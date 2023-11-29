from enum import Enum
import os
from utils import formattedDateTime

class LogLevel(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2

class Logger:
    LOG_PATH = os.getcwd() + "/logs"
    os.makedirs(LOG_PATH, exist_ok=True)
    current_scene = ""
    current_steps = []

    @staticmethod
    def logScene(scene):
        Logger.info(f"\nПрохожу сценарий {scene} ...")
        Logger.current_scene = scene
        Logger.current_steps = []

    @staticmethod
    def logStep(step, driver=None):
        if not (driver is None):
            step += f" (ID экрана: {driver.get_screen_id()})"
        Logger.info(step)
        Logger.current_steps.append(step)

    @staticmethod
    def logError(msg, driver=None):
        Logger.error(f"Ошибка: {msg}")
        log_prefix = f"{Logger.LOG_PATH}/{Logger.current_scene}_{formattedDateTime()}"
        with open(log_prefix + ".txt", "w") as f:
            f.write(f"Сценарий: {Logger.current_scene}\n")
            for step in Logger.current_steps:
                f.write(step + "\n")
            f.write(f"Ошибка: {msg}")
        if not (driver is None):
            driver.screenshot(log_prefix + ".png")
        Logger.error(f"Логи ошибки: {log_prefix}")

    @staticmethod
    def info(msg):
        Logger.log(msg, LogLevel.INFO)

    @staticmethod
    def warning(msg):
        Logger.log(msg, LogLevel.WARNING)

    @staticmethod
    def error(msg):
        Logger.log(msg, LogLevel.ERROR)

    @staticmethod
    def log(msg, log_level):
        if log_level == LogLevel.INFO:
            print(f"{msg}")
        elif log_level == LogLevel.WARNING:
            print(f"\033[33m{msg}\033[0m")
        elif log_level == LogLevel.ERROR:
            print(f"\033[31m{msg}\033[0m")
        else:
            print(msg)


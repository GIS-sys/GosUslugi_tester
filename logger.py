import os
from utils import formattedDateTime

class Logger:
    LOG_PATH = os.getcwd() + "/logs"
    os.makedirs(LOG_PATH, exist_ok=True)
    current_scene = ""
    current_steps = []

    @staticmethod
    def logScene(scene):
        print(f"Прохожу сценарий {scene} ...")
        Logger.current_scene = scene
        Logger.current_steps = []

    @staticmethod
    def logStep(step):
        print(step)
        Logger.current_steps.append(step)

    @staticmethod
    def logError(msg, driver=None):
        print(f"Ошибка: {msg}")
        log_prefix = f"{Logger.LOG_PATH}/{Logger.current_scene}_{formattedDateTime()}"
        with open(log_prefix + ".txt", "w") as f:
            f.write(f"Сценарий: {Logger.current_scene}\n")
            for step in Logger.current_steps:
                f.write(step + "\n")
            f.write(f"Ошибка: {msg}")
        if not (driver is None):
            driver.screenshot(log_prefix + ".png")
        print(f"Логи ошибки: {log_prefix}")

    @staticmethod
    def log(msg):
        print(msg)


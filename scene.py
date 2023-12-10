from action import Action
import config
from logger import Logger
from utils import findFilesByRegex


class Scene:
    def __init__(self, name):
        self.name = name
        if self.name.endswith(".scn"):
            self.name = self.name[:-4]
        self.check()
        self.configure()

    def check(self):
        paths = findFilesByRegex("data", f"**/{self.name}.scn")
        if not paths:
            Logger.error(f"Должен существовать файл {self.getName()}")
            exit()
        self.path = paths[0]
        if len(paths) > 1:
            Logger.warning(f"Предупреждение: было обнаружено несколько сценариев с именем {self.getName()}, использую {self.getPath()}")

    def __iter__(self):
        with open(self.getPath(), "r") as f:
            for line in f:
                line = line.strip()
                if len(line) == 0 or line.startswith(config.ACTIONS_COMMENTS) or line.startswith(config.CONFIG_LINESTART):
                    continue
                yield Action.fromLine(line)

    def configure(self):
        self.auth_email, self.auth_pass, self.auth_role = None, None, None
        self.number = None
        with open(self.getPath(), "r") as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue
                if not line.startswith(config.CONFIG_LINESTART):
                    continue
                for ls in line:
                    if line.startswith(ls):
                        line = line[len(ls):].strip()
                        break
                if line.startswith("AUTH_EMAIL"):
                    self.auth_email = line[len("AUTH_EMAIL"):].strip()
                if line.startswith("AUTH_PASS"):
                    self.auth_pass = line[len("AUTH_PASS"):].strip()
                if line.startswith("AUTH_ROLE"):
                    self.auth_role = line[len("AUTH_ROLE"):].strip()
                if line.startswith("NUMBER"):
                    self.number = line[len("NUMBER"):].strip()
        if not self.auth_email or not self.auth_pass or not self.auth_role:
            Logger.error(f"Файл сценария {self.name} не содержит информации о пользователе")
            exit()
        if not self.number:
            Logger.error(f"Файл сценария {self.name} не содержит информации о номере услуги")
            exit()
        try:
            self.number = int(self.number)
        except ValueError:
            Logger.error(f"Файл сценария {self.name} содержит некорректный номер услуги: {self.number}")
            exit()

    def getAuthEmail(self):
        return self.auth_email

    def getAuthPass(self):
        return self.auth_pass

    def getAuthRole(self):
        return self.auth_role

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def getNumber(self):
        return int(self.number)


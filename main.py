from driver import Driver
from logger import Logger
from utils import findFilesByRegex
import os


class Scene:
    def __init__(self, name):
        self.name = name
        if self.name.endswith(".scn"):
            self.name = self.name[:-4]
        self.check()

    def check(self):
        if len(self.name) < 6:
            print(f"Название файла сценария {self.name} должно начинаться с номера услуги, например: 618022_convert")
            exit()
        try:
            int(self.name[:6])
        except ValueError:
            print(f"Название файла сценария {self.name} должно начинаться с номера услуги, например: 618022_convert")
            exit()
        paths = findFilesByRegex("scenes", f"**/{self.name}.scn")
        if not paths:
            print(f"Должен существовать файл {self.getName()}")
            exit()
        self.path = paths[0]
        if len(paths) > 1:
            print(f"Предупреждение: было обнаружено несколько сценариев с именем {self.getName()}, использую {self.getPath()}")

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def getNumber(self):
        return int(self.name[:6])

def inputScenes():
    print("Введите названия сценариев, которые хотите запустить, через запятую или пробел (данные файлы с расширением .scn должны лежать в папке scenes или любой её подпапке).")
    print("Например: 619069.scn, 618022_add_changes, 618022_convert")
    scenes = input().replace(" ", ",").split(",")
    scenes = [x for x in scenes if x != ""]
    scenes = list(map(str.strip, scenes))
    return scenes
    

if __name__ == "__main__":
    scenes = inputScenes()
    dataForRun = [Scene(scene) for scene in scenes]
    for scene in dataForRun:
        Logger.logScene(scene.getName())
        Driver().run(scene)


from driver import Driver
from logger import Logger
from scene import Scene


def inputScenes():
    Logger.info("Введите названия сценариев, которые хотите запустить, через запятую или пробел (данные файлы с расширением .scn должны лежать в папке scenes или любой её подпапке).")
    Logger.info("Например: example.scn, 618022_convert.scn")
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


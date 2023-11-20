from driver import Driver

def checkScenes(scenes):
    for scene in scenes:
        if len(scene) < 6:
            print(f"Название файла сценария {scene} должно начинаться с номера услуги, например: 618022_convert")
            exit()
        try:
            int(scene[:6])
        except ValueError:
            print(f"Название файла сценария {scene} должно начинаться с номера услуги, например: 618022_convert")
            exit()

if __name__ == "__main__":
    scenesS = input("Введите названия сценариев, которые хотите запустить, через запятую (данные файлы с расширением .scn должны лежать в папке scenes). Например: 618022_add_changes,618022_convert\n")
    scenes = list(map(str.strip, scenesS.split(",")))
    checkScenes(scenes)
    dataForRun = [(int(scene[:6]), f"scenes/{scene}.scn", scene) for scene in scenes]
    for scene in dataForRun:
        print(f"\nRunning {scene[2]}...")
        Driver().run(scene)


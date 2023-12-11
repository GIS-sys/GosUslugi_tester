from action import Action
import config
from logger import Logger
from utils import tryN

import os
import random
import selenium
import time
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class Driver:
    def __init__(self):
        self.DOWNLOAD_PATH = os.getcwd() + config.DOWNLOAD_PATH
        os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)
        self.options = Options()
        self.options.headless = False
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.dir", self.DOWNLOAD_PATH)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        self.driver = webdriver.Firefox(firefox_profile=self.profile, executable_path=config.GECKODRIVER_PATH, options=self.options)

    def __del__(self):
        self.driver.quit()

    def screenshot(self, filepath):
        self.driver.save_screenshot(filepath)

    def get_screen_id(self):
        return Action.waitGetElement(self, (By.XPATH, '//epgu-constructor-form-player'))[0].get_attribute("data-test-screen-id")

    def auth(self, email, password):
        self.driver.get("https://esia-portal1.test.gosuslugi.ru/login/")
        inputEmail = Action.waitGetElement(self, (By.ID, "login"))
        inputPassword = Action.waitGetElement(self, (By.ID, "password"))
        buttonAuth = Action.waitGetElement(self, (By.XPATH, '//button[normalize-space()="Войти"]'))
        if len(inputEmail) != 1 or len(inputPassword) != 1 or len(buttonAuth) != 1:
            raise Exception("Authentification page is not loaded properly")
        inputEmail[0].send_keys(email)
        inputPassword[0].send_keys(password)
        buttonAuth[0].click()

    def role(self, role):
        self.driver.get("https://svcdev-roles.test.gosuslugi.ru/")
        buttonRole = tryN(lambda: Action.waitGetElement(self, (By.CLASS_NAME, 'role')), 2, 1)
        for button in buttonRole:
            if button.get_property("title").startswith(role):
                tryN(button.click, 5, 1)
                return
        raise Exception("Role not found")

    def chooseService(self, code):
        self.driver.get(f"http://svcdev-beta.test.gosuslugi.ru/{code}/1/form")
        try:
            buttonAuth = Action.waitGetElement(self, (By.XPATH, '//span[normalize-space()="Начать заново"]'))
        except selenium.common.exceptions.TimeoutException:
            Logger.warning("Отсутствует кнопка 'Начать заново', полагаю, что услуга уже началась")
            return
        if len(buttonAuth) > 1:
            raise Exception("Role chosing page is not loaded properly")
        tryN(buttonAuth[0].click, 5, 1)

    def initiate(self, scene):
        for action in scene:
            try:
                action.perform(self)
            except selenium.common.exceptions.TimeoutException as e:
                Logger.logError("Время ожидания действия истекло", self)
                test = self.driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")
                with open(config.LOG_FILE, "a") as f:
                    for item in test:
                        f.write(str(item) + "\n")
                return False
            time.sleep(config.DELAY_BETWEEN_ACTIONS)
        Logger.success(f"Услуга {scene.getName()} успешно пройдена")
        return True

    def run(self, scene):
        self.auth(scene.getAuthEmail(), scene.getAuthPass())
        time.sleep(3)
        self.role(scene.getAuthRole())
        self.chooseService(scene.getNumber())
        if not self.initiate(scene) or config.CLOSE_AFTER_TEST:
            time.sleep(config.WAIT_AFTER_TEST)
        else:
            while True:
                pass

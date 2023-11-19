from action import Action
from actions import Actions
import config
from utils import tryN

import time
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import random

class Driver:
    def __init__(self):
        self.options = Options()
        self.options.headless = False
        self.driver = webdriver.Firefox(executable_path=config.GECKODRIVER_PATH, options=self.options)

    def __del__(self):
        self.driver.quit()

    def auth(self, email, password):
        self.driver.get("https://esia-portal1.test.gosuslugi.ru/login/")
        inputEmail = Action.waitGetElement(self.driver, (By.ID, "login"))
        inputPassword = Action.waitGetElement(self.driver, (By.ID, "password"))
        buttonAuth = Action.waitGetElement(self.driver, (By.XPATH, '//button[normalize-space()="Войти"]'))
        if len(inputEmail) != 1 or len(inputPassword) != 1 or len(buttonAuth) != 1:
            raise Exception("Authentification page is not loaded properly")
        inputEmail[0].send_keys(email)
        inputPassword[0].send_keys(password)
        buttonAuth[0].click()

    def role(self, role):
        self.driver.get("https://svcdev-roles.test.gosuslugi.ru/")
        buttonRole = Action.waitGetElement(self.driver, (By.CLASS_NAME, 'role'))
        for button in buttonRole:
            if button.get_property("title").startswith(role):
                tryN(button.click, 5, 1)
                return
        raise Exception("Role not found")

    def chooseService(self, code):
        self.driver.get(f"http://svcdev-beta.test.gosuslugi.ru/{code}/1/form")
        try:
            buttonAuth = Action.waitGetElement(self.driver, (By.XPATH, '//span[normalize-space()="Начать заново"]'))
        except selenium.common.exceptions.TimeoutException:
            print("Отсутствует кнопка 'Начать заново', полагаю, что услуга уже началась")
            return
        if len(buttonAuth) > 1:
            raise Exception("Role chosing page is not loaded properly")
        tryN(buttonAuth[0].click, 5, 1)

    def initiate(self):
        for action in Actions(config.SCENE_FILEPATH):
            action.perform(self.driver)

    def run(self):
        self.auth(config.AUTH_EMAIL, config.AUTH_PASS)
        self.role(config.AUTH_ROLE)
        self.chooseService(config.SERVICE_CODE)
        self.initiate()
        if config.CLOSE_AFTER_TEST:
            time.sleep(config.WAIT_AFTER_TEST)


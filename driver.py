from config import GECKODRIVER_PATH
from utils import tryN

import time
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

class Driver:
    def __init__(self):
        self.options = Options()
        self.options.headless = False
        self.driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH, options=self.options)

    def __del__(self):
        self.driver.quit()

    def _waitGetElement(self, args):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(args))

    def auth(self, email, password):
        self.driver.get("https://esia-portal1.test.gosuslugi.ru/login/")
        inputEmail = self._waitGetElement((By.ID, "login"))
        inputPassword = self._waitGetElement((By.ID, "password"))
        buttonAuth = self._waitGetElement((By.XPATH, '//button[normalize-space()="Войти"]'))
        if len(inputEmail) != 1 or len(inputPassword) != 1 or len(buttonAuth) != 1:
            raise Exception("Authentification page is not loaded properly")
        inputEmail[0].send_keys(email)
        inputPassword[0].send_keys(password)
        buttonAuth[0].click()

    def role(self, role):
        self.driver.get("https://svcdev-roles.test.gosuslugi.ru/")
        buttonRole = self._waitGetElement((By.CLASS_NAME, 'role'))
        for button in buttonRole:
            if button.get_property("title").startswith(role):
                tryN(button.click, 5, 1)
                return
        raise Exception("Role not found")

    def chooseService(self, code):
        self.driver.get(f"http://svcdev-beta.test.gosuslugi.ru/{code}/1/form")
        try:
            buttonAuth = self._waitGetElement((By.XPATH, '//span[normalize-space()="Начать заново"]'))
        except selenium.common.exceptions.TimeoutException:
            print("Отсутствует кнопка 'Начать заново', полагаю, что услуга уже началась")
            return
        if len(buttonAuth) > 1:
            raise Exception("Role chosing page is not loaded properly")
        tryN(buttonAuth[0].click, 5, 1)

    def initiate(self):
        for action in [["button", "Начать"], ["button", "Заявитель"], ["list", "Перечень", "Аттестоваться"], ["button", "Продолжить"],
                       ["button", "Да"], ["button", "Признание результатов"], ["button", "Да"], ["button", "Нет"], ["button", "Перейти"], ["button", "Верно"],
                       ["input", "телефона", "1234567890"]]:
            if action[0] == "button":
                button = self._waitGetElement((By.XPATH, f"//epgu-constructor-screen-resolver//button//*[contains(text(),'{action[1]}')]"))
                button[0].click()
            if action[0] == "list":
                listOpen = self._waitGetElement((By.XPATH, f"//epgu-constructor-screen-resolver//epgu-constructor-dropdown[contains(.,'{action[1]}')]//input[contains(@class,'focusable-input')]"))
                listOpen[0].click()
                listEl = self._waitGetElement((By.XPATH, f"//epgu-constructor-screen-resolver//epgu-constructor-dropdown[contains(.,'{action[1]}')]//*[contains(@class,'dropdown-list-wrapper')]//*[contains(@class,'dropdown-item')]//*[contains(.,'{action[2]}')]"))
                listEl[0].click()
            if action[0] == "input":
                inputEl = self._waitGetElement((By.XPATH, f"//epgu-constructor-screen-resolver//epgu-constructor-component-item[contains(.,'{action[1]}')]//input"))
                inputEl[0].send_keys(action[2])

    def tmp(self):
        self.driver.get(f"http://localhost:8080")
        allElements = self._waitGetElement((By.XPATH, "//div//span[contains(@class, 'a')][contains(@class, 'b')]"))
        for x in allElements:
            print(x.tag_name, x.text, x.get_attribute("innerHTML"))
        exit()

    def run(self):
        #self.tmp()
        self.auth("esiatest002@yandex.ru", "11111111")
        self.role("Фамилия002 Имя002  Отчество002")
        self.chooseService(619069)
        self.initiate()
        time.sleep(10)



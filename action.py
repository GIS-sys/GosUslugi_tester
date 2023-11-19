from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Action(ABC):
    @staticmethod
    def fromList(lis):
        if lis[0] == "button":
            return ActionButton(label=lis[1])
        if lis[0] == "list":
            return ActionList(label=lis[1], choice=lis[2])
        if lis[0] == "input":
            return ActionInput(label=lis[1], text=lis[2])
        raise Exception("Action.fromList got unexpected action type")

    @staticmethod
    def waitGetElement(driver, args):
        return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(args))

class ActionO(ABC):
    @abstractmethod
    def perform(self, driver):
        pass

    @staticmethod
    def getXpathBy():
        pass

class ActionButton(ActionO):
    def __init__(self, label):
        self.label = label

    def perform(self, driver):
        button = Action.waitGetElement(driver, (By.XPATH, f"//epgu-constructor-screen-resolver//button//*[contains(text(),'{self.label}')]"))
        button[0].click()

class ActionList(ActionO):
    def __init__(self, label, choice):
        self.label = label
        self.choice = choice

    def perform(self, driver):
        listOpen = Action.waitGetElement(driver, (By.XPATH, f"//epgu-constructor-screen-resolver//epgu-constructor-dropdown[contains(.,'{self.label}')]//input[contains(@class,'focusable-input')]"))
        listOpen[0].click()
        listEl = Action.waitGetElement(driver, (By.XPATH, f"//epgu-constructor-screen-resolver//epgu-constructor-dropdown[contains(.,'{self.label}')]//*[contains(@class,'dropdown-list-wrapper')]//*[contains(@class,'dropdown-item')]//*[contains(.,'{self.choice}')]"))
        listEl[0].click()

class ActionInput(ActionO):
    def __init__(self, label, text):
        self.label = label
        self.text = text

    def perform(self, driver):
        inputEl = Action.waitGetElement(driver, (By.XPATH, f"//epgu-constructor-screen-resolver//epgu-constructor-component-item[contains(.,'{self.label}')]//input"))
        inputEl[0].send_keys(self.text)

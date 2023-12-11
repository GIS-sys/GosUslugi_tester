from abc import ABC, abstractmethod
from logger import Logger
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def addStringOrList(baseList, stringOrList, foo):
    if isinstance(stringOrList, str):
        return [foo(x, stringOrList) for x in baseList]
    elif isinstance(stringOrList, list):
        newRes = []
        for x in baseList:
            for singleString in stringOrList:
                newRes.append(foo(x, singleString))
        return newRes
    else:
        raise Exception(f"addStringOrList got unexpected argument type: {type(stringOrList)}")

class Action(ABC):
    @staticmethod
    def fromList(lis):
        if lis[0] == "button":
            return ActionButton(label=lis[1])
        if lis[0] == "list":
            return ActionList(label=lis[1], choice=lis[2])
        if lis[0] == "lookup":
            return ActionLookup(label=lis[1], choice=lis[2])
        if lis[0] == "input":
            return ActionInput(label=lis[1], text=lis[2])
        if lis[0] == "address":
            return ActionAddress(label=lis[1], text=lis[2])
        if lis[0] == "file":
            return ActionFileUpload(ext=lis[1])
        if lis[0] == "vm":
            return ActionDownloadVm()
        if lis[0] == "pdf":
            return ActionDownloadPdf()
        if lis[0] == "checkbox":
            return ActionCheckbox(label=lis[1])
        if lis[0] == "find":
            return ActionFind(label=lis[1])
        raise Exception(f"Action.fromList got unexpected action type: {lis}")

    @staticmethod
    def fromLine(line):
        return Action.fromList(eval(f"[{line}]"))

    @staticmethod
    def waitGetElement(driver, args, timeout=10):
        return WebDriverWait(driver.driver, timeout).until(EC.presence_of_all_elements_located(args))

    @staticmethod
    def getXpathBy(inside_main_screen=False, inside_component=True, tag=None, label=None, add=None):
        res = ["//epgu-constructor-screen-resolver"]
        if inside_main_screen:
            res = addStringOrList(res, "//div[contains(@class,'form__item') and not(contains(@class,'form__item--hidden'))]", lambda x, y: (x + y))
        if inside_component:
            res = addStringOrList(res, "//epgu-constructor-component-item", lambda x, y: (x + y))
            if not (label is None):
                res = addStringOrList(res, label, lambda x, y: (x + "[contains(.,'{label}')]".format(label=y)))
            if not (tag is None):
                res = addStringOrList(res, tag, lambda x, y: (x + "//{tag}".format(tag=y)))
        else:
            if not (tag is None):
                res = addStringOrList(res, tag, lambda x, y: (x + "//{tag}".format(tag=y)))
            if not (label is None):
                res = addStringOrList(res, label, lambda x, y: (x + "[contains(.,'{label}')]".format(label=y)))
        if not (add is None):
            res = addStringOrList(res, add, lambda x, y: (x + "//{add}".format(add=y)))
        res = '|'.join(res)
        return (By.XPATH, res)

    @staticmethod
    def clickOutside(driver):
        Action.waitGetElement(driver, (By.XPATH, "//html"))[0].click()

class ActionO(ABC):
    @abstractmethod
    def perform(self, driver):
        pass

class ActionButton(ActionO):
    def __init__(self, label):
        self.label = label

    def perform(self, driver):
        Logger.logStep(f"Нажимаю на кнопку '{self.label}'", driver)
        button = Action.waitGetElement(driver, Action.getXpathBy(inside_component=False, tag="button[not(contains(@class,'disabled'))]", label=self.label))
        button[0].click()

class ActionList(ActionO):
    def __init__(self, label, choice):
        self.label = label
        self.choice = choice

    def perform(self, driver):
        Logger.logStep(f"Выбираю в списке '{self.label}' ответ '{self.choice}'", driver)
        listOpen = Action.waitGetElement(driver, Action.getXpathBy(inside_main_screen=True, tag="input[contains(@class,'focusable-input')]", label=self.label))
        listOpen[0].click()
        listEl = Action.waitGetElement(driver, Action.getXpathBy(
            inside_component=False,
            tag="epgu-constructor-dropdown",
            label=self.label,
            add=f"*[contains(@class,'dropdown-list-wrapper')]//*[contains(@class,'dropdown-item')]//*[contains(.,'{self.choice}')]"
        ))
        listEl[0].click()

class ActionLookup(ActionO):
    def __init__(self, label, choice):
        self.label = label
        self.choice = choice

    def perform(self, driver):
        Logger.logStep(f"Выбираю в списке со словарём '{self.label}' ответ '{self.choice}'", driver)
        listOpen = Action.waitGetElement(driver, Action.getXpathBy(inside_main_screen=True, tag="input[contains(@class,'search-input')]", label=self.label))
        listOpen[0].click()
        listOpen[0].send_keys(self.choice)
        time.sleep(1)
        listEls = Action.waitGetElement(driver, Action.getXpathBy(
            inside_component=False,
            tag="epgu-constructor-component-list-resolver",
            label=self.label,
            add=f"*[contains(@class,'lookup-list-container') and contains(@class,'expanded')]//*[contains(@class,'lookup-item-text')]"
        ))
        for el in listEls:
            if self.choice in el.get_attribute('innerHTML'):
                el.click()
                return
        raise selenium.common.exceptions.TimeoutException("ActionLookup - perform - timeout")

class ActionInput(ActionO):
    def __init__(self, label, text):
        self.label = label
        self.text = text

    def perform(self, driver):
        Logger.logStep(f"Пишу в поле '{self.label}' текст '{self.text}'", driver)
        inputEl = Action.waitGetElement(driver, Action.getXpathBy(inside_main_screen=True, tag=["input", "div[contains(@class,'multiline-input')]", "textarea"], label=self.label))
        inputEl[0].send_keys(self.text)

class ActionAddress(ActionO):
    def __init__(self, label, text):
        self.label = label
        self.text = text

    def perform(self, driver):
        Logger.logStep(f"Пишу в поле адреса '{self.label}' текст '{self.text}'", driver)
        inputEl = Action.waitGetElement(driver, Action.getXpathBy(inside_main_screen=True, tag=["textarea[contains(@class,'search-input')]"], label=self.label))
        inputEl[0].send_keys(self.text)
        Action.clickOutside(driver)
        time.sleep(1)

class ActionFileUpload(ActionO):
    def __init__(self, ext):
        self.ext = ext

    def perform(self, driver):
        Logger.logStep(f"Загружаю файл расширения '.{self.ext}'", driver)
        inputUpload = Action.waitGetElement(driver, Action.getXpathBy(inside_component=False, tag="input[contains(@type,'file')]"))
        inputUpload[0].send_keys(f"{os.getcwd()}/files/tmp.{self.ext}")

class ActionDownloadVm(ActionO):
    def perform(self, driver):
        Logger.logStep(f"Скачиваю VM-шаблон", driver)
        buttonDownload = Action.waitGetElement(driver, Action.getXpathBy(
            inside_component=False,
            tag="epgu-constructor-uploader-manager-item[.//img[contains(@alt,'.xml')]]",
            add="button[contains(@class,'download_button')]"
        ))
        buttonDownload[-1].click()

class ActionDownloadPdf(ActionO):
    def perform(self, driver):
        Logger.logStep(f"Скачиваю PDF-шаблон", driver)
        buttonDownload = Action.waitGetElement(driver, Action.getXpathBy(
            inside_component=False,
            tag="epgu-constructor-uploader-manager-item[.//img[contains(@alt,'.pdf')]]",
            add="button[contains(@class,'download_button')]"
        ))
        buttonDownload[-1].click()

class ActionCheckbox(ActionO):
    def __init__(self, label):
        self.label = label

    def perform(self, driver):
        Logger.logStep(f"Нажимаю чекбокс '{self.label}'", driver)
        checkbox = Action.waitGetElement(driver, Action.getXpathBy(inside_main_screen=True, tag="epgu-cf-ui-constructor-constructor-checkbox", label=self.label, add="span[contains(@class,'checkbox')]"))
        checkbox[0].click()

class ActionFind(ActionO):
    def __init__(self, label):
        self.label = label

    def perform(self, driver):
        Logger.logStep(f"Проверяю присутствие на странице текста '{self.label}'", driver)
        Action.waitGetElement(driver, Action.getXpathBy(inside_component=False, tag="*", label=self.label))


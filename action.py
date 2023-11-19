from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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
        if lis[0] == "input":
            return ActionInput(label=lis[1], text=lis[2])
        if lis[0] == "file":
            return ActionFileUpload(ext=lis[1])
        if lis[0] == "vm":
            return ActionDownloadVm()
        raise Exception("Action.fromList got unexpected action type")

    @staticmethod
    def fromLine(line):
        return Action.fromList(eval(line))

    @staticmethod
    def waitGetElement(driver, args):
        return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(args))

    @staticmethod
    def getXpathBy(inside_component=True, tag=None, label=None, add=None):
        res = ["//epgu-constructor-screen-resolver"]
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

class ActionO(ABC):
    @abstractmethod
    def perform(self, driver):
        pass

class ActionButton(ActionO):
    def __init__(self, label):
        self.label = label

    def perform(self, driver):
        print(f"Нажимаю на кнопку '{self.label}'")
        button = Action.waitGetElement(driver, Action.getXpathBy(inside_component=False, tag="button[not(contains(@class,'disabled'))]", label=self.label))
        button[0].click()

class ActionList(ActionO):
    def __init__(self, label, choice):
        self.label = label
        self.choice = choice

    def perform(self, driver):
        print(f"Выбираю в списке '{self.label}' ответ '{self.choice}'")
        listOpen = Action.waitGetElement(driver, Action.getXpathBy(tag="input[contains(@class,'focusable-input')]", label=self.label))
        listOpen[0].click()
        listEl = Action.waitGetElement(driver, Action.getXpathBy(
            inside_component=False,
            tag="epgu-constructor-dropdown",
            label=self.label,
            add=f"*[contains(@class,'dropdown-list-wrapper')]//*[contains(@class,'dropdown-item')]//*[contains(.,'{self.choice}')]"
        ))
        listEl[0].click()

class ActionInput(ActionO):
    def __init__(self, label, text):
        self.label = label
        self.text = text

    def perform(self, driver):
        print(f"Пишу в поле '{self.label}' текст '{self.text}'")
        inputEl = Action.waitGetElement(driver, Action.getXpathBy(tag=["input", "div[contains(@class,'multiline-input')]"], label=self.label))
        inputEl[0].send_keys(self.text)

class ActionFileUpload(ActionO):
    def __init__(self, ext):
        self.ext = ext

    def perform(self, driver):
        print(f"Загружаю файл расширения '.{self.ext}'")
        inputUpload = Action.waitGetElement(driver, Action.getXpathBy(inside_component=False, tag="input[contains(@type,'file')]"))
        inputUpload[0].send_keys(f"{os.getcwd()}/files/tmp.{self.ext}")

class ActionDownloadVm(ActionO):
    def perform(self, driver):
        print(f"Скачиваю VM-шаблон")
        buttonDownload = Action.waitGetElement(driver, Action.getXpathBy(
            inside_component=False,
            tag="epgu-constructor-uploader-manager-item",
            label="application",
            add="button[contains(@class,'download_button')]"
        ))
        buttonDownload[0].click()


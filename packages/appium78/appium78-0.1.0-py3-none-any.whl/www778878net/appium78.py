import asyncio
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Appium78:
    def __init__(self, device_name, app_package, app_activity, appium_url="http://127.0.0.1:4723"):
        self.device_name = device_name
        self.appium_url = appium_url
        self.app_package = app_package
        self.app_activity = app_activity
        self.driver = None

    def initialize_driver(self):
        appium_options = {
            "platformName": "Android",
            "deviceName": self.device_name,
            "appPackage": self.app_package,
            "appActivity": self.app_activity,
            "automationName": "UiAutomator2",
            "noReset": True,
            "newCommandTimeout": 120000,
            "dontStopAppOnReset": True,
            "skipDeviceInitialization": True,
            "skipServerInstallation": True,
            "ignoreHiddenApiPolicyError": True,
            "disableWindowAnimation": True,
            "skipUnlock": True,
            "ignoreUnimportantViews": True,
            "allowTestPackages": True,
            "enforceAppInstall": False
        }
        self.driver = webdriver.Remote(self.appium_url, options=appium_options)

    async def perform_swipe_down(self):
        if not self.driver:
            raise Exception("Driver not initialized")

        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.7)
        end_y = int(size['height'] * 0.3)

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        await asyncio.sleep(2)

    def find_elements(self, by):
        if not self.driver:
            return []
        return self.driver.find_elements(by)

    def click_element(self, element):
        element.click()

    def get_page_source(self):
        return self.driver.page_source if self.driver else ""

    def quit(self):
        if self.driver:
            self.driver.quit()

    def get_element_dom_by_xpath(self, xpath):
        if not self.driver:
            return ""
        element = self.driver.find_element(AppiumBy.XPATH, xpath)
        return element.get_attribute("outerHTML") if element else ""
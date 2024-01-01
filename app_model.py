from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json
import pyautogui
import pyperclip
import os
from enum import Enum
FILE_PATH = "messages.txt"

class Platform(Enum):
    FB = "Facebook Marketplace"
    KJ = "Kijiji"

class AutomationModel:
    def __init__(self):
        self.messages_file = "messages.json"
        self.messages = self.get_messages()

    # Persistent Data
    def get_platforms(self):
        return ["Facebook Marketplace", "Kijiji"]
    
    def get_messages(self):
        try:
            if os.path.exists(FILE_PATH):
                with open(FILE_PATH, 'r') as file:
                    json_data = file.read()
                    data = json.loads(json_data)
                    return data
            else:
                return {}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

    def update_messages(self, messages):
        try:
            json_data = json.dumps(messages)
            with open('messages.txt', 'w') as file:
                file.write(json_data)
        except Exception as e:
            print(f"An error occurred: {e}")

    def increment_message_responses(self,title):
        messages = self.get_messages()
        messages[title][2] += 1
        self.update_messages(messages)

    def decrement_message_responses(self, title):
        messages = self.get_messages()
        messages[title][2]  -= 1
        self.update_messages(messages)
        
    # Business Logic
    def fb_login(self, driver, email, password):
        try:
            driver.get("https://www.facebook.com/login/?next=%2Fmarketplace%2F")
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(email)
            password_input = driver.find_element(By.NAME, "pass")
            password_input.send_keys(password)
            login_button = driver.find_element(By.ID, "loginbutton")
            login_button.click()
        except Exception as e:
            print("Error encountered:", e)

    def open_rentals(self, driver):
        try:
            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Marketplace']")))
            search_box.send_keys("rentals")
            search_box.send_keys(Keys.ENTER)
        except Exception as e: 
            print("Error encountered:", e)


    def send_msgs(self, driver, title, message):
        try:
            time.sleep(3)
            end_of_results_text = "Results from outside your search"
            listings = []
            found_end_of_results = False
            while not found_end_of_results:
                try:
                    listings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), '$')]")))
                    driver.find_element(By.XPATH, f"//*[contains(text(), '{end_of_results_text}')]")
                    found_end_of_results = True
                except:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            messages_sent = 0
            for listing in listings:
                listing.click()
                time.sleep(2)
                try:
                    driver.find_element(By.XPATH, "//span[contains(., 'Message Again')]")
                except NoSuchElementException:
                    time.sleep(3)
                    pyautogui.click(1150, 810)
                    time.sleep(3)
                    pyperclip.copy(message)
                    pyautogui.keyDown('command')
                    pyautogui.press('v')
                    pyautogui.moveTo(1150, 865)
                    pyautogui.click(500,500)
                    messages = self.get_messages()
                    messages[title][1] += 1
                    self.update_messages(messages)
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(2)
        except Exception as e:
            print("Error encountered:", e)

    def fb_automation(self, driver, email, password, title, message):
        self.fb_login(driver,email, password)
        time.sleep(3)
        self.open_rentals(driver)
        time.sleep(3)
        self.send_msgs(driver, title, message)
    
    def kijiji_automation():
        return
        
    def start_automation(self, platform, email, password, title, message):
        driver = webdriver.Firefox()
        driver.fullscreen_window()
        if platform == Platform.FB.value:
            self.fb_automation(driver, email, password, title, message)
        elif platform == Platform.KJ.value:
            self.kijiji_automation()
        driver.quit()

        

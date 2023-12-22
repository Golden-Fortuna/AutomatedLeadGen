from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from enum import Enum
import time
import pyautogui
import pyperclip

EMAIL = "maribellas.events@hotmail.com"
PASSWORD = "Selena21!"

MSG = (
    "My name is Ruben Solano, I own a property management company. "
    "I am doing some market research and had a question for you. "
    "Is there any price that would make you consider hiring property managers? "
    "\n\n"
    "I am not saying that whatever price you say I would be able to do, however "
    "I am trying to get a gauge for what investors like yourself are looking for! "
    "I really appreciate your time!"
)


def scroll_page(n):
    html = driver.find_element(By.TAG_NAME, 'html')
    for _ in range(n):
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(10) 

def send_msgs(driver):
    try:
        time.sleep(3)
        end_of_results_text = "Results from outside your search"
        listings = []
        found_end_of_results = False
        while not found_end_of_results:
            try:
                listings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), 'CA$')]")))
                driver.find_element(By.XPATH, f"//*[contains(text(), '{end_of_results_text}')]")
                found_end_of_results = True
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("size: " + str(len(listings)))
        messages_sent = 0
        for listing in listings:
            time.sleep(3)
            try:
                listing.click()
                time.sleep(3)
                pyautogui.click(1150, 810)
                time.sleep(3)
                pyperclip.copy(MSG)
                pyautogui.keyDown('command')
                pyautogui.press('v')
                pyautogui.click(1150, 865)
                time.sleep(40)
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()  # Close the detail view

            except Exception as e:
                print("Error Encountered: ", e)
        print(f"{messages_sent} messages sent to potential clients.")
    except Exception as e:
        print("Error encountered:", e)


def open_rentals(driver):
    try:
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Marketplace']")))
        search_box.send_keys("rentals")
        search_box.send_keys(Keys.ENTER)
    except Exception as e: 
        print("Error encountered:", e)


def fb_login(driver):
    try:
        driver.get("https://www.facebook.com/login/?next=%2Fmarketplace%2F")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(EMAIL)
        password_input = driver.find_element(By.NAME, "pass")
        password_input.send_keys(PASSWORD)
        login_button = driver.find_element(By.ID, "loginbutton")
        login_button.click()
    except Exception as e:
        print("Error encountered:", e)

if __name__ == "__main__":
    driver = webdriver.Firefox()
    fb_login(driver)
    time.sleep(3)
    open_rentals(driver)
    time.sleep(5)
    send_msgs(driver)
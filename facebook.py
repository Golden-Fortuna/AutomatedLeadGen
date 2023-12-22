import tkinter as tk
from threading import Thread
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from enum import Enum
import time
import pyautogui
import pyperclip

class AutomationApp:
    def __init__(self, master):
        self.master = master
        master.title("Facebook Automation")
        tk.Label(master, text="Email:").grid(row=0)
        self.email_entry = tk.Entry(master)
        self.email_entry.grid(row=0, column=1)
        tk.Label(master, text="Password:").grid(row=1)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1)
        tk.Label(master, text="Message:").grid(row=2)
        self.message_text = tk.Text(master, height=10, width=50)
        self.message_text.grid(row=2, column=1)
        self.start_button = tk.Button(master, text="Start Automation", command=self.start_automation)
        self.start_button.grid(row=3, column=1)
        self.status_label = tk.Label(master, text="", fg="green")
        self.status_label.grid(row=4, column=1)
    
    def send_msgs(self,driver,message):
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
            print(f"Collected {len(listings)} listings.")
            messages_sent = 0
            for listing in listings:
                listing.click()
                time.sleep(2)
                try:
                    element = driver.find_element(By.XPATH, "//span[contains(., 'Message Again')]")
                    print("Already Messaged...")
                except NoSuchElementException:
                    print("Sending Message...")
                    time.sleep(3)
                    pyautogui.click(1150, 810)
                    time.sleep(3)
                    pyperclip.copy(message)
                    pyautogui.keyDown('command')
                    pyautogui.press('v')
                    pyautogui.click(1150, 865)
                    pyautogui.click(500,500)
                    messages_sent += 1
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(2)
            return messages_sent
        except Exception as e:
            print("Error encountered:", e)

    def open_rentals(self,driver):
        try:
            search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search Marketplace']")))
            search_box.send_keys("rentals")
            search_box.send_keys(Keys.ENTER)
        except Exception as e: 
            print("Error encountered:", e)

    def fb_login(self,driver, email, password):
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

    def run_automation(self, email, password, message):
        driver = webdriver.Firefox()
        driver.fullscreen_window()

        self.fb_login(driver, email, password)
        time.sleep(3)
        self.open_rentals(driver)
        time.sleep(3)
        messages_sent = self.send_msgs(driver, message)
        driver.quit()
        return messages_sent

    def start_automation(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        message = self.message_text.get("1.0", tk.END)
        self.start_button.config(state="disabled")
        messages_sent = self.run_automation(email, password, message)
        self.status_label.config(text=f"{messages_sent} messages sent to potential clients.")
        self.start_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()


import tkinter as tk
from tkinter import ttk
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
        master.configure(bg='#2C2F33')  # Dark grey background

        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TNotebook', background='#2C2F33', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2C2F33', foreground='#FFF', padding=[10, 5], borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', '#23272A'), ('active', '#2C2F33')], foreground=[('selected', '#FFF'), ('active', '#AAA')])
        style.configure('TFrame', background='#2C2F33')
        style.configure('TButton', background='#23272A', foreground='#FFF', borderwidth=0)
        style.configure('TLabel', background='#2C2F33', foreground='#FFF', font=('Helvetica', 10))
        style.configure('TEntry', fieldbackground='#23272A', foreground='#FFF', borderwidth=0)
        style.map('TEntry', fieldbackground=[('focus', '#23272A')], foreground=[('focus', '#FFF')])

        tabControl = ttk.Notebook(master)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Automation')
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='Dashboard')
        tabControl.pack(expand=1, fill="both", padx=10, pady=10)

        self.create_automation_tab(tab1)
        self.create_dashboard_tab(tab2)

    def create_automation_tab(self, tab):
        ttk.Label(tab, text="Email:").grid(row=0, column=0, sticky='e', padx=(10, 0), pady=(10, 10))
        self.email_text = tk.Text(tab,height=1, width=50, bg='#23272A', fg='#FFF', borderwidth=0, insertbackground='#FFF')
        self.email_text.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky='ew')
        ttk.Label(tab, text="Password:").grid(row=1, column=0, sticky='e', padx=(10, 0), pady=(0, 10))
        self.password_text = tk.Text(tab,height=1, width=50, bg='#23272A', fg='#FFF', borderwidth=0, insertbackground='#FFF')
        self.password_text.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')
        ttk.Label(tab, text="Message:").grid(row=2, column=0, sticky='ne', padx=(10, 0), pady=(0, 10))
        self.message_text = tk.Text(tab, height=10, width=50, bg='#23272A', fg='#FFF', borderwidth=0, insertbackground='#FFF')
        self.message_text.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.start_button = ttk.Button(tab, text="Start Automation", command=self.start_automation)
        self.start_button.grid(row=3, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.status_label = ttk.Label(tab, text="", foreground='#32CD32')  # Lime green for visibility
        self.status_label.grid(row=4, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')

    def create_dashboard_tab(self, tab):
        self.dashboard_label = ttk.Label(tab, text="Dashboard will be updated here")
        self.dashboard_label.pack(pady=(10, 10))

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
        email = self.email_text.get("1.0", tk.END)
        password = self.password_text.get("1.0", tk.END)
        message = self.message_text.get("1.0", tk.END)
        self.start_button.config(state="disabled")
        messages_sent = self.run_automation(email, password, message)
        self.status_label.config(text=f"{messages_sent} messages sent to potential clients.")
        self.start_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()


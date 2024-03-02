from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json
import pyautogui
import pyperclip
import os
from enum import Enum

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)

# Get the directory of the current script
script_dir = os.path.dirname(script_path)
FILE_PATH = os.path.join(script_dir, "messages.txt")

class Platform(Enum):
    FB = "Facebook Marketplace"
    KJ = "Kijiji"

class AutomationModel:
    def __init__(self):
        self.messages_file = "messages.json"
        self.messages = self.get_messages()
        self.blacklist = self.load_blacklist()

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
    
    # Load blacklist
    def load_blacklist(self):
        blacklist_path = "blacklist.txt"
        if os.path.exists(blacklist_path):
            with open(blacklist_path, 'r') as file:
                return set(line.strip() for line in file)
        else:
            return set()
        
    def is_blacklisted(self, name):
        # Assumes `name` is a string with the format "First Last"
        # Modify this as needed to fit how names are presented in the listings
        return name in self.blacklist

    def add_to_blacklist(self, name):
        if name not in self.blacklist:
            self.blacklist.add(name)
            with open("blacklist.txt", 'a') as file:
                file.write(f"{name}\n")
        
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

    def close_chats(self, driver):
        # Check if message popped up. Close it if so
        close_chat_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Close chat']")

        # Check if any close chat buttons were found
        if close_chat_buttons:
            print(f"Found {len(close_chat_buttons)} close chat button(s). Closing all.")
            for button in close_chat_buttons:
                try:
                    button.click()
                except:
                    print("A button could not be closed because it is off screen.")
        else:
            print("No close chat buttons found.")


    def close_listing(self, driver):
        close_button = driver.find_element(By.XPATH, "//div[@aria-label='Close']")
        
        close_button.click()
        return

    def send_msgs(self, driver, title, message):
        try:
            time.sleep(3)
            end_of_results_text = "Results from outside your search"
            listings = []
            found_end_of_results = False
            max_listings = 360  # Maximum number of listings to load. Make a cap to stop infinite scroll
            print("Starting search")
            last_count = 0

            while not found_end_of_results and len(listings) < max_listings:
                try:
                    # Wait for the listings to be present and then retrieve all listings currently loaded
                    current_listings = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), '$')]"))
                    )
                    
                    # Calculate the number of new listings loaded in this iteration
                    new_listings = current_listings[last_count:]
                    
                    # Update the listings list with only new listings
                    listings.extend(new_listings)
                    
                    # Update the last_count for the next iteration
                    last_count = len(current_listings)

                    # Scroll to the bottom to load new listings
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    # Introduce a small delay to ensure new listings have time to load
                    # You might need to adjust this delay based on the website's loading speed
                    time.sleep(2)

                except TimeoutException:
                    # Handle the case where no new listings are found after scrolling
                    print("No new listings found after scrolling.")
                    found_end_of_results = True
                except Exception as e:
                    # Log other exceptions
                    print(f"An error occurred: {e}")
                    # Attempt to scroll in case of any failure to find elements, assuming more listings might be loaded
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # Delay to allow for loading
           
            messages_sent = 0
            print("Ended search")
            for listing in listings:
            
                
                time.sleep(1)
                
                self.close_chats(driver)
                
                listing.click()

                seller_name_parent_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "(//a[contains(@href, '/marketplace/profile')])[2]")
                    )
                )

                self.close_chats(driver)

                seller_name = seller_name_parent_element.accessible_name
                
                if self.is_blacklisted(seller_name):
                    print(f"Skipping blacklisted seller: {seller_name}")
                    self.close_listing(driver)
                    continue

                try:
                    driver.find_element(By.XPATH, "//span[contains(., 'Message Again')]")
                except NoSuchElementException:
                 
                    try:
                        
                        # XPath to find all <textarea> elements containing the specified text
                        xpath = "//textarea[text()='Hi, is this available?']"

                        # Wait for at least two such elements to be present
                        elements = WebDriverWait(driver, 10).until(
                            lambda driver: driver.find_elements(By.XPATH, xpath) if len(driver.find_elements(By.XPATH, xpath)) >= 2 else False
                        )
                        
                        self.close_chats(driver)
                        
                        textarea = elements[1]
                        
                        # Click the textarea to focus
                        textarea.click()
                    
                    except:
                        self.close_listing(driver)
                        time.sleep(3) # To not be suspicious
                        continue
                    
  
                    time.sleep(3)
                    self.close_chats(driver)
                    textarea.send_keys(message)
                    
                    # Find the Send button
                    xpath = "//span[text()='Send']"

                    # Wait for at least two such elements to be present
                    elements = WebDriverWait(driver, 10).until(
                        lambda driver: driver.find_elements(By.XPATH, xpath) if len(driver.find_elements(By.XPATH, xpath)) >= 2 else False
                    )
                    self.close_chats(driver)
                    
                    send_button = elements[1]
                    
                    send_button.click()
                    
                    messages = self.get_messages()
                    messages[title][1] += 1
                    self.update_messages(messages)

                
                self.add_to_blacklist(seller_name)
                time.sleep(3) # To not be suspicious
                self.close_chats(driver)
                self.close_listing(driver)
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
        if platform == Platform.FB.value:
            self.fb_automation(driver, email, password, title, message)
        elif platform == Platform.KJ.value:
            self.kijiji_automation()
        driver.quit()

        

from app_model import AutomationModel
import json

class AppViewModel:
    def __init__(self):
        self.model = AutomationModel()
        self.email = ""
        self.password = ""
        self.message = ""

    def update_credentials(self, email, password, message):
        self.email = email
        self.password = password
        self.message = message

    def start_automation(self, platform, email, password, title, message):
        self.model.start_automation(platform, email, password, title, message)

    def get_messages(self):
        return self.model.get_messages()
    
    def update_messages(self, messages):
        self.model.update_messages(messages)
    
    def increment_message_responses(self, title):
        self.model.increment_message_responses(title)
    
    def decrement_message_responses(self, title):
        self.model.decrement_message_responses(title)
    
    def delete_messages(self, message_title):
        return

    def get_platforms(self):
        return self.model.get_platforms()
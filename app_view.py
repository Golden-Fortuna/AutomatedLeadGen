from app_view_model import AppViewModel
import tkinter as tk
from tkinter import ttk
from enum import Enum

class Action(Enum):
    ADD =  "ADD"
    EDIT = "EDIT"

class AppView:
    def __init__(self, master):
        self.master = master
        self.viewmodel = AppViewModel()
        master.title("Automated Lead Generation")
        master.configure(bg='#2C2F33')
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TNotebook', background='#2C2F33', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2C2F33', foreground='#FFF', padding=[10, 5], borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', '#23272A'), ('active', '#2C2F33')],
                   foreground=[('selected', '#FFF'), ('active', '#AAA')])
        style.configure('TFrame', background='#2C2F33')
        style.configure('TButton', background='#23272A', foreground='#FFF', borderwidth=0)
        style.configure('TLabel', background='#2C2F33', foreground='#FFF', font=('Helvetica', 10))
        style.configure('TEntry', fieldbackground='#23272A', foreground='#FFF', borderwidth=0)
        style.map('TEntry', fieldbackground=[('focus', '#23272A')], foreground=[('focus', '#FFF')])
        tabControl = ttk.Notebook(master)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Automation')
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='A/B Testing')
        tabControl.pack(expand=1, fill="both", padx=10, pady=10)
        tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.create_automation_tab(tab1)
        self.create_dashboard_tab(tab2)

    # AUTOMATION___________________________________________________
    def create_automation_tab(self, tab):
        tab.columnconfigure(1, weight=1) 
        ttk.Label(tab, text="Platform:").grid(row=0, column=0, sticky='e', padx=(10, 0), pady=(10, 10))
        self.platforms_var = tk.StringVar()
        self.platforms_dropdown = ttk.Combobox(tab, textvariable=self.platforms_var, state='readonly')
        self.platforms_dropdown['values'] = self.viewmodel.get_platforms()
        self.platforms_dropdown.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky='ew')
        ttk.Label(tab, text="Email:").grid(row=1, column=0, sticky='e', padx=(10, 0), pady=(10, 10))
        self.email_text = tk.Text(tab, height=1, bg='#23272A', fg='#FFF', borderwidth=0, insertbackground='#FFF')
        self.email_text.grid(row=1, column=1, padx=(0, 10), pady=(10, 10), sticky='ew')
        self.email_text.grid(row=1, column=1, padx=(0, 10), pady=(10, 10), sticky='ew')
        ttk.Label(tab, text="Password:").grid(row=2, column=0, sticky='e', padx=(10, 0), pady=(10, 10))
        self.password_text = tk.Text(tab, height=1, bg='#23272A', fg='#FFF', borderwidth=0, insertbackground='#FFF')
        self.password_text.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')
        ttk.Label(tab, text="Message:").grid(row=4, column=0, sticky='e', padx=(10, 0), pady=(0, 10))
        self.message_var = tk.StringVar()
        self.messages_dropdown = ttk.Combobox(tab, textvariable=self.message_var, state='readonly')
        self.messages_dropdown['values'] = tuple(self.viewmodel.get_messages().keys())
        self.messages_dropdown.grid(row=4, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.add_message_button = ttk.Button(tab, text="Add", command=lambda: self.show_message_fields(Action.ADD))
        self.add_message_button.grid(row=4, column=2, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.edit_message_button = ttk.Button(tab, text="Edit", command=lambda: self.show_message_fields(Action.EDIT))
        self.edit_message_button.grid(row=4, column=3, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.delete_message_button = ttk.Button(tab, text="Delete", command=self.create_delete_confirmation_popup)
        self.delete_message_button.grid(row=4, column=4, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.start_button = ttk.Button(tab, text="Start Automation", command=self.start_automation)
        self.start_button.grid(row=7, column=1, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.message_title_label = ttk.Label(tab, text="Message Title:")
        self.message_title_label.grid(row=5, column=0, sticky='e', padx=(10, 0), pady=(10, 10))
        self.message_title_text = tk.Text(tab, height=1, bg='#23272A', fg='#FFF', borderwidth=0, insertbackground='#FFF')
        self.message_title_text.grid(row=5, column=1, padx=(0, 10), pady=(10, 10), sticky='ew')
        self.message_frame = ttk.Frame(tab)
        self.message_frame.grid(row=6, column=1, padx=(0, 10), pady=(10, 10), sticky='nsew')
        tab.columnconfigure(1, weight=1)  
        self.message_frame.rowconfigure(0, weight=1)  
        self.message_frame.columnconfigure(0, weight=1)  
        self.message_label = ttk.Label(tab, text="Message Content:")
        self.message_label.grid(row=6, column=0, sticky='e', padx=(10, 0), pady=(10, 10))
        self.new_message_text = tk.Text(self.message_frame, height=5, bg='#23272A', fg='#FFF', borderwidth=0, insertbackground='#FFF')
        self.new_message_text.grid(row=0, column=0, sticky='nsew')
        self.message_scrollbar = tk.Scrollbar(self.message_frame, command=self.new_message_text.yview)
        self.message_scrollbar.grid(row=0, column=1, sticky='ns')
        self.new_message_text.config(yscrollcommand=self.message_scrollbar.set)
        self.cancel_button = ttk.Button(tab, text="Cancel", command=self.hide_message_fields)
        self.cancel_button.grid(row=6, column=2, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.confirm_add_button = ttk.Button(tab, text="Add Message", command=self.add_message)
        self.confirm_add_button.grid(row=6, column=3, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.apply_edit_button = ttk.Button(tab, text="Apply Edit", command=self.edit_messages)
        self.apply_edit_button.grid(row=6, column=3, padx=(0, 10), pady=(0, 10), sticky='ew')
        self.message_title_label.grid_remove()
        self.message_title_text.grid_remove()
        self.message_label.grid_remove()
        self.new_message_text.grid_remove()
        self.confirm_add_button.grid_remove()
        self.cancel_button.grid_remove()
        self.apply_edit_button.grid_remove()
        self.message_scrollbar.grid_remove()

    def show_message_fields(self, action):
        self.message_title_label.grid()        
        self.message_title_text.grid()         
        self.message_label.grid()          
        self.new_message_text.grid()          
        self.message_scrollbar.grid()
        if action == Action.ADD:
            self.confirm_add_button.grid()         
            self.message_title_text.config(state='normal')
        elif action == Action.EDIT:
            self.apply_edit_button.grid()
            if self.message_var.get():
                title = self.message_var.get()
                messages = self.viewmodel.get_messages()
                message = messages[title][0]
                self.message_title_text.insert("1.0", title)
                self.new_message_text.insert("1.0", message)
                self.message_title_text.config(state='disabled')
        self.cancel_button.grid()              
        self.add_message_button.grid_remove()  
        self.edit_message_button.grid_remove()
        self.delete_message_button.grid_remove()
    
    def hide_message_fields(self):
        self.message_title_text.delete("1.0", tk.END)
        self.new_message_text.delete("1.0", tk.END)
        self.message_title_label.grid_remove()  
        self.message_title_text.grid_remove()   
        self.message_label.grid_remove()   
        self.new_message_text.grid_remove()     
        self.confirm_add_button.grid_remove()   
        self.cancel_button.grid_remove()       
        self.apply_edit_button.grid_remove() 
        self.message_scrollbar.grid_remove()
        self.add_message_button.grid()         
        self.edit_message_button.grid()
        self.delete_message_button.grid()
    
    def add_message(self):
        title = self.message_title_text.get("1.0", tk.END).strip()
        message_content = self.new_message_text.get("1.0", tk.END).strip()
        messages = self.viewmodel.get_messages()
        if title and message_content:
            messages[title] = [message_content, 0, 0]
            self.viewmodel.update_messages(messages) 
            self.messages_dropdown['values'] = tuple(messages.keys())
            self.messages_dropdown.set(title)
            self.hide_message_fields()

    def edit_messages(self):
        title = self.message_title_text.get("1.0", tk.END).rstrip('\n')
        messages = self.viewmodel.get_messages()
        if title in messages:
            messages[title][0] = self.new_message_text.get("1.0", tk.END).rstrip('\n')
            self.viewmodel.update_messages(messages)
            self.hide_message_fields()

    def confirm_delete(self, popup):
        title = self.message_var.get()
        messages = self.viewmodel.get_messages()
        if title in messages:
            messages.pop(title)
            self.viewmodel.update_messages(messages)
            self.messages_dropdown['values'] = tuple(messages.keys())
            self.message_var.set("")
        popup.destroy()

    def start_automation(self):
        platform = self.platforms_dropdown.get()
        email = self.email_text.get("1.0", tk.END).strip()
        password = self.password_text.get("1.0", tk.END).strip()
        message_title = self.messages_dropdown.get()
        messages = self.viewmodel.get_messages()
        if all([platform, email, password, message_title]) and message_title in messages:
            message_content = messages[message_title][0]
            self.viewmodel.start_automation(platform, email, password, message_title, message_content)
    

    def create_delete_confirmation_popup(self):
        popup = tk.Toplevel()
        popup.title("Confirm Delete")
        popup.geometry("300x100") 
        popup.configure(bg='#2C2F33')
        warning_label = tk.Label(popup, text="You will not be able to recover this message", font=("Helvetica", 10), bg='#2C2F33', fg='#FFF')
        warning_label.pack(pady=(10, 10), padx=(10, 10))
        button_frame = tk.Frame(popup, bg='#2C2F33')
        button_frame.pack(fill='x', padx=50) 
        cancel_button = tk.Button(button_frame, text="Cancel", command=popup.destroy, background='#23272A', borderwidth=0)
        cancel_button.pack(side='left', expand=True)  
        confirm_button = tk.Button(button_frame, text="Confirm Delete", command=lambda: self.confirm_delete(popup), background='#23272A', borderwidth=0)
        confirm_button.pack(side='right', expand=True)  

    # DASHBOARD________________________________________________
    def create_dashboard_tab(self, tab):
        self.dashboard_frame = ttk.Frame(tab, style='TFrame')
        self.dashboard_frame.pack(fill='both', expand=True)
        self.refresh_dashboard()

    def calculate_conversion_rate(self, sent, responses):
        return (responses / sent * 100) if sent else 0

    def refresh_dashboard(self):
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        columns = ('title', 'sent', 'responses', 'conversion_rate', 'increment', 'decrement')
        self.tree = ttk.Treeview(self.dashboard_frame, columns=columns, show='headings')
        self.tree.heading('title', text='Title')
        self.tree.heading('sent', text='Sent')
        self.tree.heading('responses', text='Responses')
        self.tree.heading('conversion_rate', text='Conversion Rate (%)')
        self.tree.heading('increment', text='Increment')
        self.tree.heading('decrement', text='Decrement')
        self.tree.column('title', width=200, anchor='center')
        self.tree.column('sent', width=80, anchor='center')
        self.tree.column('responses', width=80, anchor='center')
        self.tree.column('conversion_rate', width=120, anchor='center')
        self.tree.column('increment', width=60, anchor='center')
        self.tree.column('decrement', width=60, anchor='center')

        messages = self.viewmodel.get_messages()
        for title, stats in messages.items():
            sent_count = stats[1]
            response_count = stats[2]
            conversion_rate = self.calculate_conversion_rate(sent_count, response_count)
            self.tree.insert('', tk.END, values=(title, sent_count, response_count, f'{conversion_rate:.2f}', '+', '-'))

        self.tree.pack(expand=True, fill='both')
        self.tree.bind('<ButtonRelease-1>', self.on_treeview_click)

    def on_treeview_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)

        if region == 'cell' and item:
            title = self.tree.item(item, 'values')[0]
            column_text = self.tree.heading(column, 'text')
            if column_text == 'Increment':
                self.increment_response_count(title)
            elif column_text == 'Decrement':
                self.decrement_response_count(title)

    def increment_response_count(self, title):
        self.viewmodel.increment_message_responses(title)
        self.refresh_dashboard()

    def decrement_response_count(self, title):
        self.viewmodel.decrement_message_responses(title)
        self.refresh_dashboard()

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "A/B Testing":
            self.refresh_dashboard()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = AppView(root)
    root.mainloop()

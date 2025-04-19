import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, scrolledtext
import datetime
from infrastructure.network.client_socket import ClientSocket
import re

class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("💬 Python Chat Client")
        self.master.geometry("750x520")
        self.master.configure(bg="#ecf0f1")

        # Use a modern ttk theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        padding=6,
                        relief="flat",
                        background="#3498db",
                        foreground="white",
                        font=('Segoe UI', 10))
        style.map("TButton",
                  background=[("active", "white")],
                  foreground=[("active", "#3498db")])

        style.configure("TCombobox",
                        fieldbackground="#ecf0f1",
                        background="white",
                        foreground="black",
                        arrowcolor="#3498db")
        style.map("TCombobox",
                  fieldbackground=[("active", "white")],
                  foreground=[("active", "black")])

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(master, state='disabled', height=20,
                                                      bg="white", fg="#2c3e50",
                                                      font=("Segoe UI", 11))
        self.chat_display.pack(padx=10, pady=(10, 5), fill='both', expand=True)

        # Frame for message + send
        msg_frame = tk.Frame(master, bg="#ecf0f1")
        msg_frame.pack(padx=10, pady=(0, 10), fill='x')

        # Message entry
        self.entry_field = tk.Entry(msg_frame, font=("Segoe UI", 11), bg="white", relief=tk.FLAT)
        self.entry_field.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_field.bind("<Return>", self.send_message)

        # Send button (small and neat)
        self.send_button = ttk.Button(msg_frame, text="📤", width=3, command=self.send_message)
        self.send_button.pack(side='left')

        # Frame for bottom controls
        bottom_frame = tk.Frame(master, bg="#ecf0f1")
        bottom_frame.pack(fill='x', padx=10, pady=(0, 10))

        # Dropdown for private messaging
        self.pm_user_var = tk.StringVar()
        self.pm_user_dropdown = ttk.Combobox(bottom_frame, textvariable=self.pm_user_var, state='readonly',
                                             font=("Segoe UI", 10), width=30)
        self.pm_user_dropdown.pack(side='left', padx=(0, 10))
        self.pm_user_dropdown.set("Send to all")

        # Reconnect button
        self.reconnect_button = ttk.Button(bottom_frame, text="🔄 Reconnect", command=self.reconnect)
        self.reconnect_button.pack(side='right')

        # User list
        self.user_listbox = tk.Listbox(master, width=25, bg="#dfe6e9", fg="#2c3e50", font=("Segoe UI", 10))
        self.user_listbox.pack(padx=10, pady=(0, 10), fill='y', side='right')
        
        # Username prompt (Updated)
        self.username = self.prompt_username()
        if not self.username:
            messagebox.showerror("Input Error", "Username is required.")
            master.destroy()
            return

        self.connect_client()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def prompt_username(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Enter Username")
        dialog.geometry("300x150")
        dialog.configure(bg="#ecf0f1")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(self.master)

        tk.Label(dialog, text="Enter your username to join the chat", bg="#ecf0f1",
                 font=("Segoe UI", 11, "bold"), fg="#2c3e50").pack(pady=(20, 10))

        username_var = tk.StringVar()

        username_entry = tk.Entry(dialog, textvariable=username_var, font=("Segoe UI", 11),
                                  justify="center", relief="flat")
        username_entry.pack(pady=(0, 15), ipadx=10, ipady=5)
        username_entry.focus()

        def submit():
            name = username_var.get().strip()
            if name:
                dialog.destroy()
            else:
                messagebox.showerror("Input Error", "Username cannot be empty.")

        submit_btn = tk.Button(dialog, text="Join", command=submit,
                               bg="#3498db", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
        submit_btn.pack()
        username_entry.bind("<Return>", lambda e: submit())

        self.master.wait_window(dialog)
        return username_var.get().strip()

    def connect_client(self):
        self.client = ClientSocket(host='192.168.1.104', port=1485, username=self.username)
        self.client.on_message = self.display_message
        self.client.on_user_list = self.update_user_list

        if not self.client.connect():
            messagebox.showerror("Connection Error", "Could not connect to server.")
            return False
        return True

    def reconnect(self):
        self.client.close()
        if self.connect_client():
            self.display_message("[INFO] Reconnected successfully.")
        else:
            self.display_message("[ERROR] Reconnection failed.")

    def send_message(self, event=None):
        message = self.entry_field.get().strip()
        if message:
            target_user = self.pm_user_var.get()
            if target_user != "Send to all":
                message = f"pm {target_user} {message}"
            self.client.send(message)
            self.entry_field.delete(0, tk.END)

    def display_message(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        # Replace [username@ip] with [username]
        message = re.sub(r"\[(\w+)@\d{1,3}(?:\.\d{1,3}){3}\]", r"[\1]", message)

        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"[{timestamp}] {message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def update_user_list(self, users):
        self.user_listbox.delete(0, tk.END)
        filtered_users = [user for user in users if user != self.username]
        for user in filtered_users:
            self.user_listbox.insert(tk.END, user)
        self.pm_user_dropdown['values'] = ["Send to all"] + filtered_users

    def on_closing(self):
        self.client.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatClientGUI(root)
    root.mainloop()

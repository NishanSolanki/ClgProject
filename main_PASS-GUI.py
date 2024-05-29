import os, string, random, webbrowser, sys, getpass, tkinter as tk
from tkinter import messagebox, font
from usb_authenticator import generate_key
import datetime

# appending directory which contains this file to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Defining relative paths to the current script
project_path = os.path.join(os.getcwd(), "PROJECT")
op_folder_path = os.path.join(project_path, "OP")
usb_data_folder_path = os.path.join(project_path, "usb_data")

def initialize_usb():
    password = input("Enter a password for the USB: ")
    salt = os.urandom(16)

    key = generate_key(password.encode(), salt)

    folder_path = os.path.join(os.getcwd(), "usb_data")
    os.makedirs(folder_path, exist_ok=True)

    with open(os.path.join(folder_path, "usb_key.bin"), "wb") as key_file:
        key_file.write(key)
    with open(os.path.join(folder_path, "salt.bin"), "wb") as salt_file:
        salt_file.write(salt)

def authenticate():
    password = getpass.getpass(prompt="Enter the USB password: ")

    folder_path = os.path.join(os.getcwd(), "usb_data")

    with open(os.path.join(folder_path, "usb_key.bin"), "rb") as key_file:
        key = key_file.read()
    with open(os.path.join(folder_path, "salt.bin"), "rb") as salt_file:
        salt = salt_file.read()

    entered_key = generate_key(password.encode(), salt)

    if entered_key == key:
        return True
    else:
        return False

def generate_password(length=16):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def save_password(app_name, username, password):
    """Save a password for an application."""
    with open('OP/passwords.txt', 'a') as file:
        file.write(f'{app_name} : {username} : {password}\n')
    
    with open('OP/pass_logs.txt', 'a') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f'{timestamp} - Password saved for {app_name} : {username}\n')

def remove_password(app_name, username):
    """Remove a password for a given application and username."""
    with open('OP/passwords.txt', 'r') as file:
        lines = file.readlines()

    with open('OP/passwords.txt', 'w') as file:
        for line in lines:
            if f'{app_name} : {username}' not in line:
                file.write(line)
    
    with open('OP/pass_logs.txt', 'a') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f'{timestamp} - Password removed for {app_name} : {username}\n')

def display_passwords():
    """Display all stored passwords."""
    with open('OP/passwords.txt', 'r') as file:
        passwords = file.readlines()
        if passwords:
            password_list = "\n".join(passwords)
            messagebox.showinfo("Stored Passwords", f"List of Stored Passwords:\n{password_list}")
        else:
            messagebox.showinfo("Stored Passwords", "No passwords stored yet.")

def check_unique_username(app_name, username):
    """Check if a username is unique for a given application."""
    with open('OP/passwords.txt', 'r') as file:
        lines = file.readlines()
        existing_usernames = [line.split(' : ')[1] for line in lines if line.startswith(app_name)]
    return username not in existing_usernames

def generate_password_command():
    """Command to generate and display a random password."""
    password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(tk.END, password)

def save_password_command():
    """Command to save password for an application."""
    app_name = app_name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if check_unique_username(app_name, username):
        save_password(app_name, username, password)
        messagebox.showinfo("Password Saved", "Password saved successfully.")
    else:
        messagebox.showerror("Error", "Username must be unique for the same app.")

def remove_password_command():
    """Command to remove password for an application."""
    app_name = app_name_entry.get()
    username = username_entry.get()
    
    if not app_name and not username:  # Check if both app_name and username are blank
        messagebox.showinfo("No Values Provided", "No values provided. No passwords removed.")
        return

    remove_password(app_name, username)
    messagebox.showinfo("Password Removed", "Password removed successfully.")

def display_passwords_command():
    """Command to display all stored passwords."""
    display_passwords()

def open_readme(event):
    """Open README file."""
    try:
        webbrowser.open("file://" + os.path.abspath("README_FOR_PASSWORD_MANAGER.md"))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open README file: {e}")

if not os.path.exists(os.path.join(os.getcwd(), "usb_data", "usb_key.bin")):
    initialize_usb()
else:
    if not authenticate():
        print("Authentication failed. Exiting.")
        exit()

# GUI Setup
root = tk.Tk()
root.title("Password Manager")

# Styling for labels and entry placeholders
label_font = font.Font(family="Helvetica", size=14, weight="bold")
placeholder_font = font.Font(family="Helvetica", size=12)
placeholder_color = "#000000"

# Labels
tk.Label(root, text="App Name:",font=label_font).grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
tk.Label(root, text="Username:",font=label_font).grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
tk.Label(root, text="Password:",font=label_font).grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

# Entry Fields
app_name_entry = tk.Entry(root, font=placeholder_font, fg=placeholder_color)
app_name_entry.grid(row=0, column=1, padx=5, pady=5)
username_entry = tk.Entry(root, font=placeholder_font, fg=placeholder_color)
username_entry.grid(row=1, column=1, padx=5, pady=5)
password_entry = tk.Entry(root, font=placeholder_font, fg=placeholder_color)
password_entry.grid(row=2, column=1, padx=5, pady=5)

# Styling
button_font = font.Font(family="Helvetica", size=12, weight="bold")
label_font = font.Font(family="Helvetica", size=14, weight="bold")

# Buttons
generate_password_button = tk.Button(root, text="Generate Password", command=generate_password_command, font=button_font, bg="#4CAF50", fg="white")
generate_password_button.grid(row=2, column=2, padx=5, pady=5)
save_password_button = tk.Button(root, text="Save Password", command=save_password_command, font=button_font, bg="#2196F3", fg="white")
save_password_button.grid(row=3, column=0, padx=5, pady=5)
remove_password_button = tk.Button(root, text="Remove Password", command=remove_password_command, font=button_font, bg="#f44336", fg="white")
remove_password_button.grid(row=3, column=1, padx=5, pady=5)
display_passwords_button = tk.Button(root, text="Display Passwords", command=display_passwords_command, font=button_font, bg="#FF9800", fg="white")
display_passwords_button.grid(row=3, column=2, padx=5, pady=5)

# Help Label
help_frame = tk.Frame(root)
help_frame.grid(row=4, column=0, columnspan=3, pady=5, sticky="se")
help_label = tk.Label(help_frame, text="HELP", fg="blue", cursor="hand2", font=label_font)
help_label.pack()
help_label.bind("<Button-1>", open_readme)

root.mainloop()

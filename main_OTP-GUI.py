import os, pyotp, datetime, webbrowser, sys,getpass, tkinter as tk, pyscreenshot as ImageGrab, pyzbar.pyzbar as pyzbar, logging 
from tkinter import simpledialog, messagebox, font
from  usb_authenticator import generate_key

#logging.basicConfig(filename='app.log',filemode='a',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.debug('This is a debug message')
#logging.info('This is an info message')
#logging.warning('This is a warning message')
#logging.error('This is an error message')
#logging.critical('This is a critical message')


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

def generate_totp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp.now()
    
def log_otp_generation(app_name):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    with open("OP/otp_generation_log.txt", "a") as log_file:
        log_file.write(f"{app_name} : OTP generated at {timestamp}\n")

def load_keys():
    """Load stored keys from file."""
    keys = {}
    try:
        with open("OP/stored_keys.txt", "r") as file:
            for line in file:
                app_name, secret_key = line.strip().split(':')
                keys[app_name] = secret_key
    except FileNotFoundError:
        pass
    return keys

def generate_totp_command():
    """Command to generate TOTP for selected app."""
    stored_keys = load_keys()
    if not stored_keys:
        messagebox.showinfo("Error", "No stored keys. Please register a new key first.")
        return

    keys_list = "\n".join(stored_keys.keys())
    selected_app = simpledialog.askstring("Select 2FA App", f"Choose from the following registered apps:\n{keys_list}")

    if selected_app and selected_app in stored_keys:
        totp_code = generate_totp(stored_keys[selected_app])
        messagebox.showinfo("Generated TOTP", f"TOTP for {selected_app}: {totp_code}, valid for next 30 seconds")
        log_otp_generation(selected_app)
    elif selected_app:
        messagebox.showinfo("Error", "Invalid app name.")

def register_new_key_command():
    """Command to register a new key."""
    app_name = simpledialog.askstring("Register New Key", "Enter the name of the 2FA app:")
    secret_key = simpledialog.askstring("Register New Key", "Enter the shared secret key:")
    if app_name and secret_key:
        save_key(app_name, secret_key)
        messagebox.showinfo("Registration Successful", "New key registered successfully.")
    else:
        messagebox.showinfo("Error", "Invalid input.")


def remove_key_command():
    """Command to remove a registered key."""
    stored_keys = load_keys()
    if not stored_keys:
        messagebox.showinfo("Error", "No stored keys to remove.")
        return

    keys_list = "\n".join(stored_keys.keys())
    selected_app = simpledialog.askstring("Remove Key", f"Choose from the following registered apps:\n{keys_list}")

    if selected_app and selected_app in stored_keys:
        del stored_keys[selected_app]
        update_stored_keys_file(stored_keys)
        messagebox.showinfo("Key Removed", f"Key for {selected_app} removed successfully.")
    elif selected_app:
        messagebox.showinfo("Error", "Invalid app name.")

def list_registered_keys_command():
    """Command to list registered keys."""
    stored_keys = load_keys()
    if not stored_keys:
        messagebox.showinfo("Info", "No registered keys.")
        return

    keys_list = "\n".join(stored_keys.keys())
    messagebox.showinfo("Registered Keys", f"Registered 2FA Apps:\n{keys_list}")

def save_key(app_name, secret_key):
    """Save a new key."""
    secret_key = secret_key.replace(" ", "")
    stored_keys = load_keys()
    stored_keys[app_name] = secret_key
    update_stored_keys_file(stored_keys)

def update_stored_keys_file(stored_keys):
    """Update stored keys file."""
    with open("OP/stored_keys.txt", "w") as file:
        for app_name, secret_key in stored_keys.items():
            file.write(f"{app_name}:{secret_key}\n")

def open_readme(event):
    """Open README file."""
    try:
        webbrowser.open("file://" + os.path.abspath("README_FOR_OTP_GENERATOR.md"))
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
root.title("2FA App")

# Styling
button_font = font.Font(family="Helvetica", size=12, weight="bold")
label_font = font.Font(family="Helvetica", size=14, weight="bold")

# Buttons
generate_button = tk.Button(root, text="Generate TOTP", command=generate_totp_command, font=button_font, bg="#4CAF50", fg="white")
generate_button.pack(padx=10, pady=5, ipadx=10, ipady=5)
register_button = tk.Button(root, text="Register New Key", command=register_new_key_command, font=button_font, bg="#2196F3", fg="white")
register_button.pack(padx=10, pady=5, ipadx=10, ipady=5)
remove_button = tk.Button(root, text="Remove Key", command=remove_key_command, font=button_font, bg="#f44336", fg="white")
remove_button.pack(padx=10, pady=5, ipadx=10, ipady=5)
list_button = tk.Button(root, text="List Registered Keys", command=list_registered_keys_command, font=button_font, bg="#FF9800", fg="white")
list_button.pack(padx=10, pady=5, ipadx=10, ipady=5)


# Help button
help_frame = tk.Frame(root)
help_frame.pack(side="top", anchor="ne", padx=10, pady=5)
help_label = tk.Label(help_frame, text="HELP", fg="blue", cursor="hand2", font=label_font)
help_label.pack()
help_label.bind("<Button-1>", open_readme)

root.mainloop()



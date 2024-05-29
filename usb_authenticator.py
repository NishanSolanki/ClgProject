import os, shutil, getpass, base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def initialize_usb():
    password = getpass.getpass(prompt="Enter a password for the USB: ")
    salt = os.urandom(16)

    key = generate_key(password.encode(), salt)

    # Define folder path within the current directory
    folder_path = os.path.join(os.getcwd(), "usb_data")

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Store the key and salt in the folder
    with open(os.path.join(folder_path, "usb_key.bin"), "wb") as key_file:
        key_file.write(key)
    with open(os.path.join(folder_path, "salt.bin"), "wb") as salt_file:
        salt_file.write(salt)

def authenticate():
    password = getpass.getpass(prompt="Enter the USB password: ")

    # Retrieve key and salt from storage 
    with open(os.path.join(os.getcwd(), "usb_data", "usb_key.bin"), "rb") as key_file:
        key = key_file.read()
    with open(os.path.join(os.getcwd(), "usb_data", "salt.bin"), "rb") as salt_file:
        salt = salt_file.read()

    entered_key = generate_key(password.encode(), salt)

    if entered_key == key:
        return True
    else:
        return False

# Main program
if not os.path.exists(os.path.join(os.getcwd(), "usb_data", "usb_key.bin")):
    initialize_usb()
else:
    if not authenticate():
        print("Authentication failed. Exiting.")
        exit()

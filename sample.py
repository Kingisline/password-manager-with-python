import os
import json
import cryptography
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox, simpledialog
import pyperclip  

# Paths
PASSWORDS_FILE = "passwords.json"
KEY_FILE = "key.key"
AUTH_FILE = "auth.key"

# Generate or load encryption key
def load_key():
    # Check if the key file exists
    if not os.path.exists(KEY_FILE):
        print("Key file not found. Generating a new key.")  # Debugging: log the key generation
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print(f"New key generated and saved: {key.decode()}")  # Debugging: log the new key
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
        # print(f"Loaded key: {key.decode()}")   Debugging: log the loaded key
    return key


def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()

# Save or load passwords
def load_passwords():
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_passwords(passwords):
    with open(PASSWORDS_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

# Authentication passkey
def setup_auth_key():
    if not os.path.exists(AUTH_FILE):
        passkey = simpledialog.askstring("Setup Passkey", "Create a passkey for accessing the Password Manager:", show='*')
        if passkey:
            try:
                # Encrypt the passkey before saving
                key = load_key()
                encrypted_passkey = encrypt_data(passkey, key)
                
                # Save the encrypted passkey
                with open(AUTH_FILE, "w") as auth_file:
                    auth_file.write(encrypted_passkey)
                print(f"Encrypted passkey: {encrypted_passkey}")  # Debug: print the encrypted passkey
                messagebox.showinfo("Success", "Passkey set up successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while setting up the passkey: {e}")
                exit()
        else:
            messagebox.showerror("Error", "Passkey setup failed.")
            exit()

# Authentication passkey
def authenticate_user():
    if not os.path.exists(AUTH_FILE):
        setup_auth_key()

    try:
        # Read and decrypt the passkey
        with open(AUTH_FILE, "r") as auth_file:
            encrypted_passkey = auth_file.read()
        
        # print(f"Encrypted passkey read from file: {encrypted_passkey}")   Debug: print the data read from file
        
        key = load_key()
        decrypted_passkey = decrypt_data(encrypted_passkey, key)

       # print(f"Decrypted passkey: {decrypted_passkey}")   Debug: print the decrypted passkey
        
        for _ in range(3):
            entered_passkey = simpledialog.askstring("Authentication", "Enter your passkey:", show='*')
            if entered_passkey == decrypted_passkey:
                return True
            else:
                messagebox.showwarning("Incorrect Passkey", "The passkey entered is incorrect.")
        
        messagebox.showerror("Access Denied", "Too many incorrect attempts. Exiting.")
        exit()

    except cryptography.fernet.InvalidToken:
        messagebox.showerror("Decryption Error", "Failed to decrypt the passkey. The data may be corrupted or the key does not match.")
        exit()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during authentication: {e}")
        exit()


# Password Manager UI Functions
def add_password_ui(passwords, key):
    website = simpledialog.askstring("Add Password", "Enter the website:")
    username = simpledialog.askstring("Add Password", "Enter the username:")
    password = simpledialog.askstring("Add Password", "Enter the password:", show='*')

    if website and username and password:
        encrypted_password = encrypt_data(password, key)
        if website not in passwords or not isinstance(passwords[website], list):
            passwords[website] = []
        passwords[website].append({"username": encrypt_data(username, key), "password": encrypted_password})
        save_passwords(passwords)
        messagebox.showinfo("Success", "Password added successfully!")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")


def retrieve_password_ui(passwords, key):
    website = simpledialog.askstring("Retrieve Password", "Enter the website:")

    if website in passwords and isinstance(passwords[website], list):
        accounts = passwords[website]
        account_list = "\n".join([f"{i + 1}. {decrypt_data(account['username'], key)}" for i, account in enumerate(accounts)])
        selected = simpledialog.askinteger("Select Account", f"Accounts for {website}:\n{account_list}\nEnter the account number:")

        if selected and 1 <= selected <= len(accounts):
            username = decrypt_data(accounts[selected - 1]["username"], key)
            password = decrypt_data(accounts[selected - 1]["password"], key)

            # Create a new window to display the credentials and copy buttons
            retrieve_window = tk.Toplevel()
            retrieve_window.title(f"Credentials for {website}")

            # Username label and copy button
            username_label = tk.Label(retrieve_window, text=f"Username: {username}")
            username_label.pack(pady=5)
            username_copy_button = tk.Button(retrieve_window, text="Copy Username", command=lambda: pyperclip.copy(username))
            username_copy_button.pack(pady=5)

            # Password label (hidden) and copy button
            password_label = tk.Label(retrieve_window, text="Password: ******")  # Hide the password
            password_label.pack(pady=5)
            password_copy_button = tk.Button(retrieve_window, text="Copy Password", command=lambda: pyperclip.copy(password))
            password_copy_button.pack(pady=5)

            retrieve_window.mainloop()  # Start the new window loop

        else:
            messagebox.showwarning("Invalid Selection", "No valid account selected.")
    else:
        messagebox.showwarning("Not Found", "No entry found for the specified website.")


def list_passwords_ui(passwords):
    if passwords:
        websites = "\n".join(passwords.keys())
        messagebox.showinfo("Stored Websites", f"Websites:\n{websites}")
    else:
        messagebox.showinfo("No Passwords", "No passwords stored.")

def autofill_credentials(passwords, key):
    website = simpledialog.askstring("Autofill Login", "Enter the website:")
    if website in passwords and isinstance(passwords[website], list):
        accounts = passwords[website]
        account_list = "\n".join([f"{i + 1}. {decrypt_data(account['username'], key)}" for i, account in enumerate(accounts)])
        selected = simpledialog.askinteger("Select Account", f"Accounts for {website}:\n{account_list}\nEnter the account number:")

        if selected and 1 <= selected <= len(accounts):
            username = decrypt_data(accounts[selected - 1]["username"], key)
            password = decrypt_data(accounts[selected - 1]["password"], key)
            messagebox.showinfo("Autofill", f"Autofill Details:\nUsername: {username}\nPassword: {password}")
        else:
            messagebox.showwarning("Invalid Selection", "No valid account selected.")
    else:
        messagebox.showwarning("Not Found", "No entry found for the specified website.")

def main():
    authenticate_user()
    key = load_key()
    passwords = load_passwords()

    # Create the main application window
    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("300x250")

    # Create UI buttons
    add_button = tk.Button(root, text="Add Password", command=lambda: add_password_ui(passwords, key))
    add_button.pack(pady=10)

    retrieve_button = tk.Button(root, text="Retrieve Password", command=lambda: retrieve_password_ui(passwords, key))
    retrieve_button.pack(pady=10)

    list_button = tk.Button(root, text="List Websites", command=lambda: list_passwords_ui(passwords))
    list_button.pack(pady=10)

    autofill_button = tk.Button(root, text="Autofill Login", command=lambda: autofill_credentials(passwords, key))
    autofill_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

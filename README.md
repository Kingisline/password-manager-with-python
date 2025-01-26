# Password Manager

### Overview

This Python-based password manager provides a secure way to store, retrieve, and manage your passwords. It encrypts sensitive data using cryptography to ensure the confidentiality of stored passwords and authentication credentials. The application features a user-friendly graphical interface built with Tkinter.


### Features
- **Password Storage:** Allows users to store passwords securely with encryption.
- **Password Retrieval:** Retrieve saved credentials by entering a passkey.
- **Copy to Clipboard:** Copy the username and password to the clipboard with the click of a button.
- **Authentication:** Secures access to the password manager with a passkey that is encrypted.
- **Encryption:** Strong encryption is used to ensure the security of all stored data.


## Algorithms and Cryptography Used
The password manager uses Fernet symmetric encryption from the `cryptography` library to protect passwords and authentication keys. Here's an overview of the key cryptographic components:

### Fernet Symmetric Encryption
- **Fernet** is a symmetric encryption method, which means the same key is used to both encrypt and decrypt data.
- It uses **AES (Advanced Encryption Standard)** under the hood with a **256-bit key.**
- This ensures that passwords are securely encrypted before being saved, and only authorized users can decrypt them using the correct key.
### Key Generation and Storage
- The encryption key is generated using Fernet.generate_key(), and it's stored securely in a file named `key.key.`
- If the key file does not exist, a new key is generated and saved.

## Dependencies

```
pip install cryptography pyperclip
```

## Images

![Image](https://github.com/user-attachments/assets/8ee002b0-1999-4018-9048-fa13d8185d5c)

![Image](https://github.com/user-attachments/assets/5a5f1fb4-0170-4074-a999-88ece4023ad2)


## Social Media

[Instagram](https://www.instagram.com/ppl_call_me_as_bad_capton?igsh=NG1tYmpsYW5jcWY=)

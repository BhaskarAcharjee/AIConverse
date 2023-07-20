import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import hashlib
from AIConverse import create_main_application_window # Import the module containing create_main_application_window()

# Sample login credentials (for demonstration purposes only)
valid_credentials = {"user123": "482c811da5d5b4bc6d497ffa98491e38",  # hashed "password123"
                     "bhaskar": "656871241f3a30bd66b171dda2148cd8"}  # hashed "bhaskar123"

# Function to create the login window
def create_login_window():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x150")

    # Create the username label and entry field
    username_label = tk.Label(login_window, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    # Create the password label and entry field
    password_label = tk.Label(login_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    # Create the login button
    login_button = ttk.Button(login_window, text="Login", command=authenticate_user)
    login_button.pack(pady=10)

    # Create the register button
    register_button = ttk.Button(login_window, text="Register", command=register_user)
    register_button.pack(pady=5)

    # Run the login window loop
    login_window.mainloop()

# Function to perform user authentication
def authenticate_user():
    global logged_in_user

    username = username_entry.get()
    password = password_entry.get()

    if username in valid_credentials and validate_password(password, valid_credentials[username]):
        # If the credentials are correct, close the login window and set the logged_in_user
        logged_in_user = username
        login_window.destroy()
        create_main_application_window()
    else:
        # Show an error message if the credentials are incorrect
        messagebox.showerror("Login Error", "Invalid username or password")

# Function to validate the password using hashing
def validate_password(password, hashed_password):
    # Hash the entered password and compare it with the stored hashed password
    return hashlib.md5(password.encode()).hexdigest() == hashed_password

# Function to handle user registration
def register_user():
    global valid_credentials

    username = username_entry.get()
    password = password_entry.get()

    if username.strip() and password.strip():
        if username not in valid_credentials:
            # Hash the password and store it in the valid_credentials dictionary
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            valid_credentials[username] = hashed_password
            messagebox.showinfo("Registration Successful", "User registered successfully!")
        else:
            messagebox.showerror("Registration Error", "Username already exists.")
    else:
        messagebox.showerror("Registration Error", "Please enter a valid username and password.")

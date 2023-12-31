import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import hashlib
from AIConverse import create_main_application_window
from shared_data import valid_credentials, user_data, save_user_data_to_json

# Global variables for user registration
global login_window, registration_step, username_entry, password_entry, first_name_entry, last_name_entry

registration_step = 1


def create_login_window():
    global login_window
    login_window = tk.Tk()
    login_window.title("AIConverse Login")
    # login_window.geometry("500x300")
    login_window.state("zoomed")

    logo_label = tk.Label(login_window, text="🤖", font=("Arial", 60, "bold"))
    logo_label.pack(pady=30)

    welcome_label = tk.Label(login_window, text="Welcome to AIConverse", font=("Arial", 16))
    welcome_label.pack()

    login_label = tk.Label(login_window, text="Login with your AIConverse account", font=("Arial", 14))
    login_label.pack(pady=20)

    # "Sign In" and "Sign Up" buttons side by side in the center of the window
    login_frame = tk.Frame(login_window)
    login_frame.pack()

    login_button = ttk.Button(login_frame, text="Sign In", command=show_login_window)
    login_button.pack(side=tk.LEFT, padx=20)

    signup_button = ttk.Button(login_frame, text="Sign Up", command=show_signup_window)
    signup_button.pack(side=tk.RIGHT, padx=20)

    login_window.mainloop()


def show_login_window():
    global login_window
    login_window.destroy()
    create_login_form()


def create_login_form():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("AIConverse Login")
    # login_window.geometry("500x300")
    login_window.state("zoomed")

    logo_label = tk.Label(login_window, text="🤖", font=("Arial", 60, "bold"))
    logo_label.pack(pady=30)

    login_label = tk.Label(login_window, text="Login with your credentials", font=("Arial", 16))
    login_label.pack(pady=20)

    # Create the username label and entry field
    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=10)

    # Create the password label and entry field
    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=10)

    # Create the login button
    login_button = ttk.Button(login_window, text="Login", command=authenticate_user)
    login_button.pack(pady=20)

    # "Forgot password" and "Want to register" texts
    forgot_password_text = tk.Label(login_window, text="Forgot password", fg="blue", cursor="hand2")
    forgot_password_text.pack(pady=5)
    forgot_password_text.bind("<Button-1>", forgot_password)

    want_to_register_text = tk.Label(login_window, text="Want to register", fg="blue", cursor="hand2")
    want_to_register_text.pack(pady=5)
    want_to_register_text.bind("<Button-1>", go_to_signup)

    # Run the login window loop
    login_window.mainloop()


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


def show_signup_window():
    global login_window
    login_window.destroy()
    create_signup_window()


def create_signup_window():
    global login_window, registration_step, first_name_entry, last_name_entry, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("AIConverse Sign Up")
    # login_window.geometry("500x300")
    login_window.state("zoomed")

    logo_label = tk.Label(login_window, text="🤖", font=("Arial", 60, "bold"))
    logo_label.pack(pady=30)

    headline_label = tk.Label(login_window, text="Create Your Account", font=("Arial", 16))
    headline_label.pack(pady=20)

    if registration_step == 1:
        username_label = tk.Label(login_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(login_window)
        username_entry.pack(pady=10)

        password_label = tk.Label(login_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack(pady=10)

        continue_button = ttk.Button(login_window, text="Continue", command=step_two)
        continue_button.pack(pady=20)

        # "Already have an account? Log in" text
        login_text = tk.Label(login_window, text="Already have an account? Log in", fg="blue", cursor="hand2")
        login_text.pack(pady=5)
        login_text.bind("<Button-1>", go_to_login)


    elif registration_step == 2:
        first_name_label = tk.Label(login_window, text="First Name:")
        first_name_label.pack()
        first_name_entry = tk.Entry(login_window)
        first_name_entry.pack(pady=10)

        last_name_label = tk.Label(login_window, text="Last Name:")
        last_name_label.pack()
        last_name_entry = tk.Entry(login_window)
        last_name_entry.pack(pady=10)

        register_button = ttk.Button(login_window, text="Register", command=complete_registration)
        register_button.pack(pady=20)

        # "Already have an account? Log in" text
        login_text = tk.Label(login_window, text="Already have an account? Log in", fg="blue", cursor="hand2")
        login_text.pack(pady=5)
        login_text.bind("<Button-1>", go_to_login)

    login_window.mainloop()


def step_two():
    global registration_step, user_data

    username = username_entry.get()
    password = password_entry.get()

    if username.strip() and password.strip():
        user_data["username"] = username
        user_data["password"] = hashlib.md5(password.encode()).hexdigest()
        # Save chat contents to JSON after generating AI response
        save_user_data_to_json()

        registration_step = 2
        login_window.destroy()
        create_signup_window()
    else:
        messagebox.showerror("Registration Error", "Please enter a valid username and password.")


def complete_registration():
    global user_data, valid_credentials, registration_step

    first_name = first_name_entry.get()
    last_name = last_name_entry.get()

    if first_name.strip() and last_name.strip():
        user_data["first_name"] = first_name
        user_data["last_name"] = last_name

        # Store the user_data dictionary in the valid_credentials dictionary (for demonstration purposes only)
        valid_credentials[user_data["username"]] = user_data["password"]

        # Save chat contents to JSON after generating AI response
        save_user_data_to_json()


        messagebox.showinfo("Registration Successful", "User registered successfully!")
        registration_step = 1
        login_window.destroy()
        create_login_window()
    else:
        messagebox.showerror("Registration Error", "Please enter your first name and last name.")


# Function to navigate to the login window
def go_to_login(event):
    global login_window, registration_step
    login_window.destroy()
    registration_step = 1
    create_login_form()

# Function to navigate to the sign-up window
def go_to_signup(event):
    global login_window
    login_window.destroy()
    create_signup_window()

# Function to handle "Forgot password" behavior (you can implement this according to your requirements)
def forgot_password(event):
    messagebox.showinfo("Forgot Password", "This feature is not implemented yet!")


if __name__ == "__main__":
    create_login_window()
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from AIConverse import create_main_application_window
from login import create_login_window
from shared_data import logged_in_user

def main():
    # Start with the login window
    create_login_window()

    # Once the login is successful and the user is authenticated, proceed to the main application
    if logged_in_user is not None:
        create_main_application_window()

if __name__ == "__main__":
    main()
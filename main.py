from login import create_login_window
from AIConverse import create_main_application_window

logged_in_user = None

def main():
    # Start with the login window
    create_login_window()

    # Once the login is successful and the user is authenticated, proceed to the main application
    if logged_in_user is not None:
        create_main_application_window()

if __name__ == "__main__":
    main()
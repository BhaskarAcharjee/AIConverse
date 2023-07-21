# Dynamically store login credentials
valid_credentials = {
    # Sample login credentials (for demonstration purposes only)
    "user123": "482c811da5d5b4bc6d497ffa98491e38",  # hashed "password123"
    "bhaskar": "656871241f3a30bd66b171dda2148cd8",  # hashed "bhaskar123"
}

# save user data
user_data = {
    "first_name": "",
    "last_name": "",
    "username": "",
    "password": "", 
    "chat_contents": {}  # not implemented yet
}

# logged in user check
logged_in_user = None
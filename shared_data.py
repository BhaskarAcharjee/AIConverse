import json 

# Dynamically store login credentials
valid_credentials = {
    # Sample login credentials (for demonstration purposes only)
    "user123": "482c811da5d5b4bc6d497ffa98491e38",  # hashed "password123"
    "bhaskar": "656871241f3a30bd66b171dda2148cd8",  # hashed "bhaskar123"
    "b"      : "92eb5ffee6ae2fec3ad71c777531578f",  # hashed "b"
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

# Function to save user data to JSON
def save_user_data_to_json():
    with open("user_data.json", "w") as json_file:
        json.dump(user_data, json_file)

import json 

# Dynamically store login credentials
valid_credentials = {
    # Sample login credentials (for demonstration purposes only)
    "user123": "482c811da5d5b4bc6d497ffa98491e38",  # hashed "password123"
    "bhaskar": "656871241f3a30bd66b171dda2148cd8",  # hashed "bhaskar123"
    "b"      : "92eb5ffee6ae2fec3ad71c777531578f",  # hashed "b"
}

# logged in user check
logged_in_user = None

# save user data
user_data = {
    "first_name": "",
    "last_name": "",
    "username": "",
    "password": "", 
    "chat_contents": {},
    "theme_settings": {},
}

# Default color scheme values
color_schemes = {
    'Light': {
        'col_left_panel': "#F5F5F5",
        'col_right_panel': "#FFFFFF",
        'col_profile_frame': "#F0F0F0",
        'col_profile_image': "#F0F0F0",
        'col_profile_details': "#F0F0F0",
        'col_profile_name': "#F0F0F0",
        'col_profile_status': "#F0F0F0",
        'col_profile_options_button': "#F0F0F0",
        'col_options_frame': "#F0F0F0",
        'col_options_canvas': "#F0F0F0",
        'col_buttons_frame': "#F0F0F0",
        'col_chat_titles_frame': "#F0F0F0",
        'col_typing_indicator_label': "#F0F0F0",
        'col_chat_option_frame': "#F0F0F0",
        'col_chat_option_label': "#F0F0F0",
        'col_selected_chat_tab': "#D0D0D0",
    },
    'Dark': {
        'col_left_panel': "#1F1F1F",
        'col_right_panel': "#2A2A2A",
        'col_profile_frame': "#1F1F1F",
        'col_profile_image': "#363636",
        'col_profile_details': "#363636",
        'col_profile_name': "#FFFFFF",
        'col_profile_status': "#FFFFFF",
        'col_profile_options_button': "#363636",
        'col_options_frame': "#363636",
        'col_options_canvas': "#363636",
        'col_buttons_frame': "#363636",
        'col_chat_titles_frame': "#1F1F1F",
        'col_typing_indicator_label': "#363636",
        'col_chat_option_frame': "#363636",
        'col_chat_option_label': "#FFFFFF",
        'col_selected_chat_tab': "#D0D0D0",
    }
}

# Default layout and bubble style values
layout_styles = {
    'Compact': {
        'col_left_panel': '#F5F5F5',        
        'col_right_panel': '#FFFFFF',       
        'col_profile_frame': '#F0F0F0',     
        'col_typing_indicator_label': '#363636',  
        # Add more layout-specific styles here for Compact layout
    },
    'Comfortable': {
        'col_left_panel': '#EDEDED',        
        'col_right_panel': '#FAFAFA',       
        'col_profile_frame': '#E0E0E0',     
        'col_typing_indicator_label': '#E0E0E0',  
        # Add more layout-specific styles here for Comfortable layout
    }
}

bubble_styles = {
    'Standard': {
        # 'col_chat_bubble_user': '#C3E88D',      
        # 'col_chat_bubble_bot': '#80CBC4',       
        # 'col_chat_bubble_user_text': '#000000', 
        # 'col_chat_bubble_bot_text': '#000000',  
        'col_left_panel': '#EDEDED',        
        'col_right_panel': '#FAFAFA',       
        'col_profile_frame': '#E0E0E0',     
        'col_typing_indicator_label': '#E0E0E0',  
        # Add more bubble style-specific styles here for Standard style
    },
    'Modern': {
        # 'col_chat_bubble_user': '#BB86FC',      
        # 'col_chat_bubble_bot': '#03DAC6',       
        # 'col_chat_bubble_user_text': '#FFFFFF', 
        # 'col_chat_bubble_bot_text': '#000000', 
        'col_left_panel': '#EDEDED',        
        'col_right_panel': '#FAFAFA',       
        'col_profile_frame': '#E0E0E0',     
        'col_typing_indicator_label': '#E0E0E0',   
        # Add more bubble style-specific styles here for Modern style
    }
}

# Default settings values
default_settings = {
    'color_scheme': 'Light',
    'layout': 'Compact',
    'bubble_style': 'Standard'
}

# Extract the color values from the color scheme
def extract_color_values(color_scheme):
    col_left_panel = color_scheme['col_left_panel']
    col_right_panel = color_scheme['col_right_panel']
    col_profile_frame = color_scheme['col_profile_frame']
    col_profile_image = color_scheme['col_profile_image']
    col_profile_details = color_scheme['col_profile_details']
    col_profile_name = color_scheme['col_profile_name']
    col_profile_status = color_scheme['col_profile_status']
    col_profile_options_button = color_scheme['col_profile_options_button']
    col_options_frame = color_scheme['col_options_frame']
    col_options_canvas = color_scheme['col_options_canvas']
    col_buttons_frame = color_scheme['col_buttons_frame']
    col_chat_titles_frame = color_scheme['col_chat_titles_frame']
    col_typing_indicator_label = color_scheme['col_typing_indicator_label']
    col_chat_option_frame = color_scheme['col_chat_option_frame']
    col_chat_option_label = color_scheme['col_chat_option_label']
    col_selected_chat_tab = color_scheme['col_selected_chat_tab']

    return (
        col_left_panel, col_right_panel, col_profile_frame, col_profile_image, col_profile_details,
        col_profile_name, col_profile_status, col_profile_options_button, col_options_frame, col_options_canvas,
        col_buttons_frame, col_chat_titles_frame, col_typing_indicator_label, col_chat_option_frame,
        col_chat_option_label, col_selected_chat_tab
    )

# Function to save user data to JSON
def save_user_data_to_json():
    with open("user_data.json", "w") as json_file:
        json.dump(user_data, json_file)

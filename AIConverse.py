import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import tkinter.messagebox as messagebox
import time
from shared_data import user_data, save_user_data_to_json, logged_in_user, color_schemes, layout_styles, bubble_styles, default_settings, extract_color_values

# Dictionary to store chat tabs and their corresponding chat titles
chat_tabs = {}
# Global variable to keep track of the selected chat tab
selected_chat_tab = None

# Combine all settings into a single dictionary
app_settings = {**default_settings, **color_schemes['Light'], **layout_styles['Compact'], **bubble_styles['Standard']}

# Function to create the main application window
def create_main_application_window():

    # Create the main window
    global window
    window = tk.Tk()
    window.title("AIConverse")
    window.state("zoomed")

    # Get the default color scheme for the selected theme (Light or Dark)
    selected_color_scheme = user_data.get("color_scheme", "Light")
    color_scheme = color_schemes[selected_color_scheme]

    # Extract the color values from the color scheme
    (col_left_panel, col_right_panel, col_profile_frame, col_profile_image, col_profile_details, col_profile_name, col_profile_status, col_profile_options_button, col_options_frame, col_options_canvas, col_buttons_frame, col_chat_titles_frame, col_typing_indicator_label, col_chat_option_frame, col_chat_option_label, col_selected_chat_tab
    ) = extract_color_values(color_scheme)

    #>>>>>>>>>>>>>>>>>>>>>>>>>>> Basic Architecture <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Create the left panel for chat options
    left_panel = tk.Frame(window, width=200, bg=col_left_panel)

    # Create the right panel for the chat display
    right_panel = tk.Frame(window, bg=col_right_panel)

    # Position the left and right panels
    left_panel.pack(side="left", fill="y")
    right_panel.pack(side="right", fill="both", expand=True)

    # Create the tab manager for managing chat tabs
    tab_manager = ttk.Notebook(right_panel)

    # Position the tab manager in the right panel
    tab_manager.pack(fill="both", expand=True)

    #>>>>>>>>>>>>>>>>>>>>>>>>>>> Left Panel Chat Titles <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Create the profile section
    profile_frame = tk.Frame(left_panel, bg=col_profile_frame, pady=10)
    profile_frame.pack(fill="x", side="bottom")

    # Create the chat options section
    options_canvas = tk.Canvas(left_panel, bg=col_options_canvas, width=200)
    options_frame = tk.Frame(options_canvas, bg=col_options_frame)
    options_scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=options_canvas.yview)

    options_canvas.create_window((0, 0), window=options_frame, anchor="nw")
    options_canvas.configure(yscrollcommand=options_scrollbar.set)

    # Create the new chat button
    def start_new_chat():
        chat_content = []  # Initialize an empty list for chat content
        create_chat_tab(chat_content)

    # Create a frame to contain the buttons
    buttons_frame = tk.Frame(left_panel, bg=col_buttons_frame)
    buttons_frame.pack(fill="x", padx=10, pady=10)

    # Create the new chat button
    chat_button = ttk.Button(buttons_frame, text="New Chat", command=start_new_chat, width=28)
    chat_button.pack(side="left", padx=0, pady=10)

    # Function to toggle the sidebar visibility
    def toggle_sidebar():
        if left_panel.winfo_ismapped():
            left_panel.pack_forget()
            hide_sidebar_button.configure(text="▶")
        else:
            left_panel.pack(side="left", fill="y")
            hide_sidebar_button.configure(text="◀")

    # Create the hide sidebar button
    hide_sidebar_button = ttk.Button(buttons_frame, text="◀", command=toggle_sidebar, width=5)
    hide_sidebar_button.pack(side="left", padx=10, pady=10)

    # Create the chat titles section
    chat_titles_frame = tk.Frame(options_frame, bg=col_chat_titles_frame)
    chat_titles_frame.pack(fill="x")

    # Configure the chat titles frame to resize with the canvas
    def configure_chat_titles_frame(event):
        options_canvas.configure(scrollregion=options_canvas.bbox("all"))

    chat_titles_frame.bind("<Configure>", configure_chat_titles_frame)

    # Configure the options canvas to scroll the chat titles frame
    def configure_canvas(event):
        options_canvas.configure(scrollregion=options_canvas.bbox("all"))

    options_frame.bind("<Configure>", configure_canvas)

    options_canvas.pack(side="left", fill="both", expand=True)
    options_scrollbar.pack(side="right", fill="y")

    #>>>>>>>>>>>>>>>>>>>>>>>>>>> Chat Tab Section <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Function to create a new chat tab
    def create_chat_tab(chat_content, chat_title=None):
        global chat_tab  # Access the global variable to update it

        chat_tab = tk.Frame(tab_manager)  # Define chat_tab

        if not chat_title:
            # Generate a unique chat title based on the current date and time, including milliseconds
            title_timestamp_str = time.strftime("%d-%b-%y %H:%M", time.localtime())
            milliseconds = int((time.time() % 1) * 1000)  # Calculate milliseconds from the current time
            chat_title = f"Chat: {title_timestamp_str}:{milliseconds}"

        user_data["chat_contents"][chat_title] = chat_content   # Initialize empty chat content for the new chat tab

        # Save chat contents to JSON after generating AI response
        save_user_data_to_json()

        # Create a new chat tab
        chat_tab = tk.Frame(tab_manager)
        chat_tab.pack(fill="both", expand=True)

        # Create the chat window for the tab
        chat_window = tk.Text(chat_tab, width=80, height=30)
        chat_window.configure(state='disabled')
        chat_window.pack(fill="both", expand=True)

        # Create the user input box and send button for the tab
        user_input_frame = tk.Frame(chat_tab)
        user_input_frame.pack(side="top", pady=6)

        user_input = tk.Entry(user_input_frame, width=90, font=("Arial", 10), bd=5)
        user_input.pack(side="left", pady=6)

        # Create the send button
        send_button = ttk.Button(user_input_frame, text="Send", command=lambda: handle_user_input(chat_window, user_input, chat_title))
        send_button.pack(side="left")

        # Create the footer label
        footer_label = tk.Label(chat_tab, text="Free Research Preview. AIConverse may produce inaccurate information about people, places, or facts. AIConverse July 20 Version", bg="#F0F0F0", fg="#888888")
        footer_label.pack(side="top")

        # Create the typing indicator label for the tab
        typing_indicator_label = tk.Label(chat_tab, text="", bg=col_typing_indicator_label)
        typing_indicator_label.pack(side="bottom")


        # Function to handle user input for the tab
        def handle_user_input(chat_window, user_input, chat_title):
            user_message = user_input.get()
            user_input.delete(0, tk.END)

            # Check if the chat_title exists in the chat_contents dictionary
            if chat_title not in user_data["chat_contents"]:
                user_data["chat_contents"][chat_title] = []  # Create an empty list for the chat_title

            user_data["chat_contents"][chat_title].append(("You", user_message, time.time()))
            # Save chat contents to JSON after generating AI response
            save_user_data_to_json()

            display_chat_content(chat_window, user_data["chat_contents"][chat_title])
            generate_response(chat_window, user_message, typing_indicator_label, chat_title)  # Pass chat_title as a parameter

        # Add the chat tab to the tab manager
        tab_manager.add(chat_tab, text=chat_title)

        # Select the newly created chat tab and update the selected_chat_tab
        tab_manager.select(chat_tab)
        selected_chat_tab = chat_tab

        # Add the chat tab and its corresponding title and chat window to the chat_tabs dictionary
        chat_tabs[chat_tab] = {
            "title": chat_title,
            "window": chat_window
        }

        # Update the chat options section with the new chat tab
        create_chat_option(chat_title)

        # Highlight the selected chat option in the chat titles section
        for chat_option_frame in chat_titles_frame.winfo_children():
            if chat_option_frame.winfo_children()[0]['text'] == chat_title:
                chat_option_frame.configure(bg=col_selected_chat_tab)
            else:
                chat_option_frame.configure(bg=col_chat_option_frame)
        
        # Display the chat content for the new chat tab
        display_chat_content(chat_window, user_data["chat_contents"][chat_title])

    # Function to create a chat option in the chat options section
    def create_chat_option(chat_title):
        chat_option_frame = tk.Frame(chat_titles_frame, bg=col_chat_option_frame)
        chat_option_frame.pack(fill="x")

        # Function to switch to the corresponding chat tab
        def switch_chat(event):
            switch_chat_tab(chat_title)

        chat_option_label = tk.Label(chat_option_frame, text=chat_title, bg=col_chat_option_label, width=19, anchor="w")
        chat_option_label.pack(side="left", padx=5, pady=5)
        chat_option_label.bind("<Button-1>", switch_chat)

        # Function to rename the chat tab
        def rename_chat():
            chat_option_label_text = chat_option_label.cget("text")
            new_chat_title = simpledialog.askstring("Rename Chat", "Enter a new chat title:")
            if new_chat_title:
                # Update the chat title in the chat option label
                chat_option_label.configure(text=new_chat_title)

                # Get the old chat title
                old_chat_title = chat_option_label_text

                # Update the chat title in the tab manager
                tab_manager.tab(tab_manager.select(), text=new_chat_title)

                # Update the chat title in the user_data["chat_contents"] dictionary
                user_data["chat_contents"][new_chat_title] = user_data["chat_contents"].pop(old_chat_title)

                # Update the chat title in the chat_tabs dictionary
                chat_tabs[chat_tab]["title"] = new_chat_title

                # Save chat contents to JSON after renaming the chat
                save_user_data_to_json()

        rename_button = ttk.Button(chat_option_frame, text="🖊️", width=3, command=rename_chat)
        rename_button.pack(side="left")

        # Function to export the chat
        def export_chat():
            # Ask for the file name
            file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_name:
                with open(file_name, "w") as file:
                    for chat in user_data["chat_contents"][chat_title]:
                        user, message, timestamp = chat
                        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
                        file.write(f"{timestamp_str} - {user}: {message}\n")

        export_button = ttk.Button(chat_option_frame, text="💾", width=3, command=export_chat)
        export_button.pack(side="left")

        # Function to delete the chat tab and associated chat option
        def delete_chat():
            for tab in list(chat_tabs.keys()):
                if chat_tabs[tab]["title"] == chat_title:
                    tab_manager.forget(tab)
                    del chat_tabs[tab]
                    del user_data["chat_contents"][chat_title]
                    # Update chat contents in JSON after deleting chat
                    save_user_data_to_json()
                    chat_option_frame.destroy()
                    break

        delete_button = ttk.Button(chat_option_frame, text="🗑️", width=3, command=delete_chat)
        delete_button.pack(side="left")


    # Function to switch to a specific chat tab
    def switch_chat_tab(chat_title):
        global selected_chat_tab  # Access the global variable to update it

        for chat_tab, chat_info in chat_tabs.items():
            if chat_info["title"] == chat_title:
                tab_manager.select(chat_tab)
                selected_chat_tab = chat_tab  # Update the selected_chat_tab with the chat_tab object

                # Highlight the selected chat option
                for chat_option_frame in chat_titles_frame.winfo_children():
                    if chat_option_frame.winfo_children()[0]['text'] == chat_title:
                        chat_option_frame.configure(bg=col_selected_chat_tab)
                    else:
                        chat_option_frame.configure(bg=col_chat_option_frame)
                break

    # Set the first chat option as the selected option when the application starts
    if chat_titles_frame.winfo_children():
        chat_titles_frame.winfo_children()[0].configure(bg=col_selected_chat_tab)

    #>>>>>>>>>>>>>>>>>>>>>>>>>>> Chat Display Section <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Function to generate a response from the AI
    def generate_response(chat_window, user_message, typing_indicator_label, chat_title):
        # Show typing indicator
        typing_indicator_label.configure(text="AI is typing...")

        # TODO: Implement your AI response generation logic here
        # Replace the code below with your own AI response generation code
        response = "This is a sample response from the AI."

        # Hide typing indicator
        typing_indicator_label.configure(text="")

        user_data["chat_contents"][chat_title].append(("AI", response, time.time()))
        # Save chat contents to JSON after generating AI response
        save_user_data_to_json()

        display_chat_content(chat_window, user_data["chat_contents"][chat_title])

    # Function to display the chat content in the chat window
    def display_chat_content(chat_window, content):
        chat_window.configure(state='normal')
        chat_window.delete("1.0", tk.END)  # Clear previous content

        for chat in content:
            user, message, timestamp = chat
            timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

            # Create a chat bubble based on the user
            if user == "You":
                chat_window.insert(tk.END, f"{timestamp_str}\n", "timestamp")
                chat_window.insert(tk.END, f"You:\n", "user_label")
                chat_window.insert(tk.END, f"{message}\n\n", "user_bubble")
            else:
                chat_window.insert(tk.END, f"{timestamp_str}\n", "timestamp")
                chat_window.insert(tk.END, f"AI:\n", "ai_label")
                chat_window.insert(tk.END, f"{message}\n\n", "ai_bubble")

        chat_window.configure(state='disabled')
        chat_window.see(tk.END)  # Scroll to the bottom of the chat window

        # Configure tags for chat bubbles and labels
        chat_window.tag_configure("timestamp", font=("Arial", 8, "italic"), foreground="#999999")
        chat_window.tag_configure("user_label", font=("Arial", 10, "bold"), foreground="#0084FF")
        chat_window.tag_configure("user_bubble", background="#DCF8C6", foreground="#000000", font=("Arial", 12))
        chat_window.tag_configure("ai_label", font=("Arial", 10, "bold"), foreground="#FF6767")
        chat_window.tag_configure("ai_bubble", background="#E8E8E8", foreground="#000000", font=("Arial", 12))

    # Function to load chats after relogin
    def load_chats_after_relogin():
        # Create a copy of chat_contents to avoid modification during iteration
        chat_contents_copy = user_data["chat_contents"].copy()

        # Create a list to store the updated chat titles after re-login
        updated_chat_titles = []

        for chat_title, chat_content in chat_contents_copy.items():
            create_chat_tab(chat_content, chat_title)  # Create a new chat tab for each chat title with the original title
            updated_chat_titles.append(chat_title)  # Store the original chat title

        # Update the chat titles in the chat options section
        update_chat_titles_in_chat_options(updated_chat_titles)

    # Function to update chat titles in the chat options section after re-login
    def update_chat_titles_in_chat_options(updated_chat_titles):
        # Clear the existing chat options frames
        for chat_option_frame in chat_titles_frame.winfo_children():
            chat_option_frame.destroy()

        for chat_title in updated_chat_titles:
            create_chat_option(chat_title)


    #>>>>>>>>>>>>>>>>>>>>>>>>>>> Default Tab <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Create the default screen content
    default_tab = tk.Frame(tab_manager)
    default_tab.pack(fill="both", expand=True)

    # Create a container frame to hold the welcome label and Examples, Capabilities, and Limitations label frames
    content_frame = tk.Frame(default_tab, bg=col_right_panel)
    content_frame.pack(fill="both", expand=True)

    # Add the welcome label
    welcome_label = tk.Label(content_frame, text="Welcome to AIConverse!", font=("Arial", 18, "bold"), bg=col_right_panel)
    welcome_label.grid(row=0, column=0, columnspan=3, pady=150, sticky="ew")

    # Create LabelFrames for Examples, Capabilities, and Limitations
    examples_frame = tk.LabelFrame(content_frame, text="Examples", font=("Arial", 16, "bold"), bg=col_right_panel)
    examples_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    capabilities_frame = tk.LabelFrame(content_frame, text="Capabilities", font=("Arial", 16, "bold"), bg=col_right_panel)
    capabilities_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

    limitations_frame = tk.LabelFrame(content_frame, text="Limitations", font=("Arial", 16, "bold"), bg=col_right_panel)
    limitations_frame.grid(row=1, column=2, padx=20, pady=10, sticky="nsew")

    # Add the content to the Examples tab
    examples = [
        "Explain quantum computing in simple terms",
        "Got any creative ideas for a 10-year-old’s birthday?",
        "How do I make an HTTP request in Javascript?",
    ]

    for i, example in enumerate(examples, start=1):
        example_label = tk.Label(examples_frame, text=example, font=("Arial", 12), bg=col_right_panel, anchor="w")
        example_label.grid(row=i, column=0, padx=20, pady=5, sticky="w")

    # Add the content to the Capabilities tab
    capabilities = [
        "Tell me a joke",
        "Translate English to French",
        "Explain the concept of machine learning",
    ]

    for i, capability in enumerate(capabilities, start=1):
        capability_label = tk.Label(capabilities_frame, text=capability, font=("Arial", 12), bg=col_right_panel, anchor="w")
        capability_label.grid(row=i, column=0, padx=20, pady=5, sticky="w")

    # Add the content to the Limitations tab
    limitations = [
        "May produce inaccurate information",
        "Does not always ask clarifying questions",
        "Sensitive to input phrasing",
    ]

    for i, limitation in enumerate(limitations, start=1):
        limitation_label = tk.Label(limitations_frame, text=limitation, font=("Arial", 12), bg=col_right_panel, anchor="w")
        limitation_label.grid(row=i, column=0, padx=20, pady=5, sticky="w")

    #>>>>>>>>>>>>>>>>>>>>>>>>>>> Profile Section <<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # Create the profile image
    first_name_initial = user_data.get("first_name", "")[:1].upper()
    last_name_initial = user_data.get("last_name", "")[:1].upper()
    profile_image_text = f"{first_name_initial}{last_name_initial}" if first_name_initial and last_name_initial else "XD"

    profile_image = tk.Label(profile_frame, text=profile_image_text, bg=col_profile_image, font=("Arial", 24, "bold"), padx=10, pady=10)
    profile_image.pack(side="left")

    # Create the profile details
    profile_details = tk.Frame(profile_frame, bg=col_profile_details)
    profile_details.pack(side="left")

    # Assuming the user's first name and last name are stored in the user_data dictionary
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name", "")

    # Format the profile name text
    if first_name and last_name:
        profile_name_text = f"{first_name[:1].upper()}. {last_name[:7].capitalize() + '...' if len(last_name) > 7 else last_name.capitalize()}"
    else:
        profile_name_text = "User"

    # Create the profile name label
    profile_name = tk.Label(profile_details, text=profile_name_text, bg=col_profile_name, font=("Arial", 14, "bold"))
    profile_name.pack(anchor="w")

    profile_status = tk.Label(profile_details, text="Online", bg=col_profile_status, font=("Arial", 10))
    profile_status.pack(anchor="w")

    # Create the profile options button
    profile_options_button = tk.Label(profile_frame, text="•••", bg=col_profile_options_button, padx=10)
    profile_options_button.pack(side="right", padx=10)

    # Function to show the profile options popup sub-panel
    def show_profile_options():
        popup = tk.Toplevel(window)
        popup.title("Profile Options")
        popup.geometry("200x150")

        options_frame = tk.Frame(popup, bg=col_options_frame)
        options_frame.pack(fill="both", expand=True)

        options = ["Clear Conversations", "Help & FAQ", "Settings", "Logout"]

        for option in options:
            button = ttk.Button(options_frame, text=option, command=lambda o=option: handle_profile_option(o))
            button.pack(fill="x", padx=10, pady=5)

    # Function to handle the profile options
    def handle_profile_option(option):
        if option == "Clear Conversations":
            clear_conversations()
        elif option == "Help & FAQ":
            show_help_faq()
        elif option == "Settings":
            show_settings()
        elif option == "Logout":
            logout()

    # Bind the profile options button to show the profile options
    profile_options_button.bind("<Button-1>", lambda event: show_profile_options())

    # Function to clear conversations
    def clear_conversations():
        result = messagebox.askquestion("Clear Conversations", "Are you sure you want to clear all conversations?")
        if result == "yes":
            # Clear the conversation data
            user_data["chat_contents"].clear()

            # Close all chat tabs and update the chat_tabs dictionary
            for tab in list(chat_tabs.keys()):
                tab_manager.forget(tab)
                del chat_tabs[tab]

            # Clear all chat titles and associated chat options
            for chat_option_frame in chat_titles_frame.winfo_children():
                chat_option_frame.destroy()

            # Save chat contents to JSON after clearing conversations
            save_user_data_to_json()

            # Display a message indicating that conversations have been cleared
            messagebox.showinfo("Clear Conversations", "All conversations have been cleared.")

    # Function to show help and FAQ
    def show_help_faq():
        messagebox.showinfo("Help & FAQ", "This is the Help & FAQ section.")

    # Function to show settings
    def show_settings():
        # Create the settings window
        settings_window = tk.Toplevel(window)
        settings_window.title("Settings")
        settings_window.geometry("400x300")

        # Create the color scheme selection
        color_scheme_frame = tk.Frame(settings_window)
        color_scheme_frame.pack(pady=10)

        color_scheme_label = tk.Label(color_scheme_frame, text="Color Scheme:")
        color_scheme_label.pack(side="left")

        color_scheme_var = tk.StringVar()
        color_scheme_combobox = ttk.Combobox(color_scheme_frame, textvariable=color_scheme_var)
        color_scheme_combobox['values'] = ('Light', 'Dark')
        color_scheme_combobox.current(0)
        color_scheme_combobox.pack(side="left", padx=10)

        # Create the layout selection
        layout_frame = tk.Frame(settings_window)
        layout_frame.pack(pady=10)

        layout_label = tk.Label(layout_frame, text="Layout:")
        layout_label.pack(side="left")

        layout_var = tk.StringVar()
        layout_combobox = ttk.Combobox(layout_frame, textvariable=layout_var)
        layout_combobox['values'] = ('Compact', 'Comfortable')
        layout_combobox.current(0)
        layout_combobox.pack(side="left", padx=10)

        # Create the chat bubble style selection
        bubble_style_frame = tk.Frame(settings_window)
        bubble_style_frame.pack(pady=10)

        bubble_style_label = tk.Label(bubble_style_frame, text="Chat Bubble Style:")
        bubble_style_label.pack(side="left")

        bubble_style_var = tk.StringVar()
        bubble_style_combobox = ttk.Combobox(bubble_style_frame, textvariable=bubble_style_var)
        bubble_style_combobox['values'] = ('Standard', 'Modern')
        bubble_style_combobox.current(0)
        bubble_style_combobox.pack(side="left", padx=10)

        # Create the apply button
        def apply_settings():
            global app_settings

            selected_color_scheme = color_scheme_var.get()
            selected_layout = layout_var.get()
            selected_bubble_style = bubble_style_var.get()

            # Update the application settings based on the selected options
            app_settings = {
                **color_schemes[selected_color_scheme],
                **layout_styles[selected_layout],
                **bubble_styles[selected_bubble_style]
            }

            # Apply the selected settings (update the application's theme, layout, and chat bubble styles)
            update_gui_values()

            # Update the selected settings in the user_data dictionary
            user_data['theme_settings']['color_scheme'] = selected_color_scheme
            user_data['theme_settings']['layout'] = selected_layout
            user_data['theme_settings']['bubble_style'] = selected_bubble_style

            # Save the updated user_data to JSON
            save_user_data_to_json()

            # Show a success message
            messagebox.showinfo("Settings", "Settings applied successfully.")

            # Close the settings window
            settings_window.destroy()

        # Function to update the GUI elements with the new settings
        def update_gui_values():
            left_panel.configure(background=app_settings['col_left_panel'])
            right_panel.configure(background=app_settings['col_right_panel'])
            profile_frame.configure(background=app_settings['col_profile_frame'])
            profile_image.configure(background=app_settings['col_profile_image'])
            profile_details.configure(background=app_settings['col_profile_details'])
            profile_name.configure(background=app_settings['col_profile_name'])
            profile_status.configure(background=app_settings['col_profile_status'])
            profile_options_button.configure(background=app_settings['col_profile_options_button'])
            options_frame.configure(background=app_settings['col_options_frame'])
            options_canvas.configure(background=app_settings['col_options_canvas'])
            buttons_frame.configure(background=app_settings['col_buttons_frame'])
            chat_titles_frame.configure(background=app_settings['col_chat_titles_frame'])
            # typing_indicator_label.configure(background=app_settings['col_typing_indicator_label'])
            # option_frame.configure(background=app_settings['col_option_frame'])
            # chat_option_label.configure(background=app_settings['col_chat_option_label'])
            # Update other GUI elements with layout and bubble style settings as needed

        apply_button = ttk.Button(settings_window, text="Apply", command=apply_settings)
        apply_button.pack(pady=10)

    # Function to logout
    def logout():
        result = messagebox.askquestion("Logout", "Are you sure you want to logout?")
        if result == "yes":
            # Save chat contents to JSON after generating AI response
            save_user_data_to_json()

            # Perform logout actions
            window.destroy()

            # After closing the main window, you can call the main() function again to rerun the application
            import app
            app.main()


    # --------------end-------------

    # Load chats after relogin
    load_chats_after_relogin()

    # Run the main window loop
    window.mainloop()

if __name__ == "__main__":
    create_main_application_window()
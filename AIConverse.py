import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import time

# Create the main window
window = tk.Tk()
window.title("AIConverse")

# Create the left panel for chat options
left_panel = tk.Frame(window, width=200, bg="#F5F5F5")

# Create the profile section
profile_frame = tk.Frame(left_panel, bg="#F0F0F0", pady=10)
profile_frame.pack(fill="x", side="bottom")

# Create the profile image
profile_image = tk.Label(profile_frame, text="JD", bg="#F0F0F0", font=("Arial", 24, "bold"), padx=10, pady=10)
profile_image.pack(side="left")

# Create the profile details
profile_details = tk.Frame(profile_frame, bg="#F0F0F0")
profile_details.pack(side="left")

# Create the profile name and status
profile_name = tk.Label(profile_details, text="John Doe", bg="#F0F0F0", font=("Arial", 14, "bold"))
profile_name.pack(anchor="w")

profile_status = tk.Label(profile_details, text="Online", bg="#F0F0F0", font=("Arial", 10))
profile_status.pack(anchor="w")

# Create the profile options button
profile_options_button = tk.Label(profile_frame, text="•••", bg="#F0F0F0", padx=10)
profile_options_button.pack(side="right", padx=10)

# Function to show the profile options popup sub-panel
def show_profile_options():
    popup = tk.Toplevel(window)
    popup.title("Profile Options")
    popup.geometry("200x150")

    options_frame = tk.Frame(popup, bg="#F0F0F0")
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
        for chat_title in chat_contents:
            chat_contents[chat_title] = []

        # Update the chat windows
        for tab in tab_manager.tabs():
            chat_window = tab.winfo_children()[0]
            display_chat_content(chat_window, chat_contents[tab_manager.tab(tab, "text")])

# Function to show help and FAQ
def show_help_faq():
    messagebox.showinfo("Help & FAQ", "This is the Help & FAQ section.")

# Function to show settings
def show_settings():
    messagebox.showinfo("Settings", "This is the Settings section.")

# Function to logout
def logout():
    result = messagebox.askquestion("Logout", "Are you sure you want to logout?")
    if result == "yes":
        # Perform logout actions
        window.destroy()
        # Add your logout code here

# Create the chat options section
options_canvas = tk.Canvas(left_panel, bg="#F0F0F0", width=200)
options_frame = tk.Frame(options_canvas, bg="#F0F0F0")
options_scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=options_canvas.yview)

options_canvas.create_window((0, 0), window=options_frame, anchor="nw")
options_canvas.configure(yscrollcommand=options_scrollbar.set)

# Create the new chat button
def start_new_chat():
    create_chat_tab()

# chat_button = ttk.Button(options_frame, text="New Chat", command=start_new_chat)
# chat_button.pack(fill="x", padx=10, pady=10, expand=True)

# Create a frame to contain the buttons
buttons_frame = tk.Frame(options_frame, bg="#F0F0F0")
buttons_frame.pack(fill="x")

# Function to toggle the sidebar visibility
def toggle_sidebar():
    if left_panel.winfo_ismapped():
        left_panel.pack_forget()
        hide_sidebar_button.configure(text="▶")
    else:
        left_panel.pack(side="left", fill="y")
        hide_sidebar_button.configure(text="◀")

# Create the new chat button
chat_button = ttk.Button(buttons_frame, text="New Chat", command=start_new_chat,width=25)
chat_button.pack(side="left", padx=0, pady=10)

# Create the hide sidebar button
hide_sidebar_button = ttk.Button(buttons_frame, text="◀", command=toggle_sidebar,width=5)
hide_sidebar_button.pack(side="left", padx=0, pady=10)


# Create the chat titles section
chat_titles_frame = tk.Frame(options_frame, bg="#F0F0F0")
chat_titles_frame.pack(fill="x")

# Create the chat titles scrollbar
chat_titles_scrollbar = ttk.Scrollbar(chat_titles_frame, orient="vertical", command=options_canvas.yview)
chat_titles_scrollbar.pack(side="right", fill="y")

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

# Function to create a new chat tab
def create_chat_tab():
    chat_title = "Chat " + str(tab_manager.index("end"))
    chat_contents[chat_title] = []  # Initialize empty chat content for the new chat tab

    # Create a new chat tab
    chat_tab = tk.Frame(tab_manager)
    chat_tab.pack(fill="both", expand=True)

    # Create the chat window for the tab
    chat_window = tk.Text(chat_tab, width=80, height=30)
    chat_window.configure(state='disabled')
    chat_window.pack(fill="both", expand=True)

    # Create the user input box and send button for the tab
    user_input_frame = tk.Frame(chat_tab)
    user_input_frame.pack(side="bottom", pady=10)

    user_input = tk.Entry(user_input_frame, width=60)
    user_input.pack(side="left")

    send_button = ttk.Button(user_input_frame, text="Send", command

=lambda: handle_user_input(chat_window, user_input))
    send_button.pack(side="left")

    # Create the typing indicator label for the tab
    typing_indicator_label = tk.Label(chat_tab, text="", bg="#F0F0F0")
    typing_indicator_label.pack(side="bottom")

    # Function to handle user input for the tab
    def handle_user_input(chat_window, user_input):
        user_message = user_input.get()
        user_input.delete(0, tk.END)
        chat_contents[chat_title].append(("You", user_message, time.time()))
        display_chat_content(chat_window, chat_contents[chat_title])
        generate_response(chat_window, user_message, typing_indicator_label)

    # Add the chat tab to the tab manager
    tab_manager.add(chat_tab, text=chat_title)

    # Set the newly created chat tab as the active tab
    tab_manager.select(chat_tab)

    # Update the chat options section with the new chat tab
    create_chat_option(chat_title)

# Function to create a chat option in the chat options section
def create_chat_option(chat_title):
    chat_option_frame = tk.Frame(chat_titles_frame, bg="#F0F0F0")
    chat_option_frame.pack(fill="x")

    # Function to switch to the corresponding chat tab
    def switch_chat(event):
        switch_chat_tab(chat_title)

    chat_option_label = tk.Label(chat_option_frame, text=chat_title, bg="#F0F0F0", width=20, anchor="w")
    chat_option_label.pack(side="left", pady=5)
    chat_option_label.bind("<Button-1>", switch_chat)

    # Function to delete the chat tab and associated chat option
    def delete_chat():
        for tab in tab_manager.tabs():
            if tab_manager.tab(tab, "text") == chat_title:
                tab_manager.forget(tab)
                del chat_contents[chat_title]
                chat_option_frame.destroy()
                break

    delete_button = ttk.Button(chat_option_frame, text="X", width=3, command=delete_chat)
    delete_button.pack(side="left", padx=(0, 5))

# Function to switch to a specific chat tab
def switch_chat_tab(chat_title):
    for tab in tab_manager.tabs():
        if tab_manager.tab(tab, "text") == chat_title:
            tab_manager.select(tab)
            break

# Function to display the chat content in the chat window
def display_chat_content(chat_window, content):
    chat_window.configure(state='normal')
    chat_window.delete("1.0", tk.END)  # Clear previous content
    for chat in content:
        user, message, timestamp = chat
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        chat_window.insert(tk.END, f"{user} ({timestamp_str}):\n{message}\n\n")
    chat_window.configure(state='disabled')
    chat_window.see(tk.END)  # Scroll to the bottom of the chat window

# Function to generate a response from the AI
def generate_response(chat_window, user_message, typing_indicator_label):
    # Show typing indicator
    typing_indicator_label.configure(text="AI is typing...")

    # TODO: Implement your AI response generation logic here
    # Replace the code below with your own AI response generation code
    response = "This is a sample response from the AI."

    # Hide typing indicator
    typing_indicator_label.configure(text="")

    chat_contents[tab_manager.tab(tab_manager.select(), "text")].append(("AI", response, time.time()))
    display_chat_content(chat_window, chat_contents[tab_manager.tab(tab_manager.select(), "text")])

# Create the right panel for the chat display
right_panel = tk.Frame(window, bg="#FFFFFF")

# Create the tab manager for managing chat tabs
tab_manager = ttk.Notebook(right_panel)

# Create a dictionary to store chat contents for each tab
chat_contents = {}

# Position the tab manager in the right panel
tab_manager.pack(fill="both", expand=True)

# Create the default screen content
default_tab = tk.Frame(tab_manager)
default_tab.pack(fill="both", expand=True)

default_label = tk.Label(default_tab, text="Welcome to AIConverse!", font=("Arial", 16, "bold"), pady=100)
default_label.pack()

tab_manager.add(default_tab, text="Home")

# Create the Examples tab
examples_tab = tk.Frame(tab_manager)
examples_tab.pack(fill="both", expand=True)

examples_label = tk.Label(examples_tab, text="Examples", font=("Arial", 16, "bold"), pady=100)
examples_label.pack()

# Dummy data for examples
examples = [
    "Explain quantum computing in simple terms",
    "Got any creative ideas for a 10 year old’s birthday?",
    "How do I make an HTTP request in Javascript?",
]

capabilities = [
    "Tell me a joke",
    "Translate English to French",
    "Explain the concept of machine learning",
]

limitations = [
    "May produce inaccurate information",
    "Does not always ask clarifying questions",
    "Sensitive to input phrasing",
]

for example in examples:
    example_label = tk.Label(examples_tab, text=example, font=("Arial", 12), pady=10)
    example_label.pack()

tab_manager.add(examples_tab, text="Examples")

# Create the Capabilities tab
capabilities_tab = tk.Frame(tab_manager)
capabilities_tab.pack(fill="both", expand=True)

capabilities_label = tk.Label(capabilities_tab, text="Capabilities", font=("Arial", 16, "bold"), pady=100)
capabilities_label.pack()

for capability in capabilities:
    capability_label = tk.Label(capabilities_tab, text=capability, font=("Arial", 12), pady=10)
    capability_label.pack()

tab_manager.add(capabilities_tab, text="Capabilities")

# Create the Limitations tab
limitations_tab = tk.Frame(tab_manager)
limitations_tab.pack(fill="both", expand=True)

limitations_label = tk.Label(limitations_tab, text="Limitations", font=("Arial", 16, "bold"), pady=100)
limitations_label.pack()

for limitation in limitations:
    limitation_label = tk.Label(limitations_tab, text=limitation, font=("Arial", 12), pady=10)
    limitation_label.pack()

tab_manager.add(limitations_tab, text="Limitations")

# Position the left and right panels
left_panel.pack(side="left", fill="y")
right_panel.pack(side="right", fill="both", expand=True)

# Run the main window loop
window.mainloop()
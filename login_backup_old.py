import tkinter as tk
from tkinter import messagebox
import sys, os
import frontend
import base64

# Define the correct password
initial_counter = "cGFzc3dvcmRAMTIz"
secondary_counter = base64.b64decode(initial_counter)
final_counter = secondary_counter.decode('utf-8')


max_attempts = 3  # Maximum number of allowed attempts

# Initialize attempt counter
attempt_counter = 0


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def center_window(window, width, height):
    # Get the dimensions of the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to position the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the dimensions of the window and position it
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to check the password
def check_password():
    global attempt_counter
    entered_password = password_entry.get()
    if entered_password == final_counter:
        messagebox.showinfo("Access Granted", "Correct password. Application starting...")
        password_window.destroy()  # Close the password window
        frontend.main()  # Call the function to start the main application
    else:
        attempt_counter += 1
        if attempt_counter >= max_attempts:
            messagebox.showerror("Access Denied", "Too many incorrect attempts. Exiting...")
            password_window.destroy()  # Close the password window
            sys.exit()  # Exit the application
        else:
            messagebox.showerror("Access Denied", f"Incorrect password. {max_attempts - attempt_counter} attempt(s) remaining.")
            password_entry.delete(0, tk.END)  # Clear the password field

# Password prompt window
password_window = tk.Tk()
password_window.title("Password Protection")

width = 400
height = 150

center_window(password_window, width, height)

# password_window.geometry("400x150")

password_window.iconbitmap(resource_path('ies_ico1.ico'))

password_label = tk.Label(password_window, text="Enter Password:", font=("Helvetica", 12))
password_label.pack(pady=10)

# Password entry field
password_entry = tk.Entry(password_window, show="*", font=("Helvetica", 12))
password_entry.pack(pady=5)

# Submit button
submit_button = tk.Button(password_window, text="Submit", command=check_password)
submit_button.pack(pady=10)

password_window.mainloop()
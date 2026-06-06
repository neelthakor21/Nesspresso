import tkinter as tk
from tkinter import messagebox
import src.frontend as frontend
import sys, os
import base64
import uuid
import time


try:
    # Define allowed MAC addresses
    allowed_macs = [
        "40-C2-BA-67-E9-BC",
        "00:50:56:C0:00:08"
    ]

    initial_counter = "MDExMTAwMDAwMTEwMDAwMTAxMTEwMDExMDExMTAwMTEwMTExMDExMTAxMTAxMTExMDExMTAwMTAwMTEwMDEwMDAxMDAwMDAwMDAxMTAwMDEwMDExMDAxMDAwMTEwMDEx"
    secondary_counter = base64.b64decode(initial_counter)
    recon = byte_data = bytes(int(secondary_counter[i:i+8], 2) for i in range(0, len(secondary_counter), 8))
    final_counter = recon.decode('utf-8')

    max_attempts = 3  # Maximum number of allowed attempts
    attempt_counter = 0  # Initialize attempt counter

    # Function to get the MAC address of the machine
    def get_mac_address():
        return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 8 * 6, 8)][::-1])

    # Function to check machine authorization
    def is_machine_authorized():
        mac = get_mac_address()
        mac = mac.upper()
        print(mac)
        return mac in allowed_macs

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

    # Function to display a temporary "Checking Authorization" window
    def show_checking_authorization():
        auth_window = tk.Toplevel()
        auth_window.title("Authorization Check")
        auth_window.geometry("300x100")
        auth_window.resizable(False, False)

        # Center the window
        center_window(auth_window, 300, 100)

        # Display a label showing the "Checking authorization" message
        label = tk.Label(auth_window, text="Checking authorization...", font=("Helvetica", 12))
        label.pack(expand=True, pady=20)

        # Disable window interactions (no close button, etc.)
        auth_window.overrideredirect(True)  

        # Update the window to display it and then sleep for a short time to simulate the check
        auth_window.update()
        time.sleep(2)  # Simulate time for checking authorization

        # Return the authorization window, so it can be closed later
        return auth_window

    # Function to check the password
    def check_password():
        global attempt_counter
        entered_password = password_entry.get()
        if entered_password == final_counter:
            messagebox.showinfo("Access Granted", "Correct password. Application starting...")
            password_window.destroy()
            root.destroy()  # Close the password window
            frontend.main()  # Call the function to start the main application
        else:
            attempt_counter += 1
            if attempt_counter >= max_attempts:
                messagebox.showerror("Access Denied", "Too many incorrect attempts. Exiting...")
                password_window.destroy()  # Close the password window
                root.destroy()
                sys.exit()  # Exit the application
            else:
                messagebox.showerror("Access Denied", f"Incorrect password. {max_attempts - attempt_counter} attempt(s) remaining.")
                password_entry.delete(0, tk.END)  # Clear the password field

    # Main Application Entry
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.iconbitmap(resource_path(os.path.join("docs", "logo", "logo.ico")))

    # Show the "Checking authorization" window
    auth_check_window = show_checking_authorization()

    # Check machine authorization
    if is_machine_authorized():
        # Close the "Checking authorization" window
        auth_check_window.destroy()

        # Show a message box indicating that the machine is authorized
        messagebox.showinfo("Machine Authorized", "This machine is authorized to run the application.")
        
        # Password prompt window
        password_window = tk.Toplevel(root)
        password_window.title("Password Protection")

        width = 400
        height = 150
        center_window(password_window, width, height)

        password_window.iconbitmap(resource_path(os.path.join("docs", "logo", "logo.ico")))

        password_label = tk.Label(password_window, text="Enter Password:", font=("Helvetica", 12))
        password_label.pack(pady=10)

        # Password entry field
        password_entry = tk.Entry(password_window, show="*", font=("Helvetica", 12))
        password_entry.pack(pady=5)

        # Submit button
        submit_button = tk.Button(password_window, text="Submit", command=check_password)
        submit_button.pack(pady=10)

        password_window.mainloop()

    else:
        # Close the "Checking authorization" window
        auth_check_window.destroy()

        # Show a message box indicating that the machine is not authorized
        messagebox.showerror("Unauthorized Machine", "This machine is not authorized to run the application. Exiting...")
        sys.exit()
except Exception as e:
    print("ERROR:", e)

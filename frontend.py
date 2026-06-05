import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import backend
import sys
import os
import threading
import time, random


def update_progress_bar(progress_var, progress_bar):
    """Update the progress bar with random values."""
    while progress_var.get() < 99:
        if progress_simulation_done:
            break
        progress_var.set(min(progress_var.get() + random.randint(1, 2), 85))
        progress_bar.update()
        time.sleep(random.uniform(8.5, 15.5))  # Random delay for progress update

def start_progress_bar(progress_bar, progress_var):
    """Reset and start the progress bar."""
    progress_var.set(0)  # Reset progress bar to 0%
    progress_bar.update()

# Function to handle file upload
def upload_file(result_label, progress_var, progress_bar):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")])

    if file_path:
        messagebox.showinfo("File Uploaded", "File uploaded successfully!")

        start_progress_bar(progress_bar, progress_var)

        def backend_task():
            global progress_simulation_done
            progress_simulation_done = False

            result_label.config(text="Processing your File, Please wait..........")

            # Start progress simulation
            threading.Thread(target=lambda: update_progress_bar(progress_var, progress_bar)).start()

            processed_file_path = backend.main(file_path)  # Call the backend function with file path

             # Update progress and result label based on backend result
            progress_simulation_done = True
            progress_var.set(100)  # Set progress to 100%
            progress_bar.update()

            if processed_file_path:
                result_label.config(text=f"Converted report is located at: {processed_file_path}")
            else:
                result_label.config(text="Files is failed to processed. Please try again!")

        # Start the backend task in a thread
        threading.Thread(target=backend_task).start()
    else:
        messagebox.showwarning("No File Selected", "Please select a file.")

# Function to adjust the wraplength of the label text
def adjust_wraplength(event, content_frame, title_label, info_label, result_label, footer_label):
    frame_width = content_frame.winfo_width()
    title_label.config(wraplength=frame_width - 20)  # Adding padding to avoid edge clipping
    info_label.config(wraplength=frame_width - 20)  # Adding padding to avoid edge clipping
    result_label.config(wraplength=frame_width - 20)  # Adding padding to avoid edge clipping
    footer_label.config(wraplength=frame_width - 20)  # Adding padding to avoid edge clipping

# Define the resource_path function to get the correct path for bundled files
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def center_window(root, width=800, height=600):
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position for the window to be centered
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    # Set the geometry of the window
    root.geometry(f'{width}x{height}+{x}+{y}')
    

# Function to change button color on hover
def on_enter(e, upload_button):
    upload_button.config(bg='#2980b9', fg='white')

def on_leave(e, upload_button):
    upload_button.config(bg='#3498db', fg='white')

# Create the main window

def main():
    root = tk.Tk()
    root.title("Nesspresso")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x=0
    y=0
    root.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

    root.configure(bg="#2c3e50")

    # # Center the window on the screen
    # root.eval('tk::PlaceWindow.center')

    # Center the window with specified dimensions
    center_window(root, width=1300, height=700)

    # Set custom favicon
    root.iconbitmap(resource_path('logo.ico'))  # Replace with your favicon path
    # Load the background image using Pillow
    background_image_path = resource_path('bgi1.jpg')
    background_image = Image.open(background_image_path)  # Replace with your image path

    # Convert the image to a PhotoImage object
    background_photo = ImageTk.PhotoImage(background_image)

    # Set the background image with `place` to make it responsive
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)

    # logo1 = resource_path('app_logo.png')
    # logo = Image.open(logo1)  # Replace with the path to your logo
    # logo = logo.resize((100, 100), Image.Resampling.LANCZOS)  # Optional: Resize the logo
    # logo_image = ImageTk.PhotoImage(logo)

    # logo_label = tk.Label(root, image=logo_image)
    # logo_label.place(x=15, y=15, anchor='nw')

    logo1 = resource_path('app_logo.png')

    logo = Image.open(logo1).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    logo = logo.resize((100, 100), Image.Resampling.LANCZOS)

    logo_image = ImageTk.PhotoImage(logo)

    logo_label = tk.Label(
        root,
        image=logo_image,
        borderwidth=0,
        highlightthickness=0,
        bg=root.cget("bg")
    )

    logo_label.image = logo_image
    logo_label.place(x=15, y=15, anchor='nw')

    # Create a frame to hold content within the window
    # content_frame = tk.Frame(root, bg='#34495e')
    content_frame = tk.Frame(root, bg='#042d4d')

    content_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.55, relheight=0.65)  # Smaller size

    # Use grid layout for better responsiveness
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(1, weight=0)
    content_frame.grid_rowconfigure(2, weight=1)
    content_frame.grid_rowconfigure(3, weight=0)
    content_frame.grid_rowconfigure(4, weight=0)
    content_frame.grid_rowconfigure(5, weight=1)

    # Add a title label to the content frame
    title_label = ttk.Label(content_frame, text="Upload your Nessus Report", font=("Helvetica", 20, "bold"), background='#042d4d', foreground='white')
    title_label.grid(row=0, column=0, pady=20, sticky="n")

    # Create an upload button with hover effect
    upload_button = tk.Button(content_frame, text="Choose File", command=lambda :upload_file(result_label, progress_var, progress_bar), font=("Helvetica", 14), bg='#3498db', fg='white', activebackground='#2980b9', activeforeground='white', bd=0, relief='flat', padx=10, pady=10)
    upload_button.grid(row=1, column=0, pady=10, sticky="n")

    # Bind hover effect
    upload_button.bind("<Enter>", lambda event: on_enter(event, upload_button))
    upload_button.bind("<Leave>", lambda event: on_leave(event, upload_button))

    # Add an info label for supported formats
    info_label = ttk.Label(content_frame, text="Supported formats: .csv, .xlsx, .xls", background='#042d4d', foreground='white', font=("Helvetica", 15, "italic"))
    info_label.grid(row=2, column=0, pady=15, sticky="n")

    # Progress bar setup
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(content_frame, orient="horizontal", length=300, mode="determinate", variable=progress_var)
    progress_bar.grid(row=3, column=0, pady=10, sticky="n")

    # Flag to control progress simulation
    progress_simulation_done = False

    # Label to display the converted file location
    result_label = tk.Label(content_frame, text="", font=("Helvetica", 12, "bold"), background='#042d4d', foreground='white')
    result_label.grid(row=4, column=0, pady=20, sticky="s")

    # Add a footer label to the content frame
    footer_label = ttk.Label(content_frame, text="Copyright © 2026 Nesspresso. All rights reserved. | Developed by Neel Thakor.", font=("Helvetica", 10, "italic"), background='#042d4d', foreground='white')
    footer_label.grid(row=5, column=0, pady=10, sticky="s")

    # Bind the window resize event to adjust the wrap length
    content_frame.bind("<Configure>", lambda event: adjust_wraplength(event, content_frame, title_label, info_label, result_label, footer_label))

    root.minsize(800, 600)
    # Run the application
    root.mainloop()



############################################################################################################################################################
#pyinstaller --onefile --windowed --name "Nesspresso" --icon=ico1.ico --add-data "ico1.ico;." --add-data "bgi1.jpg;." --add-data "backend.py;." frontend.py#
############################################################################################################################################################

# pyinstaller --onefile --name "Nesspresso" --icon=ies_ico1.ico --add-data "ies_ico1.ico;." --add-data "bgi1.jpg;." --add-data "backend.py;." --add-data "frontend.py;." --add-data "Banner.jpg;." login.py

# pyinstaller --onefile --name "Nesspresso" --icon=logo.ico --add-data "logo.ico;." --add-data "bgi1.jpg;." --add-data "backend.py;." --add-data "frontend.py;." --add-data "logo.png;." login.py

# python -m PyInstaller --clean --windowed --onefile --name "Nesspresso" --icon=logo.ico --add-data "logo.ico;." --add-data "logo.png;." --add-data "bgi1.jpg;." login.py
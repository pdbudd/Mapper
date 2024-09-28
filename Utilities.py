import tkinter as tk
from tkinter import filedialog
import os

def choose_file():
    """Opens a file selection dialog and returns the relative path to the selected file."""
    # Hide the root window
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog
    file_path = filedialog.askopenfilename()
    
    if file_path:
        # Convert absolute path to relative path
        relative_path = os.path.relpath(file_path)
        return relative_path
    else:
        raise ValueError("No file selected")
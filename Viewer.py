import tkinter as tk
from tkinter import filedialog, Checkbutton, IntVar
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Map import load_MapObject, MapObject
import os

class MapEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Editor")

        # Create a frame to hold the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.TOP,fill=tk.X, pady=5)

        # Buttons inside the frame
        self.load_button = tk.Button(button_frame, text="Load Map", command=self.load_map)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.new_button = tk.Button(button_frame, text="New Map", command=self.new_map)
        self.new_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(button_frame, text="Save Map", command=self.save_map)
        self.save_button.pack(side=tk.LEFT, padx=10)

        # Placeholder for image and layers
        self.MapObject: MapObject = None

        # Matplotlib Figure to display the map
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()
        
        # Layer checkboxes
        self.layer_checkboxes = {}

        # Frame for controls (checkboxes, buttons)
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.LEFT)

        # Button to add layer
        self.add_layer_button = tk.Button(self.control_frame, text="Add Layer", command=self.add_layer)
        self.add_layer_button.pack(side=tk.LEFT, pady=5)
        
        self.root.bind("<Configure>", self.on_resize)

    def load_map(self):
        # Open file dialog to choose image
        file_path = filedialog.askopenfilename()
        if file_path:
            self.MapObject = load_MapObject(file_path)

            # Display the image using Matplotlib
            self.update_display()
            
    def on_resize(self):
        """Resize the Matplotlib figure based on width and height in pixels."""
        figure_width = self.MapObject.resolution[1] / 1000  # Convert pixels to inches (DPI = 100)
        figure_height = self.MapObject.resolution[0] / 1000  # Adjust for the DPI
        self.fig.set_size_inches(figure_width, figure_height)

    def new_map(self):
        file_path = filedialog.askopenfilename()
        name = get_input_text("Name of map")
        if file_path:
            self.MapObject = MapObject(image_path=file_path, map_object_name=name)
            self.update_display()
    
    def save_map(self):
        if not os.path.exists("saved_maps\\"):
            os.mkdir("saved_maps\\")
        self.MapObject.save_MapObject(f"saved_maps\\{self.MapObject.name}")
        
    def update_display(self):
        # Clear the previous image
        self.ax.clear()

        # Display the map
        if self.MapObject.map is not None:
            self.ax.imshow(self.MapObject.map)
            self.ax.axis('off')

        # Overlay layers
        for layer_name, layer in self.MapObject.layers.items():
            if self.layer_checkboxes[layer_name].get():
                self.ax.imshow(layer.data, alpha=0.5, cmap='jet')  # Change `cmap` for different visualizations

        # Redraw the canvas
        self.canvas.draw()

    def add_layer(self):
        # Add a random numpy array as a new layer for demonstration purposes
        if self.MapObject.map is not None:
            layer_name = get_input_text("Layer name")

            # Add the layer to the layers dictionary
            self.MapObject.add_layer(layer_name)

            # Create a checkbox for the new layer
            var = IntVar()
            cb = Checkbutton(self.control_frame, text=layer_name, variable=var, command=self.update_display)
            cb.pack(anchor=tk.W)
            self.layer_checkboxes[layer_name] = var

            # Refresh display
            self.update_display()
            
def get_input_text(prompt):
    """Opens a simple text input box and returns the entered string."""
    def on_submit(event=None):  # Accept `event` parameter for binding
        nonlocal user_input
        user_input = entry.get()
        root.quit()  # Close the window after submission

    root = tk.Tk()
    root.title(prompt)
    
    # Input field
    entry = tk.Entry(root, width=40)
    entry.pack(padx=20, pady=10)
    
    # OK button
    button = tk.Button(root, text="OK", command=on_submit)
    button.pack(pady=10)

    # Bind the Enter key to the on_submit function
    root.bind("<Return>", on_submit)
    
    user_input = None
    root.mainloop()  # Start the GUI loop
    root.destroy()  # Destroy the window after use
    return user_input
            
root = tk.Tk()
app = MapEditorApp(root)
root.mainloop()
import tkinter as tk
from tkinter import filedialog, Checkbutton, IntVar
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Map import load_MapObject, MapObject
import os

class Loader:
    def __init__(self, parent):
        self.root = parent.root
        self.parent = parent
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.TOP, fill=tk.X)
        
        self.new_button = tk.Button(self.frame, text='New map', command=self.new_map)
        self.new_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.load_button = tk.Button(self.frame, text='Load map', command=self.load_map)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)
        
    def load_map(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.parent.MapObject = load_MapObject(file_path)
            self.parent.update_display()
    
    def new_map(self):
        self.parent.MapObject = MapObject()
        self.parent.update_display()
        
class Canvas:
    def __init__(self, parent):
        self.root = parent.root
        self.Parent = parent
        self.frame = tk.Frame(self.root)
        self.map = parent.MapObject.map

class Layer_menu:
    def __init__(self, parent):
        self.root = parent.root
        self.parent = parent
        self.frame = tk.Frame(self.root)

        

class MapEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Editor")

        self.resize_job = None

        self.loader = Loader(self)

        # Placeholder for image and layers
        self.MapObject: MapObject = None

        # Matplotlib Figure to display the map
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Layer checkboxes
        self.layer_checkboxes = {}

        # Frame for controls (checkboxes, buttons)
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.LEFT)

        # Button to add layer
        self.add_layer_button = tk.Button(self.control_frame, text="Add Layer", command=self.add_layer)
        self.add_layer_button.pack(side=tk.LEFT, pady=5)
        
        self.x = 0.0
        self.y = 0.0
        
        # Bind the window resize event to dynamically update the figure size
        self.root.bind("<Configure>", self.on_resize)
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_resize(self, event):
        """Handle window resizing, but throttle how often we actually update."""
        if self.resize_job is not None:
            # Cancel the previously scheduled resize job if it exists
            self.root.after_cancel(self.resize_job)

        # Schedule a new resize job to run after 100 milliseconds
        self.resize_job = self.root.after(500, self.do_resize, event.width, event.height)

    def do_resize(self, width, height):
        """Perform the actual resizing of the Matplotlib figure."""
        # Get the DPI of the figure (default DPI is usually 100)
        dpi = self.fig.get_dpi()

        # Calculate figure size in inches based on the window size in pixels
        figure_width = width / dpi
        figure_height = height / dpi

        # Set the new figure size
        self.fig.set_size_inches(figure_width, figure_height)

        # Redraw the canvas to apply the new size
        self.canvas.draw()
    
    def save_map(self):
        save_path = os.path.join("saved_maps", self.MapObject.name)
        if not os.path.exists("saved_maps"):
            os.mkdir("saved_maps")
        self.MapObject.save_MapObject(save_path)

    def update_display(self):
        # Clear the previous image
        self.ax.clear()

        # Display the map
        if self.MapObject and self.MapObject.map is not None:
            self.ax.imshow(self.MapObject.map)
            self.ax.axis('off')

        # Overlay layers
        for layer_name, layer in self.MapObject.layers.items():
            if self.layer_checkboxes.get(layer_name) and self.layer_checkboxes[layer_name].get():
                self.ax.imshow(layer.data, alpha=0.5, cmap='jet')  # Change `cmap` for different visualizations

        # Redraw the canvas
        self.canvas.draw()

    def add_layer(self):
        # Add a new layer to the MapObject
        if self.MapObject and self.MapObject.map is not None:
            layer_name = get_input_text("Layer name")
            self.MapObject.add_layer(layer_name)  # Assume `add_layer()` is defined in MapObject

            # Create a checkbox for the new layer
            var = IntVar()
            cb = Checkbutton(self.control_frame, text=layer_name, variable=var, command=self.update_display)
            cb.pack(anchor=tk.W)
            self.layer_checkboxes[layer_name] = var

            # Refresh display
            self.update_display()

    def on_click(self, event):
        if event.xdata and event.ydata:
            pass

    def on_motion(self, event):
        """Callback for mouse motion inside the Matplotlib canvas."""
        if event.xdata and event.ydata:
            self.x = event.xdata
            self.y = event.ydata
            
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

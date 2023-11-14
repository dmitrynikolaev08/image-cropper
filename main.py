import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def crop_object(image_path, output_path, background_margin=0):
    # Open the image
    image = Image.open(image_path)
    # Convert the image to grayscale for easier processing
    gray_image = image.convert('L')
    # Convert the image to a NumPy array
    img_array = np.array(gray_image)
    # Find non-zero (or non-white) pixels
    non_zero_pixels = np.where(img_array < 255)  # Adjust this threshold if needed
    # Calculate the bounding box
    y_coordinates, x_coordinates = non_zero_pixels
    top, bottom = np.min(y_coordinates), np.max(y_coordinates)
    left, right = np.min(x_coordinates), np.max(x_coordinates)
    # Expand the bounding box to include background
    top = max(0, top - background_margin)
    left = max(0, left - background_margin)
    bottom = min(img_array.shape[0], bottom + background_margin)
    right = min(img_array.shape[1], right + background_margin)
    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))
    # Convert 'RGBA' to 'RGB' if necessary
    if cropped_image.mode == 'RGBA':
        cropped_image = cropped_image.convert('RGB')
    cropped_image.save(output_path)

    cropped_image.save(output_path)


def select_image():
    # Select an image file
    path = filedialog.askopenfilename()
    if len(path) > 0:
        global img_path
        img_path = path
        # Load and display the image
        image = Image.open(path)
        image = image.resize((250, 250), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        panel.configure(image=photo)
        panel.image = photo


def process_image():
    if img_path:
        output_path = "output.jpg"  # You can modify this path
        crop_object(img_path, output_path)
        result_label.config(text=f"Processed image saved as {output_path}")


# Initialize Tkinter window
window = tk.Tk()
window.title("Background Remover")

# Initialize path variable
img_path = ""

# Create a panel to display the image
panel = tk.Label(window)
panel.pack(padx=10, pady=10)

# Create buttons
btn_select = tk.Button(window, text="Select Image", command=select_image)
btn_select.pack(side="left", padx=10, pady=10)

btn_process = tk.Button(window, text="Crop Image", command=process_image)
btn_process.pack(side="right", padx=10, pady=10)

# Label to display result message
result_label = tk.Label(window, text="")
result_label.pack(padx=10, pady=10)

window.mainloop()

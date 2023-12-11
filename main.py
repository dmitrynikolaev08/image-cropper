import sys

import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


def crop_object(image_path, output_path, padding=25, background_color=(255, 255, 255)):
    # Open the image
    image = Image.open(image_path)

    # If the image has an alpha channel, we assume it is the mask
    if image.mode == 'RGBA':
        # Extract the alpha channel as a mask
        mask = image.split()[3]
        # Convert the mask to a NumPy array
        mask_array = np.array(mask)
        # Find where the mask is not transparent
        object_pixels = np.where(mask_array > 0)
    else:
        # Convert the image to grayscale for easier processing
        gray_image = image.convert('L')
        # Convert the image to a NumPy array
        img_array = np.array(gray_image)
        # Find non-zero (or non-white) pixels
        object_pixels = np.where(img_array < 255)  # Adjust this threshold if needed

    # Calculate the bounding box
    y_coordinates, x_coordinates = object_pixels
    top, bottom = np.min(y_coordinates), np.max(y_coordinates)
    left, right = np.min(x_coordinates), np.max(x_coordinates)

    # Calculate the size of the new image with padding
    new_width = (right - left) + (2 * padding)
    new_height = (bottom - top) + (2 * padding)

    # Create a new image with the desired background color and size
    bg_image = Image.new('RGB', (new_width, new_height), background_color)

    # Paste the original image onto the new background, centered
    bg_image.paste(image, (padding - left, padding - top), mask if image.mode == 'RGBA' else None)

    # Save the image with the new background
    bg_image.save(output_path)


def select_images():
    # Select multiple image files
    paths = filedialog.askopenfilenames()
    global img_paths
    img_paths = list(paths)
    if img_paths:
        # Load and display the first selected image
        image = Image.open(img_paths[0])
        image = image.resize((250, 250), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        panel.configure(image=photo)
        panel.image = photo


def process_images():
    if img_paths:
        for img_path in img_paths:
            file_name = os.path.basename(img_path)
            # Directory of the executable
            dir_name = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(
                os.path.realpath(__file__))
            output_path = os.path.join(dir_name, file_name)
            crop_object(img_path, output_path)
        result_label.config(text=f"Processed {len(img_paths)} images.")


# Initialize Tkinter window
window = tk.Tk()
window.title("Background Remover")

# Create a panel to display the image
panel = tk.Label(window)
panel.pack(padx=10, pady=10)

# Create buttons
btn_select = tk.Button(window, text="Select Images", command=select_images)
btn_process = tk.Button(window, text="Crop Images", command=process_images)
btn_select.pack(side="left", padx=10, pady=10)
btn_process.pack(side="right", padx=10, pady=10)

# Label to display result message
result_label = tk.Label(window, text="")
result_label.pack(padx=10, pady=10)

window.mainloop()

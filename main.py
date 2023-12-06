import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


def crop_object(image_path, output_path, background_margin=25, background_color=(255, 255, 255)):
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

    bg_image = Image.new('RGB', cropped_image.size, background_color)

    if cropped_image.mode == 'RGBA':
        # Extract the alpha channel as a mask
        mask = cropped_image.split()[3]
        bg_image.paste(cropped_image.convert('RGB'), (0, 0), mask)
    else:
        bg_image.paste(cropped_image, (0, 0))

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
            output_path = file_name
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

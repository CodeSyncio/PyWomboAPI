
# this code is just an example, I coded this in a very ugly way just to demonstrate how it can be used.
import os
import asyncio
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PyWomboAPI import WomboAPI

def download_image(url, foldername, name):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    with open(os.path.join(foldername, name), 'wb') as file:
        file.write(requests.get(url).content)

async def generate_images(style_id, prompt, image_amount):
    API = WomboAPI()
    API.setup()
    foldername = prompt.replace(' ', '_')

    async for result in API.create_image_batch(style_id, prompt, image_amount):
        image_url = result.url
        download_image(image_url, foldername, f"image_{result.id}.jpg")
        print(f"Downloaded image: {image_url}")

    messagebox.showinfo("Success", "Done generating and downloading images")

def on_generate_button_click(style_id, prompt, image_amount):
    try:
        image_amount = int(image_amount)
        if image_amount <= 0:
            raise ValueError("Really? Please generate at least one image.")
        asyncio.run(generate_images(style_id, prompt, image_amount))
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def fetch_styles():
    API = WomboAPI()
    API.setup()
    styles = API.fetch_styles()
    return styles

def create_gui():
    root = tk.Tk()
    root.title("Image Generator")

    styles = fetch_styles()

    prompt_label = tk.Label(root, text="Enter Prompt:")
    prompt_label.pack(pady=5)
    prompt_entry = tk.Entry(root, width=50)
    prompt_entry.pack(pady=5)

    style_label = tk.Label(root, text="Select Style:")
    style_label.pack(pady=5)
    style_combobox = ttk.Combobox(root, state='readonly')
    style_combobox['values'] = [f"{style[0]}: {style[1]}" for style in styles]
    style_combobox.pack(pady=5)
    style_combobox.current(0)

    amount_label = tk.Label(root, text="Number of Images:")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(root, width=5)
    amount_entry.pack(pady=5)

    generate_button = tk.Button(
        root, text="Generate Images",
        command=lambda: on_generate_button_click(
            int(style_combobox.get().split(':')[0]),  # selected style ID
            prompt_entry.get().strip(),                # prompt
            amount_entry.get().strip()                 # number of images
        )
    )
    generate_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

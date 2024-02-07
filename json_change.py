import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json

current_data = {}  # To keep track of the currently loaded data

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON file: {e}")
        return None

def save_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save JSON file: {e}")

def display_json(data):
    text_area.delete(1.0, tk.END)  # Clear existing content
    for site in data['sites']:
        text_area.insert(tk.END, f"Title: {site['title']}\nURL: {site['url']}\nDetails: {site['details']}\n\n")

def add_entry():
    if not (entry_url.get() and entry_details.get() and entry_title.get()):  # Ensure all fields are filled
        messagebox.showwarning("Warning", "Please fill all fields before adding an entry.")
        return  # Skip adding the entry if any field is empty
    
    new_site = {
        "url": entry_url.get(),
        "details": entry_details.get(),
        "title": entry_title.get()
    }
    current_data["sites"].append(new_site)
    display_json(current_data)
    save_json(entry_path.get(), current_data)
    entry_url.delete(0, tk.END)
    entry_details.delete(0, tk.END)
    entry_title.delete(0, tk.END)

def remove_entry():
    title_to_remove = entry_title.get()
    current_data["sites"] = [site for site in current_data["sites"] if site["title"] != title_to_remove]
    display_json(current_data)
    save_json(entry_path.get(), current_data)
    entry_title.delete(0, tk.END)

def browse_file():
    filename = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
    if filename:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, filename)
        global current_data
        current_data = load_json(filename)
        if current_data:
            display_json(current_data)

root = tk.Tk()
root.title("JSON File Viewer and Editor")

tk.Label(root, text="File Path:").pack()
entry_path = tk.Entry(root, width=50)
entry_path.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

tk.Label(root, text="URL:").pack()
entry_url = tk.Entry(root, width=50)
entry_url.pack()

tk.Label(root, text="Details:").pack()
entry_details = tk.Entry(root, width=50)
entry_details.pack()

tk.Label(root, text="Title (for add/remove):").pack()
entry_title = tk.Entry(root, width=50)
entry_title.pack()

add_button = tk.Button(root, text="Add Entry", command=add_entry)
add_button.pack()

remove_button = tk.Button(root, text="Remove Entry", command=remove_entry)
remove_button.pack()

text_area = scrolledtext.ScrolledText(root, width=60, height=15)
text_area.pack()

root.mainloop()

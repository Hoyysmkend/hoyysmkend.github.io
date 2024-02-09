import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import json

current_data = {}  # To keep track of the currently loaded data
current_key = ""  # Track the selected key

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

def display_json(data, key):
    text_area.delete(1.0, tk.END)  # Clear existing content
    if key in data:
        for site in data[key]:
            text_area.insert(tk.END, f"Title: {site['title']}\nURL: {site['url']}\nDetails: {site['details']}\n\n")

def add_entry():
    if not (entry_url.get() and entry_details.get() and entry_title.get() and current_key):  # Ensure all fields are filled
        messagebox.showwarning("Warning", "Please fill all fields before adding an entry.")
        return  # Skip adding the entry if any field is empty
    
    new_site = {
        "url": entry_url.get(),
        "details": entry_details.get(),
        "title": entry_title.get()
    }
    if current_key in current_data:
        current_data[current_key].append(new_site)
        display_json(current_data, current_key)
        save_json(entry_path.get(), current_data)
        entry_url.delete(0, tk.END)
        entry_details.delete(0, tk.END)
        entry_title.delete(0, tk.END)

def remove_entry():
    if current_key:
        title_to_remove = entry_title.get()
        current_data[current_key] = [site for site in current_data[current_key] if site["title"] != title_to_remove]
        display_json(current_data, current_key)
        save_json(entry_path.get(), current_data)
        entry_title.delete(0, tk.END)

def browse_file():
    filename = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
    if filename:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, filename)
        global current_data
        current_data = load_json(filename)
        update_key_options()

def update_key_options():
    key_combo['values'] = list(current_data.keys()) if current_data else []
    key_combo.current(0)  # Set the first item as the current item
    on_key_selection_changed()

def on_key_selection_changed(event=None):
    global current_key
    current_key = key_combo.get()
    if current_data:
        display_json(current_data, current_key)

root = tk.Tk()
root.title("JSON File Viewer and Editor")

frame = tk.Frame(root)
frame.pack(fill=tk.X)

tk.Label(frame, text="File Path:").pack(side=tk.LEFT)
entry_path = tk.Entry(frame, width=50)
entry_path.pack(side=tk.LEFT)

browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.pack(side=tk.LEFT)

tk.Label(root, text="Key:").pack()
key_combo = ttk.Combobox(root, width=47, postcommand=update_key_options)
key_combo.pack()
key_combo.bind('<<ComboboxSelected>>', on_key_selection_changed)

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

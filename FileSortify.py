import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import FileOrganizer
from FileOrganizer import FilesExtension

try:
    from ttkthemes import ThemedTk
    root = ThemedTk(theme="arc") 
except ImportError:
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")

root.title("FileSortify")
root.configure(background="#f5f5f5")

# Apply custom styling for a modern look.
style = ttk.Style(root)
style.configure("TFrame", background="#f5f5f5")
style.configure("TLabel", background="#f5f5f5", foreground="#333333", font=("Helvetica", 12))
style.configure("Title.TLabel", font=("Helvetica", 18, "bold"), foreground="#2c3e50")
style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6)
style.configure("TEntry", padding=5)

current_directory = None
selected_files = []

frame = ttk.Frame(root, padding="15")
frame.grid(row=0, column=0, sticky="NSEW")

# Title label with modern styling.
title_label = ttk.Label(frame, text="FileSortify - Organize Your Files", style="Title.TLabel")
title_label.grid(row=0, column=0, columnspan=3, pady=15)

def select_directory():
    global current_directory, selected_files
    current_directory = filedialog.askdirectory()
    selected_files = []  # Clear selected files if a directory is chosen
    if current_directory:
        directory_label.config(text=f"Selected Directory: {current_directory}")
    else:
        directory_label.config(text="No directory selected.")

def select_files():
    global selected_files, current_directory
    selected_files = filedialog.askopenfilenames(title="Select Files")
    current_directory = None  # Clear directory if individual files are chosen
    if selected_files:
        directory_label.config(text=f"{len(selected_files)} files selected.")
    else:
        directory_label.config(text="No files selected.")

def add_category():
    ext = extension_entry.get().strip()
    folder = folder_entry.get().strip()
    if ext and folder:
        FilesExtension[ext] = folder
        update_category_list()
        extension_entry.delete(0, tk.END)
        folder_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Input Error", "Please enter both extension and folder name.")

def remove_category():
    ext = extension_entry.get().strip()
    if ext in FilesExtension:
        del FilesExtension[ext]
        update_category_list()
        extension_entry.delete(0, tk.END)
        folder_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Category Not Found", f"The extension '{ext}' was not found in the mappings.")

def edit_category():
    try:
        selection = category_list.curselection()
        if not selection:
            raise Exception("No category selected.")
        selected_text = category_list.get(selection[0])
        ext, folder = selected_text.split(": ")
        extension_entry.delete(0, tk.END)
        extension_entry.insert(0, ext)
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)
    except Exception as e:
        messagebox.showerror("Selection Error", str(e))

def update_category():
    ext = extension_entry.get().strip()
    folder = folder_entry.get().strip()
    if ext and folder:
        FilesExtension[ext] = folder
        update_category_list()
        extension_entry.delete(0, tk.END)
        folder_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Input Error", "Please enter both extension and folder name.")

def update_category_list():
    category_list.delete(0, tk.END)
    for ext, folder in FilesExtension.items():
        category_list.insert(tk.END, f"{ext}: {folder}")

def organize_files():
    if current_directory:
        result = FileOrganizer.organize_files(current_directory, FilesExtension)
        messagebox.showinfo("Operation Complete", result)
    elif selected_files:
        result = FileOrganizer.organize_selected_files(selected_files, FilesExtension)
        messagebox.showinfo("Operation Complete", result)
    else:
        messagebox.showerror("Selection Error", "Please select a directory or files first.")

directory_label = ttk.Label(frame, text="No directory or files selected", font=("Helvetica", 10))
directory_label.grid(row=1, column=0, columnspan=3, pady=10)

# Buttons for selecting directory and files.
select_dir_button = ttk.Button(frame, text="Select Directory", command=select_directory)
select_dir_button.grid(row=2, column=0, pady=10, padx=5)

select_files_button = ttk.Button(frame, text="Select Files", command=select_files)
select_files_button.grid(row=2, column=1, pady=10, padx=5)


extension_entry = ttk.Entry(frame, width=20)
extension_entry.grid(row=3, column=0, pady=10, padx=5)
folder_entry = ttk.Entry(frame, width=20)
folder_entry.grid(row=3, column=1, pady=10, padx=5)


add_button = ttk.Button(frame, text="Add Category", command=add_category)
add_button.grid(row=4, column=0, pady=10, padx=5)
remove_button = ttk.Button(frame, text="Remove Category", command=remove_category)
remove_button.grid(row=4, column=1, pady=10, padx=5)
edit_button = ttk.Button(frame, text="Edit Category", command=edit_category)
edit_button.grid(row=5, column=0, pady=10, padx=5)
update_button = ttk.Button(frame, text="Update Category", command=update_category)
update_button.grid(row=5, column=1, pady=10, padx=5)


organize_button = ttk.Button(frame, text="Organize Files", command=organize_files)
organize_button.grid(row=6, column=0, pady=15, padx=5, columnspan=2)


category_list = tk.Listbox(frame, height=10, width=50, font=("Helvetica", 10))
category_list.grid(row=7, column=0, columnspan=3, pady=10)

update_category_list()

root.mainloop()

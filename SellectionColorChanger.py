import tkinter as tk
from tkinter import ttk
import winreg

def validate_color(color):
    if len(color) % 3 != 0:
        return False
    for i in range(0, len(color), 3):
        value = color[i:i+3]
        try:
            value = int(value)
            if value < 0 or value > 255:
                return False
        except ValueError:
            return False
    return True

def save_changes():
    hilight_color = hilight_entry.get().replace(" ", "")
    if len(hilight_color) != 9 or not hilight_color.isdigit():
        show_status_message("Invalid color format", "red")
        return
    hottracking_color = hottracking_entry.get().replace(" ", "")
    if len(hottracking_color) != 9 or not hottracking_color.isdigit():
        show_status_message("Invalid color format", "red")
        return
    if not validate_color(hilight_color) or not validate_color(hottracking_color):
        show_status_message("Invalid color format", "red")
        return
    hilight_color = ' '.join([hilight_color[i:i+3] for i in range(0, len(hilight_color), 3)])
    hottracking_color = ' '.join([hottracking_color[i:i+3] for i in range(0, len(hottracking_color), 3)])
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\Colors', 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, "Hilight", 0, winreg.REG_SZ, hilight_color)
            winreg.SetValueEx(reg_key, "HotTrackingColor", 0, winreg.REG_SZ, hottracking_color)
        show_status_message("Changes saved", "green")
    except OSError:
        show_status_message("Failed to save changes", "red")

def reset_changes():
    show_status_message("Reset successful", "green")
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Control Panel\\Colors', 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, "Hilight", 0, winreg.REG_SZ, "0 120 215")
            winreg.SetValueEx(reg_key, "HotTrackingColor", 0, winreg.REG_SZ, "0 102 204")
    except OSError:
        show_status_message("Failed to reset changes", "red")

def show_status_message(message, color):
    status_label.config(text=message, foreground=color)

def hide_status_message():
    status_label.config(text="")

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"+{x}+{y}")

def validate_input(entry):
    entry_value = entry.get().replace(" ", "")[:9]
    entry.delete(0, tk.END)
    entry.insert(0, entry_value)

def on_entry_key(event):
    if event.keysym != "BackSpace" and not event.char.isdigit():
        return 'break'

def apply_changes():
    save_changes()

window = tk.Tk()
window.title("Selection Color Changer")
window.geometry("400x200")
window.resizable(False, False)
window.iconbitmap(default=r"C:\Users\sasch\Desktop\SellectionColorChanger\16x16.ico")

frame = ttk.Frame(window)
frame.pack(pady=20, padx=20)

hilight_label = ttk.Label(frame, text="Highlight (RGB):", foreground="black", font="Roboto 10")
hilight_label.pack()
hilight_entry = ttk.Entry(frame, font="Roboto 10")
hilight_entry.pack()
hilight_entry.bind("<KeyRelease>", lambda e: (validate_input(hilight_entry)))
hilight_entry.bind("<Key>", on_entry_key)

hottracking_label = ttk.Label(frame, text="HotTrackingColor (RGB):", foreground="black", font="Roboto 10")

hottracking_label.pack()
hottracking_entry = ttk.Entry(frame, font="Roboto 10")
hottracking_entry.pack()
hottracking_entry.bind("<KeyRelease>", lambda e: (validate_input(hottracking_entry)))
hottracking_entry.bind("<Key>", on_entry_key)

style = ttk.Style()
style.configure("TButton", relief="raised", foreground="black", background="#54545c")

frame_buttons = ttk.Frame(window)
frame_buttons.pack()

button_reset = ttk.Button(frame_buttons, text="Reset", command=reset_changes, style="TButton")
button_reset.pack(side=tk.LEFT)

button_apply = ttk.Button(frame_buttons, text="Apply", command=apply_changes, style="TButton")
button_apply.pack(side=tk.LEFT)

copy_text = "© allegryyy"
copy_label = ttk.Label(window, text=copy_text, font="Roboto 10")
copy_label.pack(side=tk.LEFT, padx=10, pady=(10, 10))

status_label = ttk.Label(window, text="", justify=tk.CENTER, font="Roboto 10 bold")
status_label.pack()
status_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

center_window(window)
window.mainloop()

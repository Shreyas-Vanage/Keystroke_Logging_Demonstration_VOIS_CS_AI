import tkinter as tk
from tkinter import messagebox

# Function to capture keystrokes
def log_key(event):
    key = event.keysym
    if len(key) == 1:
        log_box.insert(tk.END, key)
    elif key == "space":
        log_box.insert(tk.END, " ")
    else:
        log_box.insert(tk.END, f"[{key}]")

# Clear logs
def clear_logs():
    log_box.delete("1.0", tk.END)

# Exit safely
def exit_app():
    if messagebox.askyesno("Exit", "Do you want to exit the demo?"):
        root.destroy()

# Main window
root = tk.Tk()
root.title("Keystroke Logging Demonstration (Educational)")
root.geometry("600x400")

# Warning label
warning = tk.Label(
    root,
    text="Educational Demo Only – Captures Keystrokes ONLY Inside This App",
    fg="red",
    font=("Arial", 10, "bold")
)
warning.pack(pady=5)

# Input field
input_label = tk.Label(root, text="Type Here:")
input_label.pack()

input_box = tk.Entry(root, width=80)
input_box.pack(pady=5)
input_box.bind("<Key>", log_key)

# Log display
log_label = tk.Label(root, text="Captured Keystrokes:")
log_label.pack()

log_box = tk.Text(root, height=10, width=80)
log_box.pack(pady=5)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

clear_btn = tk.Button(btn_frame, text="Clear Logs", command=clear_logs)
clear_btn.grid(row=0, column=0, padx=10)

exit_btn = tk.Button(btn_frame, text="Exit", command=exit_app)
exit_btn.grid(row=0, column=1, padx=10)

root.mainloop()

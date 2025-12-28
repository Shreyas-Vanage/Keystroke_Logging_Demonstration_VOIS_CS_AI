import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import json
from datetime import datetime
import threading

# Global variables
listener = None
keystrokes = []
logging_active = False
start_time = ""

# Start logging
def start_logging():
    global listener, logging_active, start_time

    if logging_active:
        return

    keystrokes.clear()
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging_active = True
    status_label.config(text="Status: Logging Started", fg="green")

    def on_press(key):
        if not logging_active:
            return
        try:
            keystrokes.append({
                "key": key.char,
                "time": datetime.now().strftime("%H:%M:%S")
            })
        except AttributeError:
            keystrokes.append({
                "key": str(key),
                "time": datetime.now().strftime("%H:%M:%S")
            })

    def run_listener():
        global listener
        with keyboard.Listener(on_press=on_press) as l:
            listener = l
            l.join()

    threading.Thread(target=run_listener, daemon=True).start()

# Stop logging
def stop_logging():
    global logging_active, listener

    if not logging_active:
        return

    logging_active = False
    status_label.config(text="Status: Logging Stopped", fg="red")

    if listener:
        listener.stop()

    save_logs()
    messagebox.showinfo(
        "Logging Stopped",
        "Keystrokes saved to keystrokes.txt and keystrokes.json"
    )

# Save logs to TXT and JSON
def save_logs():
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Text file
    with open("keystrokes.txt", "w") as txt:
        txt.write(f"Session Start: {start_time}\n")
        txt.write(f"Session End: {end_time}\n")
        txt.write("Keystrokes:\n")
        for k in keystrokes:
            txt.write(f"{k['time']} : {k['key']}\n")

    # JSON file
    with open("keystrokes.json", "w") as js:
        json.dump({
            "session_start": start_time,
            "session_end": end_time,
            "keystrokes": keystrokes
        }, js, indent=4)

# Exit safely
def exit_app():
    if logging_active:
        stop_logging()
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Keystroke Logging Demonstration (Cyber Security)")
root.geometry("520x350")
root.resizable(False, False)

# Title
title = tk.Label(
    root,
    text="Keystroke Logging Demonstration",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

# Disclaimer
disclaimer = tk.Label(
    root,
    text=(
        "Educational Purpose Only\n"
        "Keystrokes are logged ONLY after clicking START\n"
        "User consent is mandatory"
    ),
    fg="red",
    font=("Arial", 10),
    justify="center"
)
disclaimer.pack(pady=5)

# Status
status_label = tk.Label(
    root,
    text="Status: Not Logging",
    fg="blue",
    font=("Arial", 12, "bold")
)
status_label.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

start_btn = tk.Button(
    btn_frame,
    text="Start Logging",
    width=15,
    bg="green",
    fg="white",
    command=start_logging
)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(
    btn_frame,
    text="Stop Logging",
    width=15,
    bg="red",
    fg="white",
    command=stop_logging
)
stop_btn.grid(row=0, column=1, padx=10)

exit_btn = tk.Button(
    root,
    text="Exit",
    width=10,
    command=exit_app
)
exit_btn.pack(pady=10)

root.mainloop()

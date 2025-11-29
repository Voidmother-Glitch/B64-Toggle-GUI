#made by Voidmother-Glitch
#Encode and Decode text to and from Base64 with utf-8 handling
#Results read-only mode was removed as it consistently broke the dark mode styling in testing.
#(Nothing quite like getting flashbanged by a bright white box in your dark mode app!)

import base64
import tkinter as tk
from tkinter import messagebox, ttk

#Colors
DARK_BG = "#1e1e1e"
DARK_ENTRY_BG = "#2d2d2d"
LIGHT_TEXT = "#ffffff"
ACCENT_COLOR = "#007acc"
HOVER_COLOR = "#005f99"
BUTTON_TEXT = "#ffffff"

def is_base64(s):
    """Validate Base64 encoding"""
    try:
        decoded = base64.b64decode(s, validate=True)
        re_encoded = base64.b64encode(decoded).decode('utf-8').rstrip('=')
        original_clean = s.rstrip('=')
        return re_encoded == original_clean
    except (base64.binascii.Error, ValueError, TypeError):
        return False

def process_text():
    input_text = input_entry.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Empty", "FEED ME, SEYMOUR!")
        return

    if is_base64(input_text):
        try:
            decoded = base64.b64decode(input_text).decode('utf-8')
            result_var.set(decoded)
            status_label.config(text="Decoded!", fg="#00ff00")
        except UnicodeDecodeError:
            decoded_bytes = base64.b64decode(input_text)
            result_var.set(str(decoded_bytes))
            status_label.config(text="Decoded! (bytes)", fg="#ffaa00")
    else:
        encoded = base64.b64encode(input_text.encode('utf-8')).decode('utf-8')
        result_var.set(encoded)
        status_label.config(text="Encoded!", fg="#00aaff")


def copy_to_clipboard():
    result = result_var.get()
    if not result:
        copy_status_label.config(text="I am empty.", fg="#ffaa00")
        root.after(2000, lambda: copy_status_label.config(text=""))
        return

    root.clipboard_clear()
    root.clipboard_append(result)
    copy_status_label.config(text="Copied to clipboard!", fg="#00ff00")
    root.after(2000, lambda: copy_status_label.config(text=""))

# GUI Setup
root = tk.Tk()
root.title("Base64 Toggle")
root.geometry("600x400")
root.configure(bg=DARK_BG)
root.resizable(True, True)

# User Input
tk.Label(root, text="Text to (en)(de)code:", bg=DARK_BG, fg=LIGHT_TEXT, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
input_entry = tk.Text(root, height=5, width=60, bg=DARK_ENTRY_BG, fg=LIGHT_TEXT, insertbackground=LIGHT_TEXT, relief="flat")
input_entry.pack(padx=10, pady=5)

# Process Button
process_btn = tk.Button(root, text="Encode/Decode", bg=ACCENT_COLOR, fg=BUTTON_TEXT, activebackground=HOVER_COLOR, activeforeground=LIGHT_TEXT, relief="flat", command=process_text, font=("Arial", 10, "bold"))
process_btn.pack(pady=5)

# Status
status_label = tk.Label(root, text="", bg=DARK_BG, font=("Arial", 10, "bold"))
status_label.pack()

# Result
tk.Label(root, text="Thanks for riding the VMG Express! Result:", bg=DARK_BG, fg=LIGHT_TEXT, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
result_var = tk.StringVar()
result_entry = tk.Entry(root, textvariable=result_var, width=70, bg=DARK_ENTRY_BG, fg=LIGHT_TEXT, relief="flat", state="normal", font=("Arial", 10))
result_entry.pack(padx=10, pady=5)

# Force dark theme even in readonly mode (state="readonly" not used because it breaks the dark mode)
def finalize_result_entry():
    result_entry.config(
        bg=DARK_ENTRY_BG,
        fg=LIGHT_TEXT,
        insertbackground=LIGHT_TEXT,  # cursor color
        #state="readonly"
    )

root.after(100, finalize_result_entry)

# Optional: Don't let user change the text. (Not used, this breaks dark mode in the Results box.)
#def make_readonly(widget):
#    widget.config(state="readonly")

# Give time to pack before locking result field (Not used, this also breaks dark mode in the Results box.)
#root.after(100, make_readonly, result_entry)

# Copy Button
copy_btn = tk.Button(root, text="Copy to Clipboard", bg=ACCENT_COLOR, fg=BUTTON_TEXT, activebackground=HOVER_COLOR, activeforeground=LIGHT_TEXT, relief="flat", command=copy_to_clipboard, font=("Arial", 10, "bold"))
copy_btn.pack(pady=5)

# Copy Status Label (appears below copy button)
copy_status_label = tk.Label(root, text="", bg=DARK_BG, fg=LIGHT_TEXT, font=("Arial", 9, "italic"))
copy_status_label.pack(pady=(5, 10))

# Run
root.mainloop()
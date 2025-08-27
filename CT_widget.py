import tkinter as tk
from CIYA import start_assistant  # Import your main assistant function

def run_assistant():
    start_assistant()  # Call your main assistant logic

root = tk.Tk()
root.title("Customisable Interface for Your Access")
root.geometry("200x200")
root.configure(bg="#282c34")  # Window background

# Optional label for context or title
title_label = tk.Label(
    root,
    text="Welcome to CIYA 2.0",
    font=("Arial", 14),
    bg="#3a3f4b",           # Slightly lighter than window
    fg="#abb2bf"            # Light gray text
)
title_label.place(relx=0.5, rely=0.3, anchor="center")  # Positioned above the button

# Styled button
run_button = tk.Button(
    root,
    text="CIYA",
    command=run_assistant,
    font=("Arial", 12),
    bg="#61afef",           # Button background
    fg="white",             # Button text
    activebackground="#528bbd",  # Optional: darker shade on hover
    activeforeground="white"
)
run_button.place(relx=0.5, rely=0.6, anchor="center")  # Centered below the label

root.mainloop()

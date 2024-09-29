import tkinter as tk
import re
import math

def calculate_crack_time(password):
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26  # Lowercase letters
    if re.search(r'[A-Z]', password):
        charset_size += 26  # Uppercase letters
    if re.search(r'[0-9]', password):
        charset_size += 10  # Digits
    if re.search(r'[@$!%*?&]', password):
        charset_size += 10  # Special symbols

    combinations = math.pow(charset_size, len(password))
    guesses_per_second = 1_000_000_000
    seconds_to_crack = combinations / guesses_per_second

    return seconds_to_crack

def format_time(seconds):
    years = seconds / (365 * 24 * 3600)

    if years > 1_000_000_000:
        return f"{years / 1_000_000_000:.2f} billion years"
    elif years > 1_000_000:
        return f"{years / 1_000_000:.2f} million years"
    elif years > 1:
        return f"{years:.2f} years"
    else:
        return f"{seconds:.2f} seconds"

def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[@$!%*?&]', password):
        score += 1

    crack_time = calculate_crack_time(password)
    formatted_crack_time = format_time(crack_time)

    if score == 5:
        strength = "Strong Password!"
    elif 3 <= score < 5:
        strength = "Moderate Password."
    else:
        strength = "Weak Password."

    return strength, formatted_crack_time

def on_submit():
    password = password_entry.get()
    strength, formatted_crack_time = check_password_strength(password)
    result_label.config(text=f"Password Strength: {strength}\nEstimated time to crack: {formatted_crack_time}")

# GUI Setup
root = tk.Tk()
root.title("Password Strength Checker")

# Set the size of the dialog box and center it on the screen
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates to center the window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Set size and position

tk.Label(root, text="Enter your password:").pack(pady=10)  # Add padding for better spacing

# Increased input box size and font size
password_entry = tk.Entry(root, font=('Arial', 14), width=30)  # Font size medium, increased width
password_entry.pack(pady=10)

submit_button = tk.Button(root, text="Check Strength", command=on_submit, font=('Arial', 14))
submit_button.pack(pady=10)

result_label = tk.Label(root, text="", font=('Arial', 14))  # Increased font size for result label
result_label.pack(pady=10)

root.mainloop()

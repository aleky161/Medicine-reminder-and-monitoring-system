import tkinter as tk
from tkinter import Label, messagebox
import csv
import sys
import subprocess

# Function to check if the entered username and password match the credentials in the CSV file
def authenticate_user(username, password):
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) >= 2 and row[0] == username and row[1] == password:
                return True
        return False

# Login button click event handler
def on_login():
    username = entry_username.get()
    password = entry_password.get()
    if authenticate_user(username, password):
        # Add your code to run script.py here
        try:
            # Use sys.executable to get the path of the current Python interpreter
            python_path = sys.executable
            # Run the script.py file using subprocess with the current Python interpreter
            subprocess.run([python_path, "script.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run script.py: {e}")
    else:
        messagebox.showerror("Error", "Invalid username or password. Please try again.")

import csv
from tkinter import messagebox

def register():
    # Retrieve input values from entry widgets
    username = entry_username.get()
    password = entry_password.get()

    # Check if 'users.csv' file already exists
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            # Iterate through existing users to check if the CSV file already contains a registered user
            for row in reader:
                if row[0] != '':
                    # If a user is already registered, show message box and return
                    messagebox.showwarning("Registration Failed", "Only one user allowed".format(row[0]))
                    return
    except FileNotFoundError:
        # 'users.csv' file does not exist, it's the first registration, so continue with registration
        pass

    # Create a CSV file and write user data to it
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

    messagebox.showinfo("Registration Successful", "Registered user: {}".format(username))


# Create main window
root = tk.Tk()
root.title("Medicine App Login")
root.geometry("300x200")

#Set background color to yellow
root.configure(bg="yellow")

# Set background image
bg_image = tk.PhotoImage(file="family.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set title font and style
title_font = ("Arial", 24, "bold")
title_label = Label(root, text="Medicine Reminder", font=title_font, bg="yellow")
title_label.pack(pady=20)

# Create right frame for login
frame_login = tk.Frame(root, bg="#F0F0F0", bd=5, relief=tk.RAISED)
frame_login.pack(side=tk.RIGHT, padx=200, pady=50)  # Update padx and pady values as needed

# Create username label and entry
label_username = tk.Label(frame_login, text="Username:")
label_username.pack()
entry_username = tk.Entry(frame_login)
entry_username.pack()

# Create password label and entry
label_password = tk.Label(frame_login, text="Password:")
label_password.pack()
entry_password = tk.Entry(frame_login, show="*")
entry_password.pack()

# Update font size for labels and entries
label_username.config(font=("Helvetica", 16))  # Update font size as needed
label_password.config(font=("Helvetica", 16))  # Update font size as needed
entry_username.config(font=("Helvetica", 16))  # Update font size as needed
entry_password.config(font=("Helvetica", 16))  # Update font size as needed

# Create login button
button_login = tk.Button(frame_login, text="Login", command=on_login)
button_login.pack()

# Create left frame for registration
frame_registration = tk.Frame(root, bg="#F0F0F0", bd=5, relief=tk.RAISED)
frame_registration.pack(side=tk.LEFT, padx=200, pady=50)

# Create username label and entry for registration
label_username_registration = tk.Label(frame_registration, text="Username:")
label_username_registration.pack()
entry_username_registration = tk.Entry(frame_registration)
entry_username_registration.pack()

# Create password label and entry for registration
label_password_registration = tk.Label(frame_registration, text="Password:")
label_password_registration.pack()
entry_password_registration = tk.Entry(frame_registration, show="*")
entry_password_registration.pack()

# Update font size for labels and entries
label_username_registration.config(font=("Helvetica", 16))  # Update font size as needed
label_password_registration.config(font=("Helvetica", 16))  # Update font size as needed
entry_username_registration.config(font=("Helvetica", 16))  # Update font size as needed
entry_password_registration.config(font=("Helvetica", 16))  # Update font size as needed

# Create register button
button_register = tk.Button(frame_registration, text="Register", command=register)
button_register.pack()

# Configure login frame
frame_login.configure(bg="#F0F0F0")  # Set background color to light gray
label_username.configure(bg="#F0F0F0")  # Set background color to light gray
entry_username.configure(bg="white")  # Set background color to white
label_password.configure(bg="#F0F0F0")  # Set background color to light gray
entry_password.configure(bg="white")  # Set background color to white
button_login.configure(bg="green", fg="white")  # Set background color to green and text color to white

# Configure registration frame
frame_registration.configure(bg="#F0F0F0")  # Set background color to light gray
label_username_registration.configure(bg="#F0F0F0")  # Set background color to light gray
entry_username_registration.configure(bg="white")  # Set background color to white
label_password_registration.configure(bg="#F0F0F0")  # Set background color to light gray
entry_password_registration.configure(bg="white")  # Set background color to white
button_register.configure(bg="blue", fg="white")  # Set background color to blue and text color to white

root.mainloop()

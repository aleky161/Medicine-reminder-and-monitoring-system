import tkinter as tk
import datetime as dt
import os
from datetime import datetime
import time
from tkinter import ttk
from tkinter import simpledialog
import plyer
from tkinter import messagebox
from tkinter import Label
from tkinter import Frame
from PIL import ImageTk, Image
import csv
import pandas as pd
from twilio.rest import Client
from pandastable import Table, TableModel
from pandastable import config as cfg
from pandastable import themes
import sys
import matplotlib
matplotlib.use('TkAgg')  # Set the backend to TkAgg
import matplotlib.pyplot as plt
sys.path.append("c:/users/aleky/appdata/roaming/python/python310/site-packages")
from reportlab.lib.enums import TA_CENTER
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder



# Define function to save data to CSV file
def save_data():
    # Get data from entry fields
    medicine = entry1.get()
    med_time = entry2.get()
    dosage = entry3.get()

    # Write data to CSV file
    with open('healing_data.csv', mode='a', newline='', encoding='UTF8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Medicine', 'Time', 'Dosage', 'Healing Likelihood'])
        writer.writerow([medicine, med_time, dosage, 1])
        
    # Clear the entry fields
    entry1.delete(0, 'end')
    entry2.delete(0, 'end')
    entry3.delete(0, 'end')

    # Add the new entry to the dataframe
    global entries_df
    try:
        entries_df = pd.concat([entries_df, pd.DataFrame([[medicine, med_time, dosage]], columns=['Medicine', 'Time', 'Dosage'])], ignore_index=True)
    except NameError:
        entries_df = pd.DataFrame([[medicine, med_time, dosage]], columns=['Medicine', 'Time', 'Dosage'])

    update_table()

    # Open the CSV file containing the reminder times set by the user
    with open('healing_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        reminders = [(datetime.strptime(row[1], '%H:%M:%S'), row[0], row[2]) for row in reader if row[1]]

    # Find the reminder that is closest to the current time
    now = dt.datetime.now()
    closest_reminder = min(reminders, key=lambda x: abs(x[0] - now))

    # Extract the medicine, time, and dosage values for the closest reminder
    reminder_time, medicine, dosage = closest_reminder

    # Calculate the number of seconds between now and the reminder time
    seconds_until_reminder = (reminder_time - now).total_seconds()

    # Delay the notification for the specified number of seconds
    print(type(time))
    seconds_until_reminder = max(0, seconds_until_reminder)
    time.sleep(seconds_until_reminder)

    #twilio client setup
    account_sid = 'ACcf6c592ea77bf5173aea508361bfe3fe'   #Replace with your account_sid'
    auth_token = 'c7bd29add3c3cabc08238e5eb4d80c43'    #Replace with your auth_token'
    client = Client(account_sid, auth_token)

    call = client.calls.create(
          from_='+13134255616',     #Replace with the phone number that you got from Twilio
          twiml=f'<Response><Say>Reminder to take your {medicine} of {dosage} at {time}</Say></Response>',
          to='+123456789',    #Phone number that you add on Twilio to be called or messaged
        url = 'https://handler.twilio.com/twiml/EH5ccb729f4b536f539d0f48b5c04452ca',
    )
    print(f"Call SID: {call.sid}")
    
    plyer.notification.notify(
        title="Medicine-Reminder",
        message=f"Reminder to take your {medicine} of {dosage} at {time}",
        app_name="Medicine Reminder",
        timeout=10
    )

# Define function to update the table with new data
def update_table():
    table.delete(*table.get_children())
    for index, row in entries_df.iterrows():
        table.insert("", tk.END, values=tuple(row))

# Load the data from the CSV file
data = pd.read_csv('healing_data.csv')

# Drop any rows where the target variable is NaN
data.dropna(subset=['Healing Likelihood'], inplace=True)

# Split the data into features (X) and labels (y)
X = pd.get_dummies(data.drop('Healing Likelihood', axis=1))
y = data['Healing Likelihood']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train a logistic regression model on the training set
model = LogisticRegression()
model.fit(X_train, y_train)

# Set up the root window
root = tk.Tk()
root.title("Medicine Reminder")
root.geometry("600x500")

# Set background image
bg_image = ImageTk.PhotoImage(Image.open("background.jpg"))
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set title font and style
title_font = ("Arial", 24, "bold")
title_label = Label(root, text="Medicine Reminder", font=title_font)
title_label.pack(pady=20)

# Set header color
header_bg = "#ffcc00"
header_fg = "black"
header_font = ("Arial", 16, "bold")
header_frame = Frame(root, bg=header_bg, padx=10, pady=10)
header_frame.pack(fill="x")
header_label = Label(header_frame, text="Your Life Matters", font=header_font, bg=header_bg, fg=header_fg)
header_label.pack()

# Create a frame for the input widgets
input_frame = tk.Frame(root, bg='#f2f2f2')
input_frame.pack(padx=10, pady=10)

# Create the widgets for entering data
def create_widgets():
    global label1, label2, label3, entry1, entry2, entry3, button1
    
    label1 = tk.Label(root, text="Enter medicine name:")
    label1.pack(side=tk.TOP, padx=10, pady=10)

    entry1 = tk.Entry(root, width=30)
    entry1.pack(side=tk.TOP)

    label2 = tk.Label(root, text="Enter time (hh:mm:ss):")
    label2.pack(side=tk.TOP, padx=10, pady=10)

    entry2 = tk.Entry(root, width=30)
    entry2.pack(side=tk.TOP)

    label3 = tk.Label(root, text="Dosage:")
    label3.pack(side=tk.TOP, padx=10, pady=10)

    entry3 = tk.Entry(root, width=30)
    entry3.pack(side=tk.TOP)

    button1 = tk.Button(root, text="Set Reminder", command=save_data)
    button1.pack(side=tk.TOP, pady=10, anchor='s')
    button1.configure(bg='yellow', activebackground='green')

create_widgets()

#Create a frame for the table
table_frame = tk.Frame(root, bg='#f2f2f2')
table_frame.pack(padx=10, pady=10)

#Create the table
table = ttk.Treeview(table_frame, columns=['Medicine', 'Time', 'Dosage'], show='headings',height=15)
table.pack(side=tk.LEFT)

table.heading('Medicine', text='Medicine')
table.heading('Time', text='Time')
table.heading('Dosage', text='Dosage')

# Define a function to read the CSV file and populate the table with its data
def load_data_from_csv():
    with open('healing_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table.insert('', tk.END, values=[row['MEDICINE'], row['TIME'], row['DOSAGE']])

# Load the data from the CSV file and populate the table
load_data_from_csv()

# Create a frame for the right side of the window
right_frame = tk.Frame(table_frame, bg='#f2f2f2')
right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

# Define a function to read the CSV file and extract the values from the specified column
def read_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        values = [float(row['Healing Likelihood']) for row in reader if row['Healing Likelihood'] is not None]
    return values

# Read the values from the CSV file
values = read_csv('healing_data.csv')

# Define a list to hold the values extracted from the CSV file
values = []

# Open the CSV file and read the values
with open('healing_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        values.append(row['Healing Likelihood'])

# Define a list to hold the value entry strings
value_entries = []

# Populate the value entry strings with the extracted values
for value in values:
    value_entry_string = tk.StringVar(value=str(value))
    value_entries.append(value_entry_string)

def make_predictions():
    # Read the values from the CSV file
    values = read_csv('healing_data.csv')
    # Count the number of times the medicine was taken
    medicine_taken = sum(1 for value in values if value == 1)
    # Calculate the percentage of times the medicine was taken
    healing_probability = medicine_taken / len(values) * 100
    # Update the predictions list with the message
    message = f"Your healing probability is {healing_probability:.2f}%. \nYour life matters."
    if healing_probability >= 60:
        message += "\nGreat job! Keep taking your medicine as prescribed.🥰"
    else:
        message += "\nDon't give up! Keep taking your medicine as prescribed.❤️"
    # Split the message into multiple lines
    lines = message.split('\n')
    for message in lines:
        predictions_list.insert(tk.END, message)

# Create the prediction button
predict_button = tk.Button(right_frame, text='Predict', command=make_predictions)
predict_button.pack(padx=5, pady=5)
predict_button.configure(bg='yellow', activebackground='green')

# Create the list of predicted values
predictions_list = tk.Listbox(right_frame, width=60, height=15)
predictions_list.pack(padx=5, pady=5, fill=tk.Y, expand=True)

#Create a scrollbar for the table
scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table.configure(yscrollcommand=scrollbar.set)

# set the style for the table
class TableStyle:
    def __init__(self):
        self.style.configure('Treeview', rowheight=30, background='#E0FFFF', fieldbackground='#E0FFFF')
        self.style.configure('Treeview.Heading', font=('Helvetica', 12), background='#FFFF00', foreground='black')
        cell_style = {"font": ("Helvetica", 12), "borderwidth": 0, "foreground": "#006400", "background": "#B0E0E6"}
        alt_cell_style = {"font": ("Helvetica", 12), "borderwidth": 0, "foreground": "black", "background": "#F0FFF0"}
        self.style.configure("Treeview.Cell", **cell_style)
        self.style.map("Treeview.Cell", background=[("odd", alt_cell_style["background"]), ("even", cell_style["background"])])
        
        # configure background colors for first and last column
        self.style.configure('Treeview.Cell.Date', background='#9ACD32', foreground='black')
        self.style.configure('Treeview.Cell.Duration', background='#87CEFA', foreground='black')
        self.style.layout('Treeview', [
            ('Treeview.treearea', {'sticky': 'nswe'}),
            ('Treeview.Heading', {'sticky': 'we'}),
            ('Treeview.Cell', {'sticky': 'we', 'border': '1', 'foreground': 'black', 'padding': '5'}),
            ('Treeview.Row', {'sticky': 'nswe', 'border': '0', 'background': 'grey50'})
        ])

# create a new tablemodel and apply the style to it
table_model = TableModel()
data = []
entries_df = pd.DataFrame(data, columns=["Medicine", "Time", "Dosage"])
table_model.df = entries_df
table.tag_configure('mytag', font=('Arial', 12), background='#F7F7F7', foreground='#333333')

# create the table using the tablemodel
pt = Table(table_frame, model=table_model)
pt.pack(expand=True, fill='both')


# start the main loop
root.mainloop()


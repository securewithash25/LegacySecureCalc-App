import tkinter as tk
from tkinter import messagebox

from cryptography.fernet import Fernet

# User Login Window
def show_login_screen():
    login_win = tk.Tk()
    login_win.title("User Login")
    login_win.geometry("300x150")
    login_win.configure(bg="#f4f4f4")

    tk.Label(login_win, text="Username:").pack()
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password:").pack()
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def validate_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "pass123":  # 🔐 Temporary login
            login_win.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Button(login_win, text="Login", command=validate_login).pack(pady=10)

    login_win.mainloop()

def smart_tip(result):
    if result > 10000:
        return "💡 That's a large result. Consider double-checking your inputs!"
    elif 0 < result < 1:
        return "🧠 Very small result. Are you working with percentages or decimals?"
    elif result == 0:
        return "⚠️ A result of 0 usually means one of your inputs was 0."
    elif result < 0:
        return "🔎 Negative result. Make sure that’s expected."
    else:
        return "✅ Calculation looks good!"


# Call login at launch
show_login_screen()

import datetime

import csv
import os


def log_to_csv(operation, num1, num2, result):
    file_exists = os.path.isfile("securecalc_data.csv")
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("securecalc_data.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(["Timestamp", "Operation", "Number 1", "Number 2", "Result"])

        writer.writerow([time_now, operation, num1, num2, result])


def log_to_file(operation, num1, num2, result):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{time_now}] {operation}: {num1} and {num2} = {result}\n"
    with open("securecalc_log.txt", "a") as file:
        file.write(log_entry)


# Replace with your actual saved key
key = b'aTeF8vKM9ZC84UObY69HLFYI5mZni4aLM9JAx7yX0cA='
cipher = Fernet(key)

def write_encrypted_log(message):
    encrypted = cipher.encrypt(message.encode())
    with open("division_log_encrypted.txt", "ab") as f:
        f.write(encrypted + b'\n')

def send_alert(message):
    print(f"📢 Simulated Alert: {message}")

def perform_division():
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())

        if num1 < 0 or num2 < 0:
            raise ValueError("Negative numbers are not allowed.")

        result = num1 / num2
        result_label.config(text=f"✅ Result: {round(result, 2)}")

        tip = smart_tip(result)
        messagebox.showinfo("Smart Tip", tip)

        log_msg = f"[{time_now}] ✅ SUCCESS: {num1} / {num2} = {round(result, 2)}"
        write_encrypted_log(log_msg)

    except ZeroDivisionError:
        error_msg = "❌ Error: Cannot divide by zero."
        messagebox.showerror("Division Error", error_msg)
        send_alert(error_msg)

        log_to_file("DIVIDE", num1, num2, result)

        log_to_csv("DIVIDE", num1, num2, result)

        log_msg = f"[{time_now}] ❌ ERROR: Division by zero with inputs {entry_num1.get()}, {entry_num2.get()}"
        write_encrypted_log(log_msg)

    except ValueError as e:
        error_msg = f"❌ Error: {e}"
        messagebox.showerror("Input Error", error_msg)
        send_alert(error_msg)

        log_msg = f"[{time_now}] ❌ ERROR: {e} with inputs {entry_num1.get()}, {entry_num2.get()}"
        write_encrypted_log(log_msg)

def perform_multiplication():
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())

        if num1 < 0 or num2 < 0:
            raise ValueError("Negative numbers are not allowed.")

        result = num1 * num2
        result_label.config(text=f"✔️ Result: {round(result, 2)}")

        tip = smart_tip(result)
        messagebox.showinfo("Smart Tip", tip)

        log_to_file("MULTIPLY", num1, num2, result)

        log_to_csv("MULTIPLY", num1, num2, result)

        log_msg = f"[{time_now}] ✅ SUCCESS: {num1} × {num2} = {round(result, 2)}"
        write_encrypted_log(log_msg)

    except ValueError as e:
        error_msg = f"❌ Error: {e}"
        messagebox.showerror("Input Error", error_msg)
        send_alert(error_msg)

        log_msg = f"[{time_now}] ❌ ERROR: {e} with inputs {entry_num1.get()}, {entry_num2.get()}"
        write_encrypted_log(log_msg)


# GUI setup
app = tk.Tk()
app.title("Legacy SecureCalc™")
app.geometry("400x300")
app.configure(bg="#f4f4f4")

# Header
tk.Label(app, text="Legacy SecureCalc™", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333").pack(pady=10)

# Inputs
frame = tk.Frame(app, bg="#f4f4f4")
frame.pack(pady=10)

entry_num1 = tk.Entry(frame, font=("Arial", 12))
entry_num1.grid(row=0, column=0, padx=10)

entry_num2 = tk.Entry(frame, font=("Arial", 12))
entry_num2.grid(row=0, column=1, padx=10)

# Divide button
tk.Button(app, text="Divide", command=perform_division, font=("Arial", 12), bg="#4CAF50", fg="white", padx=20).pack(pady=10)

tk.Button(app, text="Multiply", command=perform_multiplication, font=("Arial", 12), bg="#2196F3", fg="white", padx=20).pack(pady=10)


# Result
result_label = tk.Label(app, text="", font=("Arial", 14), bg="#f4f4f4", fg="#333")
result_label.pack(pady=10)

# Run the GUIS
app.mainloop()
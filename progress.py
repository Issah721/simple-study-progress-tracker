#This python program will track my progress
from datetime import datetime

print("Welcome to Progress tracker, Ensure to log your progress daily!")
progress_log = input("Enter your progress for today: ")

# Get the current timestamp and format it
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"[{timestamp}] {progress_log}\n"

print("Logging your progress...")
with open("progress.txt", "a") as file:
    file.write(log_entry)

print("Progress logged successfully!")
print(f"Here is your progress so far: {open('progress.txt').read()}")

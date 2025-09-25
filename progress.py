#This python program will track my progress

print("Welcome to Progress tracker, Ensure to log your progress daily!")
progress_log = input("Enter your progress for today: ")

print("Logging your progress...")
with open("progress.txt", "a") as file:
    file.write(progress_log + "\n")

print("Progress logged successfully!")
print(f"Here is your progress so far: {open('progress.txt').read()}")

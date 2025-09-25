#This python program will track my progress
from datetime import datetime

FILENAME = "progress.txt"

def add_progress_entry(filename):
    """Gets user input and appends it with a timestamp to the progress file."""
    while True:
        progress_log = input("Enter your progress for today: ")
        # Ensure the input is not empty or just whitespace
        if progress_log.strip():
            break
        print("Progress log cannot be empty. Please try again.")

    # Get the current timestamp and format it
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {progress_log}\n"

    print("Logging your progress...")
    with open(filename, "a") as file:
        file.write(log_entry)
    print("Progress logged successfully!")

def view_progress(filename):
    """Reads and prints all entries from the progress file."""
    print("\n--- Your Progress So Far ---")
    try:
        with open(filename, "r") as file:
            content = file.read()
            if not content:
                print("No progress has been logged yet. Add your first entry!")
            else:
                print(content)
    except FileNotFoundError:
        print("No progress file found. Your first entry will create it.")

def main():
    """Displays the main menu and handles user choices."""
    print("Welcome to Progress Tracker!")

    while True:
        print("\n--- Menu ---")
        print("1. Add a new progress entry")
        print("2. View all progress")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            add_progress_entry(FILENAME)
        elif choice == '2':
            view_progress(FILENAME)
        elif choice == '3':
            print("Exiting Progress Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()

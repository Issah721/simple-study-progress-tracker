#This python program will track my progress
from datetime import datetime
import json

class ProgressTracker:
    """A class to track progress by logging entries to a file."""

    def __init__(self, filename="progress.json"):
        """Initializes the ProgressTracker with a filename."""
        self.filename = filename

    def add_progress_entry(self):
        """Gets user input and appends it with a timestamp to the progress file."""
        while True:
            progress_log = input("Enter your progress for today: ")
            # Ensure the input is not empty or just whitespace
            if progress_log.strip():
                break
            print("Progress log cannot be empty. Please try again.")
        
        while True:
            category = input("Enter a category for this entry (e.g., Python, Security): ")
            if category.strip():
                break
            print("Category cannot be empty. Please try again.")

        # Get the current timestamp and format it
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        new_entry = {
            "timestamp": timestamp,
            "category": category.strip(),
            "log": progress_log.strip()
        }

        print("Logging your progress...")
        try:
            with open(self.filename, "r") as file:
                entries = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            entries = []
        
        entries.append(new_entry)

        with open(self.filename, "w") as file:
            json.dump(entries, file, indent=4)

        print("Progress logged successfully!")

    def view_progress(self):
        """Reads and prints all entries from the progress file."""
        print("\n--- Your Progress So Far ---")
        try:
            with open(self.filename, "r") as file:
                entries = json.load(file)
                if not entries:
                    print("No progress has been logged yet. Add your first entry!")
                    return
            
            for entry in entries:
                print(f"[{entry['timestamp']}] [{entry['category']}] {entry['log']}")

        except (FileNotFoundError, json.JSONDecodeError):
            print("No progress file found. Your first entry will create it.")

    def migrate_from_txt(self, old_filename="progress.txt"):
        """Migrates entries from the old .txt format to the new .json format."""
        print(f"\nStarting migration from {old_filename}...")
        try:
            with open(old_filename, "r") as txt_file:
                txt_lines = txt_file.readlines()
        except FileNotFoundError:
            print(f"Migration skipped: {old_filename} not found.")
            return

        try:
            with open(self.filename, "r") as json_file:
                json_entries = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            json_entries = []

        # Create a set of existing timestamps for quick lookups to avoid duplicates
        existing_timestamps = {entry['timestamp'] for entry in json_entries}
        newly_migrated_count = 0

        for line in txt_lines:
            line = line.strip()
            if not line:
                continue
            
            # Parse the old format: [YYYY-MM-DD HH:MM:SS] Log message
            timestamp = line[1:20]
            log = line[22:]

            if timestamp in existing_timestamps:
                continue # Skip if this entry has already been migrated

            migrated_entry = {
                "timestamp": timestamp,
                "category": "Legacy", # Assign a default category
                "log": log
            }
            json_entries.append(migrated_entry)
            newly_migrated_count += 1

        if newly_migrated_count > 0:
            # Sort entries by timestamp before saving
            json_entries.sort(key=lambda x: x['timestamp'])
            with open(self.filename, "w") as file:
                json.dump(json_entries, file, indent=4)
            print(f"Successfully migrated {newly_migrated_count} new entries.")
        else:
            print("No new entries to migrate.")

    def run(self):
        """Displays the main menu and handles user choices."""
        print("Welcome to Progress Tracker!")

        while True:
            print("\n--- Menu ---")
            print("1. Add a new progress entry")
            print("2. View all progress")
            print("3. Migrate from progress.txt")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.add_progress_entry()
            elif choice == '2':
                self.view_progress()
            elif choice == '3':
                self.migrate_from_txt()
            elif choice == '4':
                print("Exiting Progress Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

def main():
    """Initializes the tracker and runs the application."""
    tracker = ProgressTracker("progress.json")
    tracker.run()

if __name__ == "__main__":
    main()

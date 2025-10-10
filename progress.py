#This python program will track my progress
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any, Optional

Entry = Dict[str, str]
Entries = List[Entry]

class ProgressTracker:
    """A class to track progress by logging entries to a file."""

    def __init__(self, filename: str = "progress.json"):
        """Initializes the ProgressTracker with a filename."""
        self.filename = filename

    def _read_entries(self) -> Entries:
        """Reads entries from the JSON file."""
        try:
            with open(self.filename, "r") as file:
                entries: Entries = json.load(file)
                return entries
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_entries(self, entries: Entries) -> None:
        """Writes entries to the JSON file."""
        with open(self.filename, "w") as file:
            json.dump(entries, file, indent=4)

    def add_progress_entry(self) -> None:
        """Gets user input and appends it with a timestamp to the progress file."""
        while True:
            progress_log = input("Enter your progress for today: ")
            if progress_log.strip():
                break
            print("Progress log cannot be empty. Please try again.")
        
        while True:
            category = input("Enter a category for this entry (e.g., Python, Security): ")
            if category.strip():
                break
            print("Category cannot be empty. Please try again.")

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        new_entry = {
            "timestamp": timestamp,
            "category": category.strip(),
            "log": progress_log.strip()
        }

        print("Logging your progress...")
        entries = self._read_entries()
        entries.append(new_entry)
        self._write_entries(entries)

        print("Progress logged successfully!")

    def view_progress(self) -> None:
        """Reads and prints all entries from the progress file."""
        print("\n--- Your Progress So Far ---")
        entries = self._read_entries()

        if not entries:
            print("No progress has been logged yet. Add your first entry!")
        else:
            for entry in entries:
                print(f"[{entry['timestamp']}] [{entry['category']}] {entry['log']}")

    def calculate_streak(self) -> int:
        """Calculates the current streak of consecutive days with entries."""
        entries = self._read_entries()
        if not entries:
            return 0

        # Get unique dates from entries, sorted in reverse chronological order
        entry_dates = sorted(
            list(
                {datetime.strptime(e["timestamp"], "%Y-%m-%d %H:%M:%S").date() for e in entries}
            ),
            reverse=True
        )

        today = datetime.now().date()
        
        # If the last entry was before yesterday, the streak is broken.
        if entry_dates[0] < today - timedelta(days=1):
            return 0

        streak = 0
        # Start checking from today or yesterday, depending on the last entry date
        expected_date = entry_dates[0]
        for entry_date in entry_dates:
            if entry_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break # The streak is broken
        return streak

    def run(self) -> None:
        """Displays the main menu and handles user choices."""
        print("Welcome to Progress Tracker!")

        while True:
            current_streak = self.calculate_streak()
            print(f"\nYour current streak: {current_streak} day(s) 🔥")
            print("\n--- Menu ---")
            print("1. Add a new progress entry")
            print("2. View all progress")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                self.add_progress_entry()
            elif choice == '2':
                self.view_progress()
            elif choice == '3':
                print("Exiting Progress Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")

def main() -> None:
    """Initializes the tracker and runs the application."""
    tracker = ProgressTracker("progress.json")
    tracker.run()

if __name__ == "__main__":
    main()

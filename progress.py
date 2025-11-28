import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import Counter

# Try to import rich and questionary, handle if missing
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import print as rprint
    import questionary
    DEPENDENCIES_INSTALLED = True
except ImportError:
    DEPENDENCIES_INSTALLED = False
    print("Warning: 'rich' and 'questionary' libraries are not installed.")
    print("Please run: pip install -r requirements.txt")
    print("Falling back to basic mode where possible, but some features may crash.")

Entry = Dict[str, Any]
Entries = List[Entry]

class ProgressTracker:
    """A class to track progress by logging entries to a file."""

    def __init__(self, filename: str = "progress.json"):
        """Initializes the ProgressTracker with a filename."""
        self.filename = filename
        if DEPENDENCIES_INSTALLED:
            self.console = Console()
        else:
            self.console = None

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

    def get_streak(self) -> int:
        """Calculates the current study streak in days."""
        entries = self._read_entries()
        if not entries:
            return 0
        
        # Get unique dates with entries, sorted newest first
        dates = sorted(set(e['timestamp'].split(' ')[0] for e in entries), reverse=True)
        if not dates:
            return 0
            
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # If no entry today or yesterday, streak is 0
        if dates[0] != today and dates[0] != yesterday:
            return 0
            
        streak = 1
        current_date = datetime.strptime(dates[0], "%Y-%m-%d")
        
        for i in range(1, len(dates)):
            prev_date = datetime.strptime(dates[i], "%Y-%m-%d")
            diff = (current_date - prev_date).days
            if diff == 1:
                streak += 1
                current_date = prev_date
            else:
                break
                
        return streak

    def get_category_breakdown(self) -> Dict[str, int]:
        """Returns a count of entries per category."""
        entries = self._read_entries()
        categories = [e.get('category', 'Unknown') for e in entries]
        return dict(Counter(categories))

    def add_progress_entry(self) -> None:
        """Gets user input and appends it to the progress file."""
        if not DEPENDENCIES_INSTALLED:
            print("Cannot run interactive add without dependencies.")
            return

        log = questionary.text("Enter your progress for today:").ask()
        if not log: return
        
        # Get existing categories to suggest
        entries = self._read_entries()
        existing_categories = sorted(list(set(e.get('category', 'General') for e in entries)))
        if "General" not in existing_categories:
            existing_categories.append("General")
        
        choices = existing_categories + ["Create New..."]
        
        category = questionary.select(
            "Choose a category:",
            choices=choices
        ).ask()
        
        if category == "Create New...":
            category = questionary.text("Enter new category name:").ask()
            
        if not category: return

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        new_entry = {
            "timestamp": timestamp,
            "category": category.strip(),
            "log": log.strip(),
            "xp": 10 # Base XP for an entry
        }

        entries.append(new_entry)
        self._write_entries(entries)

        self.console.print(Panel(f"[green]Progress logged successfully![/green]\n[bold]+10 XP[/bold]", title="Success"))

    def view_progress(self, entries: Optional[Entries] = None) -> None:
        """Reads and prints entries."""
        if not DEPENDENCIES_INSTALLED:
            print("Cannot view rich progress without dependencies.")
            return

        if entries is None:
            entries = self._read_entries()

        if not entries:
            self.console.print("[yellow]No progress has been logged yet.[/yellow]")
            return

        # Create Table
        table = Table(title="Study Progress")
        table.add_column("Timestamp", style="cyan", no_wrap=True)
        table.add_column("Category", style="magenta")
        table.add_column("Log", style="white")
        table.add_column("XP", style="green", justify="right")

        total_xp = 0
        for entry in entries:
            xp = entry.get('xp', 0)
            total_xp += xp
            table.add_row(
                entry['timestamp'],
                entry['category'],
                entry['log'],
                str(xp)
            )

        self.console.print(table)
        
        # Stats Footer
        streak = self.get_streak()
        stats_panel = Panel(
            f"[bold]Current Streak:[/bold] {streak} days\n[bold]Total XP:[/bold] {total_xp}",
            title="Stats",
            expand=False
        )
        self.console.print(stats_panel)

    def search_entries(self) -> None:
        """Search entries by keyword."""
        if not DEPENDENCIES_INSTALLED: return
        
        term = questionary.text("Enter search term:").ask()
        if not term: return
        
        all_entries = self._read_entries()
        filtered = [
            e for e in all_entries 
            if term.lower() in e.get('log', '').lower() or term.lower() in e.get('category', '').lower()
        ]
        
        self.console.print(f"\n[bold]Search Results for '{term}':[/bold]")
        self.view_progress(filtered)

    def delete_entry(self) -> None:
        """Delete a specific entry."""
        if not DEPENDENCIES_INSTALLED: return
        
        entries = self._read_entries()
        if not entries:
            print("No entries to delete.")
            return
            
        # Create choices for selection
        choices = []
        for i, entry in enumerate(entries):
            choices.append(questionary.Choice(
                title=f"{entry['timestamp']} - {entry['log'][:50]}...",
                value=i
            ))
        choices.append(questionary.Choice(title="Cancel", value=-1))
        
        index = questionary.select(
            "Select an entry to delete:",
            choices=choices
        ).ask()
        
        if index != -1:
            confirm = questionary.confirm(f"Are you sure you want to delete this entry?").ask()
            if confirm:
                deleted = entries.pop(index)
                self._write_entries(entries)
                self.console.print(f"[red]Deleted entry:[/red] {deleted['log']}")

    def edit_entry(self) -> None:
        """Edit a specific entry."""
        if not DEPENDENCIES_INSTALLED: return
        
        entries = self._read_entries()
        if not entries:
            print("No entries to edit.")
            return
            
        # Create choices for selection
        choices = []
        for i, entry in enumerate(entries):
            choices.append(questionary.Choice(
                title=f"{entry['timestamp']} - {entry['log'][:50]}...",
                value=i
            ))
        choices.append(questionary.Choice(title="Cancel", value=-1))
        
        index = questionary.select(
            "Select an entry to edit:",
            choices=choices
        ).ask()
        
        if index != -1:
            entry = entries[index]
            
            # Edit Log
            new_log = questionary.text("Edit log:", default=entry['log']).ask()
            
            # Edit Category
            # Get existing categories
            existing_categories = sorted(list(set(e.get('category', 'General') for e in entries)))
            if entry['category'] not in existing_categories:
                existing_categories.append(entry['category'])
            
            new_category = questionary.select(
                "Edit category:",
                choices=existing_categories + ["Create New..."],
                default=entry['category']
            ).ask()
            
            if new_category == "Create New...":
                new_category = questionary.text("Enter new category name:").ask()
            
            if new_log and new_category:
                entries[index]['log'] = new_log.strip()
                entries[index]['category'] = new_category.strip()
                self._write_entries(entries)
                self.console.print("[green]Entry updated successfully![/green]")

    def run(self) -> None:
        """Displays the main menu and handles user choices."""
        if not DEPENDENCIES_INSTALLED:
            print("Dependencies missing. Please install them.")
            return

        self.console.print("[bold blue]Welcome to Progress Tracker 2.0![/bold blue]")

        while True:
            choice = questionary.select(
                "Main Menu",
                choices=[
                    "Add Entry",
                    "View Progress",
                    "Search",
                    "Edit Entry",
                    "Delete Entry",
                    "Exit"
                ]
            ).ask()

            if choice == "Add Entry":
                self.add_progress_entry()
            elif choice == "View Progress":
                self.view_progress()
            elif choice == "Search":
                self.search_entries()
            elif choice == "Edit Entry":
                self.edit_entry()
            elif choice == "Delete Entry":
                self.delete_entry()
            elif choice == "Exit":
                self.console.print("[bold]Goodbye! Keep learning![/bold]")
                break

def main() -> None:
    """Initializes the tracker and runs the application."""
    tracker = ProgressTracker("progress.json")
    tracker.run()

if __name__ == "__main__":
    main()

# Progress Tracker CLI

This is a simple command-line application built with Python to help track personal progress. It was created as a practical project while learning Python, evolving from a basic script into an object-oriented program.

## Features

* **Add Entries**: Add new progress entries with a descriptive log and a category.
* **Timestamping**: Each entry is automatically timestamped.
* **View History**: View a complete, chronological history of all your logged progress.
* **Streak Counter**: Tracks and displays your consecutive daily progress to keep you motivated.
* **Simple Storage**: Data is stored in a clean, human-readable `progress.json` file.

## Prerequisites

This project started as a single Python script with a few functions to handle file I/O and user input. As my understanding of Python grew, I refactored the code to embrace Object-Oriented Programming (OOP) principles.

The current version uses a `ProgressTracker` class to encapsulate the application's data (the filename) and its behavior (adding and viewing entries). This change has made the code more organized, reusable, and easier to extend with new features in the future.

No special installation is required. Simply download or clone the `progress.py` script to a local directory.

The application menu looks something like this:

Welcome to Progress Tracker!

Your current streak: 5 day(s) 🔥

--- Menu ---
1.Add a new progress entry
2. View all progress
3. Exit
Enter your choice (1-3):

1. **Add a new progress entry**: Prompts you to enter a log message and a category for your new entry.
2. **View all progress**: Displays all previously saved entries from `progress.json`.
3. **Exit**: Closes the application.

## Data Format

Your progress is stored in `progress.json` as a list of entry objects. Each entry has the following structure:

```json
{
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "category": "YourCategory",
    "log": "Your progress message."
}
```

# Progress Tracker CLI

This is a simple command-line application built with Python to help track personal progress. It has been upgraded with a beautiful interactive interface and new features to make tracking your learning journey even better.

## Features

*   **Interactive Menu**: Navigate easily with a keyboard-friendly menu.
*   **Rich Output**: View your progress in a beautifully formatted table with colors.
*   **Streak Tracking**: Keep your momentum going by tracking your daily study streak.
*   **Search**: Quickly find past entries by keyword.
*   **Edit & Delete**: Fix mistakes or remove entries directly from the CLI.
*   **XP System**: Earn XP for every entry you log!
*   **Simple Storage**: Data is stored in a clean, human-readable `progress.json` file.

## Prerequisites

*   Python 3.7+
*   `rich`
*   `questionary`

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Musau111/simple-study-progress-tracker.git
    cd simple-study-progress-tracker
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script from your terminal:

```bash
python progress.py
```

You will be presented with an interactive menu:

*   **Add Entry**: Log your progress for the day.
*   **View Progress**: See your history, streak, and total XP.
*   **Search**: Find specific entries.
*   **Edit Entry**: Modify an existing log.
*   **Delete Entry**: Remove an entry.
*   **Exit**: Close the application.

## Data Format

Your progress is stored in `progress.json` as a list of entry objects. Each entry has the following structure:

```json
{
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "category": "YourCategory",
    "log": "Your progress message.",
    "xp": 10
}
```

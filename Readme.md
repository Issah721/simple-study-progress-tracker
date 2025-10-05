# Progress Tracker

This is a simple command-line application built with Python to help track personal progress. It was created as a practical project while learning Python, evolving from a basic script into an object-oriented program.

## Features

* Add new progress entries with an automatic timestamp and a category.
* View all previously logged progress entries.
* All entries are saved in a structured format to a local JSON file (`progress.json`).

## Project Evolution

This project started as a single Python script with a few functions to handle file I/O and user input. As my understanding of Python grew, I refactored the code to embrace Object-Oriented Programming (OOP) principles.

The current version uses a `ProgressTracker` class to encapsulate the application's data (the filename) and its behavior (adding and viewing entries). This change has made the code more organized, reusable, and easier to extend with new features in the future.

## How to Run

1. Make sure you have Python installed.
2. Navigate to the project directory in your terminal.
3. Run the script using the command: `python progress.py`

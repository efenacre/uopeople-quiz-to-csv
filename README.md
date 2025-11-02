# SelfQuiz Scraping

**SelfQuiz Scraping** is a Python utility that automatically extracts and aggregates quiz data from multiple **UoPeople (Moodle-based)** quiz result HTML files.  
When you place your quiz HTML files into the `html/` folder and run the script, it will generate a unified **`quiz.csv`** and **`quiz.json`** file containing all questions, options, and correct answers.

## Purpose

This script helps UoPeople students efficiently collect and analyze their quiz data.  
It converts multiple downloaded quiz result pages into a structured CSV or JSON file for easier review, comparison, or statistical analysis.

Typical use cases:
- Review quiz questions and answers across multiple weeks or courses.
- Build a personal study database.
- Export data for analysis or visualization.

## Requirements

- **Python** 3.10 or higher  
- Operating System: Windows, macOS, or Linux

## Folder Structure

```
your-repo/
├─ html/                  # Place all your quiz .html files here
├─ selfquiz_scraping.py   # The main script
├─ requirements.txt
└─ README.md
```

## Setup (with `.venv` virtual environment)

1. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

2. **Activate the environment**

   * macOS / Linux:

     ```bash
     source .venv/bin/activate
     ```
   * Windows (PowerShell):

     ```bash
     .venv\Scripts\Activate.ps1
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Create a folder named `html/` in the same directory as `selfquiz_scraping.py`.
2. Place all your downloaded quiz HTML files inside the `html/` folder.
3. Run the script:

   ```bash
   python selfquiz_scraping.py
   ```
4. If successful, the following files will be generated in the same directory:

   ```
   quiz.json
   quiz.csv
   ```

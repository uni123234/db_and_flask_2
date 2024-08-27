"""
This module initializes the SQLite database for the application.

It creates a table named 'test' with columns:
- question: the question text (must be unique)
- answers: possible answers (stored as a text)
- correct: the correct answer (stored as a text)
"""

import sqlite3

with sqlite3.connect("app.db") as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS test (question TEXT UNIQUE, answers TEXT, correct TEXT)"
    )

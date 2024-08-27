"""
Database operations for the application.

This module provides functions to interact with the SQLite database,
including adding questions, retrieving questions, and getting correct answers.
"""

import sqlite3


def add_question(question, answers, correct):
    """
    Add a question to the database.

    Args:
        question (str): The question text.
        answers (str): The possible answers, separated by commas.
        correct (str): The correct answer.

    Returns:
        str: Success or error message.
    """
    msg = ""
    try:
        with sqlite3.connect("app.db") as conn:
            cr = conn.cursor()
            cr.execute(
                "INSERT INTO test (question, answers, correct) VALUES (?, ?, ?)",
                (question, answers, correct),
            )
            conn.commit()
            msg = "Record successfully added"
    except sqlite3.Error as e:
        conn.rollback()
        print(e)
        msg = "Error in insert operation"
    return msg


def get_questions():
    """
    Retrieve all questions from the database.

    Returns:
        list: List of questions from the database.
    """
    res = None
    try:
        with sqlite3.connect("app.db") as conn:
            conn.row_factory = sqlite3.Row
            cr = conn.cursor()
            cr.execute("SELECT * FROM test")
            res = cr.fetchall()
    except sqlite3.Error as e:
        print(e)
    return res


def get_correct_answer(question_id):
    """
    Retrieve the correct answer for a given question ID.

    Args:
        question_id (str): The question ID.

    Returns:
        str: The correct answer, or None if not found.
    """
    try:
        with sqlite3.connect("app.db") as conn:
            cr = conn.cursor()
            cr.execute("SELECT correct FROM test WHERE question = ?", (question_id,))
            correct_answer = cr.fetchone()
            if correct_answer:
                return correct_answer[0]
            else:
                return None
    except sqlite3.Error as e:
        print(e)
        return None

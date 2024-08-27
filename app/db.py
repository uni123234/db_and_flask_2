import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)


def add_question(question, answers, correct):
    msg = ""
    with sqlite3.connect("app.db") as conn:
        try:
            cr = conn.cursor()
            cr.execute("INSERT INTO test (question, answers, correct) VALUES (?, ?, ?)",
                       (question, answers, correct))
            conn.commit()
            msg = "Record successfully added"
        except Exception as e:
            conn.rollback()
            print(e)
            msg = "Error in insert operation"
    return msg


def get_questions():
    res = None
    with sqlite3.connect("app.db") as conn:
        conn.row_factory = sqlite3.Row
        cr = conn.cursor()
        cr.execute("SELECT * FROM test")
        res = cr.fetchall()
    return res


def get_correct_answer(question_id):
    with sqlite3.connect("app.db") as conn:
        cr = conn.cursor()
        cr.execute("SELECT correct FROM test WHERE question = ?",
                   (question_id,))
        correct_answer = cr.fetchone()
        if correct_answer:
            return correct_answer[0]
        else:
            return None

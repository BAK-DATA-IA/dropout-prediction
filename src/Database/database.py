import sqlite3
from datetime import datetime


def create_connection():
    return sqlite3.connect("src/database/student_dropout.db")


def create_table():

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_date TEXT,
            course TEXT,
            prediction TEXT,
            probability REAL
        )
    """)

    connection.commit()

    connection.close()



import sqlite3
from datetime import datetime
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "student_dropout.db"

def create_connection():
    return sqlite3.connect(DB_PATH)


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



def save_prediction(course, prediction, probability):

    connection = create_connection()
    cursor = connection.cursor()

    prediction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO prediction_history
        (prediction_date, course, prediction, probability)
        VALUES (?, ?, ?, ?)
        """,
        (prediction_date, course, prediction, probability)
    )

    connection.commit()


    connection.close()

def load_history():

    connection = create_connection()

    history = pd.read_sql_query(
        """
        SELECT
            prediction_date,
            course,
            prediction,
            probability
        FROM prediction_history
        ORDER BY prediction_date DESC
        """,
        connection
    )


    connection.close()

    return history



def get_prediction_statistics():

    connection=create_connection()
    cursor = connection.cursor()


    cursor.execute("""
    SELECT COUNT(*) AS total,
    SUM(CASE WHEN prediction='Abandon' THEN 1 ELSE 0 END) AS abandon,
    SUM(CASE WHEN prediction='Succès' THEN 1 ELSE 0 END) AS succes,
    AVG(probability) AS moyenne
    FROM prediction_history;
    """)


    statistics = cursor.fetchone()
    connection.close()

    return {
    "total_predictions": statistics[0],
    "dropout_predictions": statistics[1],
    "graduate_predictions": statistics[2],
    "average_probability": statistics[3]
}


def get_prediction_distribution():
    connection=create_connection()

    cursor=connection.cursor()

    cursor.execute("""SELECT
    prediction,
    COUNT(*) AS nombre
    FROM prediction_history
    GROUP BY prediction;
                   """)
    
    prediction_nombre=cursor.fetchall()

    return pd.DataFrame(columns=["prediction","effectif"],data=prediction_nombre)



def get_course_prediction_distribution():
    connection=create_connection()
    cursor=connection.cursor()

    cursor.execute("""
        SELECT
        course,
        prediction,
        COUNT(*) AS effectif
        FROM prediction_history
        GROUP BY course, prediction;
                   """)
    
    result=cursor.fetchall()
    connection.close()

    return pd.DataFrame(columns=["course","prediction","effectif"],data=result)


def get_prediction_timeline():
    connection=create_connection()
    cursor=connection.cursor()

    cursor.execute("""
                   SELECT
    SUBSTR(prediction_date,1,10) AS date,
    COUNT(*) AS effectif
    FROM prediction_history
    GROUP BY SUBSTR(prediction_date,1,10)
    ORDER BY date;
                   """)
    
    timeline=cursor.fetchall()
    connection.close()

    return pd.DataFrame(columns=["date","effectif"],data=timeline)



def get_last_predictions():

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            prediction_date,
            course,
            prediction,
            probability
        FROM prediction_history
        ORDER BY prediction_date DESC
        LIMIT 10;
    """)

    result = cursor.fetchall()

    connection.close()

    return pd.DataFrame(
        data=result,
        columns=[
            "prediction_date",
            "course",
            "prediction",
            "probability"
        ]
    )




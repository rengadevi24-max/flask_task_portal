import mysql.connector
from flask import current_app


def get_connection():
    return mysql.connector.connect(
        host=current_app.config["MYSQL_HOST"],
        port=current_app.config["MYSQL_PORT"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DATABASE"],
    )


def fetch_all(sql, values=()):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(sql, values)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()


def fetch_one(sql, values=()):
    rows = fetch_all(sql, values)
    return rows[0] if rows else None


def execute(sql, values=()):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(sql, values)
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()

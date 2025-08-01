import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",       # <-- kendi şifren neyse onu yaz
        database="depo_db"
    )

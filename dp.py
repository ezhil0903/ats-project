import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="ezhil1509",
        database="ats_system",
        cursorclass=pymysql.cursors.DictCursor
    )
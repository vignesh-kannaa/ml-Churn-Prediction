import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE'),
    'raise_on_warnings': True
}


class DBData:
    def get_finance_data():
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = "SELECT * FROM customers"
        cursor.execute(query)
        columns = cursor.column_names
        print(columns)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows, columns

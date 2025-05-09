import mysql.connector
from contextlib import contextmanager
from dotenv import load_dotenv
from urllib.parse import urlparse
import os
import ssl

load_dotenv()

from logging_setup import setup_logger


logger = setup_logger('db_helper')

# Get from Railway's Connect tab
DB_URL = "mysql://root:xHIIKhFjiYdcZEtbUqYAYRhfQjeHKOLw@tramway.proxy.rlwy.net:54974/railway"
# Parse the URL
url = urlparse(DB_URL)


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],  # removes the leading '/'
        port=url.port,
        ssl_disabled=True  # CRUCIAL FOR RAILWAY

    )

    if connection.is_connected():
        print("Connected successfully")
    else:
        print("Something went wrong")

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
        logger.info("Commited to DB")
        print("commited done")
    cursor.close()
    connection.close()
def fetch_all_data():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        return expenses

def fetch_expense_by_date(expense_date):
    logger.info(f"fetch_expense_for_date called with {expense_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense_for_date called with expense_date: {expense_date}, amount:{amount}, category: {category}, notes: {notes}")
    print(f"Inserting: {expense_date}, {amount}, {category}, {notes}")

    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date,amount,category,notes) VALUES (%s, %s, %s, %s)",(expense_date,amount,category,notes))

def delete_expense_by_date(expense_date):
    logger.info(f"delete_expense_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary_for starting date: {start_date} to end date: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category,SUM(amount) as total
                        FROM expenses WHERE expense_date
                        BETWEEN %s and %s
                        GROUP BY category;''', (start_date,end_date))
        data = cursor.fetchall()
        return data

def fetch_expense_summary_month(start_date,end_date):
    logger.info(f"fetch_expense_summary from starting month: {start_date} to end date: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT 
    DATE_FORMAT(expense_date, '%M') AS month,
    SUM(amount) AS total_amount
FROM expenses
WHERE expense_date BETWEEN %s AND %s
GROUP BY DATE_FORMAT(expense_date, '%M')
ORDER BY MIN(expense_date);  
''', (start_date, end_date))
        data = cursor.fetchall()
        return data


if __name__ == "__main__":

    insert_expense("2024-07-12",500,"food","birthday cake")
    # expense = fetch_expense_by_date("2024-07-12")
    # delete_expense_by_date("2024-07-12")
     # print(fetch_expense_summary('2024-01-01' , '2024-08-01'))
    # expense = fetch_expense_by_date("2024-08-15")
    # print(expense)
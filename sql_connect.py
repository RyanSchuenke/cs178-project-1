# Ryan Schuenke

import pymysql
from flask import flash, redirect, url_for, request
import credentials as creds

def get_connection():
    """
    Create a new database connection.
    """
    return pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.password,
        database=creds.db,
        )

def execute_query(query, args):
    """
    execute a sql query and return the result, redirct to the same page if error occurs.
    query (string): sql query to be executed
    args (dict): dictionary of arguments to be inserted into sql statement
    return rows: array of rows from query output
    """
    try:
        connection = get_connection()
        cur = connection.cursor()
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.close()
        connection.close()
    except Exception as e:
        flash(str(e), 'danger')
        return []
    return rows

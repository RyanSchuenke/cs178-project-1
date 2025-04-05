import pymysql
from flask import flash, redirect, url_for, request
import sql_credentials as creds

def get_connection():
    """Create a new database connection."""
    return pymysql.connect(
        host= creds.host,
        user= creds.user, 
        password = creds.password,
        db=creds.db,
        )

def execute_query(query, args=()):
    """execute a sql query and return the result, redirct to the same page if error occurs."""
    try:
        connection = get_connection()
        cur = connection.cursor()
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.commit()
        cur.close()
        connection.close()
    except Exception as e:
        flash({"error": str(e)}, 'error')
        return redirect(request.url)
    return rows
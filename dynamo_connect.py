# name: Ryan Schuenke
# date: 3/4/2025
# description: Implementation of CRUD operations with DynamoDB database CS178 Lab #9
# proposed score: 5 (out of 5)

import boto3
import botocore
from flask import flash
import sql_credentials

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(sql_credentials.dynamoDB_table)

def create_user(username, password):
    """Create new user in table"""
    table.put_item( 
        Item={
            'Username': username,
            'Password': password,
        }
    )


def update_password(username, password, new_password):
    """update password for user"""
    try: 
        table.update_item(
            Key = {
            'Username': username,
            'Password': password,
            }, 
            UpdateExpression = "SET Password = :r", ExpressionAttributeValues = {':r': new_password}
        )
        flash("password updated", "success")
        return True
    except botocore.exceptions.ClientError:
        flash("Movie not in database", "error")
        return False


def delete_user(user_id):
    """delete user from database"""
    try:
        table.delete_item(
            Key = {"userID": user_id}
        )
        flash("user deleted", "success")
        return True
    except botocore.exceptions.ClientError:
        flash("user not in database", "error")
        return False


def query_login(username, password):
    """query for username and password"""
    try:
        response = table.get_item(
            Key = {
                "Username": username, 
                "Password": password
            }
        )
        user = response.get("Item")
        if user == None:
            flash("Username/Password is incorrect", "error")
            return -1
        else:
            return user["userID"]
    except botocore.exceptions.ClientError:
        flash("Username/Password is incorrect", error) 
        return -1

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a new movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to Query a movie's average ratings")
    print("Press X: to EXIT application")
    print("----------------------------")


def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print('Not a valid option. Try again.')
main()

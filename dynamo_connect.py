# Ryan Schuenke

import boto3
import botocore
from flask import flash
import credentials

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(credentials.dynamoDB_table)

def create_user(username, password):
    """
    Create new user in table
    username (string): specified username for account
    password (string): specified password for account
    returns boolean: success or failure of adding record to database
    """
    try: 
        table.put_item( 
            Item={
                'username': username,
                'password': password,
            }
        )
        return True
    except botocore.exceptions.ClientError:
        return False


def update_password(username, new_password):
    """
    update password for user
    username (string): specified username for account record to update
    new_password (string): specified new password to update to for the given username
    return boolean: success or failure of updating password for account
    """
    try: 
        table.update_item(
            Key = {
            'username': username
            }, 
            UpdateExpression = "SET password = :r", ExpressionAttributeValues = {':r': new_password}
        )
        return True
    except botocore.exceptions.ClientError:
        return False


def delete_user(username):
    """
    delete user from database
    username (string): username (key) of record to be deleted
    return boolean: success or failure of deletion
    """
    try:
        table.delete_item(
            Key = {"username": username}
        )
        return True
    except botocore.exceptions.ClientError:
        return False

def query_username(username):
    """
    query for username and password, returns user
    username (string): username of record to return
    return user (dict): dictionary record of user, None if no matching username in database
    """
    try:
        response = table.get_item(
            Key = {
                "username": username
            }
        )
        user = response.get("Item")
        return user
    except botocore.exceptions.ClientError:
        return None
    
def query_login(username, password):
    """
    query for username and password
    username (string): username of record to search for
    password (string): password of account being searched for
    return boolean: success or failure to match username and password to a record in the database
    """
    try:
        user = query_username(username)
        if user == None:
            return False
        else:
            return user['password'] == password
    except Exception as e:
        return False



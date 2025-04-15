import boto3
import botocore
from flask import flash
import credentials

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(credentials.dynamoDB_table)

def create_user(username, password):
    """Create new user in table"""
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
    """update password for user"""
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
    """delete user from database"""
    try:
        table.delete_item(
            Key = {"username": username}
        )
        return True
    except botocore.exceptions.ClientError:
        return False


def query_login(username, password):
    """query for username and password"""
    try:
        user = query_username(username)
        if user == None:
            return False
        else:
            return user['password'] == password
    except Exception as e:
        return False

def query_username(username):
    """query for username and password, returns user"""
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

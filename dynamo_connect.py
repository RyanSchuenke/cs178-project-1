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
    try: 
        table.put_item( 
            Item={
                'username': username,
                'password': password,
            }
        )
        return True
    except botocore.exceptions.ClientError:
        flash("username taken", "danger")
        return False


def update_password(username, password, new_password):
    """update password for user"""
    try: 
        table.update_item(
            Key = {
            'username': username,
            'password': password,
            }, 
            UpdateExpression = "SET password = :r", ExpressionAttributeValues = {':r': new_password}
        )
        flash("password updated", "success")
        return True
    except botocore.exceptions.ClientError:
        flash("user not in database", "danger")
        return False


def delete_user(username):
    """delete user from database"""
    try:
        table.delete_item(
            Key = {"username": username}
        )
        flash("user deleted", "success")
        return True
    except botocore.exceptions.ClientError:
        flash("user not in database", "danger")
        return False


def query_login(username, password):
    """query for username and password"""
    try:
        response = table.get_item(
            Key = {
                "username": username
            }
        )
        user = response.get("Item")
        if user == None:
            return False
        else:
            return user['password'] == password
    except Exception as e:
        return False

def query_username(username):
    """query for username and password"""
    try:
        response = table.get_item(
            Key = {
                "username": username
            }
        )
        user = response.get("Item")
        if user == None:
            return False
        else:
            return True
    except botocore.exceptions.ClientError:
        flash("Username/Password is incorrect", "danger") 
        return False

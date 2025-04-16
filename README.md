# cs178-project-1
## Cloud and Database Systems Project 1
Ryan Schuenke

### Project Description
This project implements a user management system and a game of "Higher or Lower" for the population of cities from the world.sql database.  The user management system has CRUD implementation of a DynamoDB NoSQL database to manage user accounts and access.  The "Higher or Lower" game asks users to specify a country to use cities from, then provides two cities which the user will select the city with a higher population and told if they were correct on submission.

### Technologies
#### AWS
This project is running on an AWS EC2 instance.  It is also connected with a MySQL database hosted on AWS RDS and a NoSQL database, Amazon's Dynamo DB.
#### Flask
This project is implemented in Flask using both python and HTML.  Database connections are made using pymysql for the MySQL database and boto3 for DynamoDB.

### Setup and run instructions
1. Clone the repository with `git clone https://github.com/RyanSchuenke/cs178-project-1`
2. install the required dependencies: `Flask`, `boto3`, `botocore`, `pymysql`
3. Connect to an AWS account using boto3 and prepare:
    1. Load the world.py database onto a mysql instance
    2. create a DynamoDB database
    3. create a `credentials.py` file with the information to connect to the two databases
4. run the app with `python3 app.py`

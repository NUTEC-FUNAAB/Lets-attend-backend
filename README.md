# Let's Attend

### Introduction
Let's attend is an event management system that allows users to create, manage and join events.

### Features
* Create events
* Invite users to events
* Accept or decline invitations
* View events that you have created
* View events that you have accepted
* View upcoming events
* Event notifications and reminders

### Installation (Linux)
Create the database with the config/regen.sql file. Ensure that your password
corresponds to the sql password requirements. `you need to have MySQL installed for the db`

regen.sql
```mysql
DROP DATABASE IF EXISTS attend;
DROP DATABASE IF EXISTS attend_test;
CREATE DATABASE attend;
CREATE DATABASE attend_test;
CREATE USER IF NOT EXISTS 'attend_dev'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD';
GRANT ALL PRIVILEGES ON attend.* TO 'attend_dev'@'localhost';
GRANT ALL PRIVILEGES ON attend_test.* TO 'attend_dev'@'localhost';
FLUSH PRIVILEGES;
```

Then set the environment variables in the .env file

`vi .env`
```bash
DB_ATTEND_MODE = dev or test
DB_ATTEND_HOST = localhost
DB_ATTEND_USER = attend_dev
DB_ATTEND_PASSWORD = YOUR_PASSWORD
DB_ATTEND_NAME = attend
DB_ATTEND_TEST_NAME = attend_test
SECRET_KEY = YOUR_SECRET__KEY
ATTEND_HOST = 0.0.0.0
ATTEND_PORT = PORT
```

Install the dependencies
```bash
cd docs/
pip install -r requirements.txt
cd ..
```

Run the flask application using gunicorn or flask
```bash
cd api/
flask run
# OR
gunicorn --access-logfile access.log --error-logfile error.log --bind 0.0.0.0:5000 api.app:app
```

### Installation (Windows)
Null

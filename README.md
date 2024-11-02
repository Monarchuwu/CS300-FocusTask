# CS300-FocusTask

## Description

## Installation
### 1. Clone the repository
```bash 
git clone https://github.com/Monarchuwu/CS300-FocusTask.git
```
### 2. Install Docker
Install [here](https://docs.docker.com/get-docker/)

### 3. Create a .env file
Create a .env file in the root directory of the project and add the following:
```bash
DATABASE_NAME=focus_task_db
DATABASE_USER=focus_task_admin
DATABASE_PASSWORD=<password>
DATABASE_PORT=5432  
DATABASE_HOST=focus-task-postgres
DJANGO_ENV=development
```
Set the DATABASE_PASSWORD to a password of your choice.

### 4. Build and run
Go to the root directory of the project and run the following commands:
```bash
docker-compose build
docker-compose up -d
```

To lint the code:
```bash
flake8
```


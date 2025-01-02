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
Create a `.env` file in the root directory of the project and add the following:
```bash
DATABASE_NAME=focus_task_db
DATABASE_USER=focus_task_admin
DATABASE_PASSWORD=<your_password>
DATABASE_PORT=5432  
DATABASE_HOST=db
DATABASE_ENGINE=django.db.backends.postgresql
DJANGO_ENV=development
SECRET_KEY=<your_secret_key>
```
Set the DATABASE_PASSWORD to a password of your choice. Set the SECRET_KEY to a secret key of your choice.
If you're in our team, you can get the file from this [link](https://drive.google.com/file/d/1Powqoi92qATvAI0RD-x41aYPqAz1yOiJ/view?usp=drive_link).

Add another `.env` in `frontend` folder with following constants:
```bash
REACT_APP_API_URL=http://localhost:8000/todolist/api 
```

Replace the `REACT_APP_API_URL` to match your backend API URL.

### 4. Build and run
Go to the root directory of the project and run the following commands:
```bash
docker-compose up --build
```

#### Backend
The backend is ready when you see the following message:
```bash
focus_task_backend   | Watching for file changes with StatReloader
```

Migrate the database:
```bash
docker-compose exec backend python manage.py migrate
```

To create a superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

#### Frontend
If `frontend/node_modules` is not installed in the frontend container, run the following command in the `frontend` directory:
```bash
npm install
```

To start the frontend, run the following command in the `frontend` directory:
```bash
npm start
```

The frontend is ready when you see the following message:
```
You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://172.19.0.2:3000

Note that the development build is not optimized.
To create a production build, use npm run build.

webpack compiled successfully
``` 

### 5. Install the Website Blocking extension

To install the Chrome Extension, follow the instructions in [this repo](https://github.com/ldn694/WebsiteBlocking).

## Development

If your run the app in the browser under the ip given after npm run start as "On Your Network", then if you make changes in `frontend/src/App.js` this should automaticly reload the page when saved.

To execute commands in the backend container:
```bash
docker-compose exec backend <command>
```

To rebuild the containers:
```bash
docker-compose down --volumes
docker-compose up --build
```

To lint the code:
```bash
flake8
```

To test the code using pytest:
```bash
docker-compose exec backend pytest
```



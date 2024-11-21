FROM python:3.11

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get upgrade -y

COPY /backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.11-slim

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

COPY requirements.txt /app/

# install dependencies
RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5000
CMD ["flask", "run"]

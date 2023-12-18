FROM python:3.11-slim

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=/app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

COPY /app/requirements.txt /app/

# install dependencies
RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /app/requirements.txt

# copy files and directories into the container
COPY training_play /app/training_play/
COPY models /app/models/

COPY app /app

EXPOSE 5000
CMD ["flask", "run"]
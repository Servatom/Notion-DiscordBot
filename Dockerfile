# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN apt-get update
RUN apt-get install python-dev -y
RUN apt-get install build-essential -y
RUN python -m pip install -r requirements.txt

RUN mkdir /Bot
WORKDIR /Bot
RUN mkdir database
COPY ./Bot /Bot

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser
RUN chown -R appuser /Bot
RUN chown -R appuser /Bot/database
USER root


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "bot.py"]

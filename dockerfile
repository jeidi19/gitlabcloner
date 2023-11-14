FROM python:latest
WORKDIR /code

COPY requirements.txt requirements.txt
RUN apt-get install git && pip install --upgrade pip && git config --global user.name "xxxxxx" && git config --global user.email "xxxx@xxxx.com"
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python", "main.py" ]
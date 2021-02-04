FROM python:3.8

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
COPY ./config ./config
COPY ./data ./data
RUN ["mkdir", "./tmp"]

WORKDIR /app/src
CMD ["python", "./main.py"]

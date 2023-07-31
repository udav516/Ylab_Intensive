FROM python:3.10-slim

RUN mkdir /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app

EXPOSE 8000

CMD ["python", "main.py"]
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn --worker-class gevent -w 1 --timeout 120 --bind 0.0.0.0:$PORT app:app
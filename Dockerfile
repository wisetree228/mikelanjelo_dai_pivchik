FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
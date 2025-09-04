FROM python:3.13

WORKDIR /app

COPY requirements.txt .

# COPY .env .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "main.py"]
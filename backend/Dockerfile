FROM python:3.12-alpine

WORKDIR /app

# Zainstaluj zależności systemowe dla psycopg2
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
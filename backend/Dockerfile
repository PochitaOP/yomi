FROM python:latest

WORKDIR /usr/src/app

RUN pip install "fastapi[all]" "python-jose[cryptography]" psycopg2 sqlalchemy passlib

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

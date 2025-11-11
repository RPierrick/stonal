FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PYTHONPATH=.

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]

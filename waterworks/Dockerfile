FROM python:3.12.12

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /app/

# Default open port
EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

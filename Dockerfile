FROM python:3.8.5

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /requirements.txt
COPY . /code
CMD gunicorn yamdb_final.wsgi:application --bind 0.0.0.0:8000
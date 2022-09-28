FROM python:3.10

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app
COPY ./scrapers ./scrapers
COPY scrapy.cfg .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

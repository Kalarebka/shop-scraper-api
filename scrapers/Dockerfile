FROM python:3.10

RUN useradd --create-home celery
USER celery
ENV PATH="/home/celery/.local/bin:${PATH}"

WORKDIR /home/celery/scrapers
ADD requirements_scraping.txt .
RUN pip install -r requirements_scraping.txt

COPY ./scrapers .
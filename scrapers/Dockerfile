FROM python:3.9

WORKDIR /scrapers

COPY requirements_scraping.txt .
RUN pip install --no-cache-dir --upgrade -r requirements_scraping.txt

COPY ./scrapers ./scrapers
COPY ./scrapy.cfg .

CMD ["scrapyrt"]
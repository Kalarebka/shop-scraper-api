FROM python:3.9

RUN mkdir -p /scrapyrt/project/scrapers
RUN mkdir -p /var/log/scrapyrt

COPY requirements_scraping.txt .
RUN pip install --no-cache-dir --upgrade -r requirements_scraping.txt


COPY scrapy.cfg /scrapyrt/project
COPY ./scrapers scrapyrt/project/scrapers

WORKDIR /scrapyrt/project
EXPOSE 9080

CMD ["scrapyrt", "-i", "0.0.0.0"]
import httpx  # should use async request package
import json
import requests

SPIDERS = ["matras", "bonito", "tantis"]


def request_live_query(query):
    results = []
    for spider in SPIDERS:
        crawl_args = json.dumps({"query": query})
        parameters = {
            "spider_name": spider,
            "start_requests": True,
            "crawl_args": crawl_args,
        }
        response = requests.get(f"http://scrapers:9080/crawl.json", params=parameters)
        results.append(response.json())
    return results

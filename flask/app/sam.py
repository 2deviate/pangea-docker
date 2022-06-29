"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: SamKnows Web Scraper.  Scrapes exchange info from website
Notifyees: craig@2deviate.com
Category: None
"""
import logging
import urllib3
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class SamKnows(object):

    url = None
    headers = None

    def __init__(self):
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }

    def request(self, method, query=None, url=None, scraper=None):
        try:
            http = urllib3.PoolManager()
            if method == "POST":
                payload = {"exchange_search[exchange]": query}
                encoded = urllib3.request.urlencode(payload)
                body = encoded.encode("ascii")
                request = http.request(
                    method=method, url=url, body=body, headers=self.headers
                )
            elif method == "GET":
                request = http.request(method=method, url=url, headers=self.headers)
            response = request.data
            soup = BeautifulSoup(response, "html.parser")
            return scraper(soup)
        except Exception as err:
            logger.error(err, exc_info=err)
            raise

    @staticmethod
    def scrape_info(soup):
        data = []
        table = soup.find("table", {"id": "exchange-list-table"})
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

    @staticmethod
    def scrape_exchange(soup):
        data = {}
        div = soup.find("div", {"class": "item-content"})
        rows = div.find_all("tr")
        for row in rows:
            elem = row.find("th")
            if elem and hasattr(elem, "text"):
                key = elem.text[:-1].strip()
                elem = row.find("td")
                if elem and hasattr(elem, "text"):
                    value = elem.text.strip()
                if key:
                    data.update({key: value})
        return data


sam = SamKnows()

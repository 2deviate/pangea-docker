"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Generic Web Scraper.  Scrapes info from website
Notifyees: craig@2deviate.com
Category: None
"""
import logging
import urllib3
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WebScraper(object):

    def scrape(self, method, url=None, headers=None, body=None, func=None, **attrs):
        try:
            http = urllib3.PoolManager()
            if method == "POST":
                payload = payload
                encoded = urllib3.request.urlencode(payload)
                body = encoded.encode("ascii")
                request = http.request(
                    method=method, url=url, body=body, headers=headers
                )
            elif method == "GET":
                request = http.request(method=method, url=url, headers=headers)
            response = request.data
            soup = BeautifulSoup(response, "html.parser")
            return func(soup, **attrs)
        except Exception as err:
            logger.error(err, exc_info=err)
            raise

    @staticmethod
    def scrape_table(soup, **attrs):        
        table = soup.find("table", attrs)
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            yield [ele for ele in cols if ele]

    @staticmethod
    def scrape_hrefs(soup, **attrs):        
        links = soup.findAll("a", attrs)        
        for link in links:
            yield link        

scraper = WebScraper()
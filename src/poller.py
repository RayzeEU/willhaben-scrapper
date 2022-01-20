import logging

import lxml.html
import requests

from datetime import datetime
from datetime import timedelta

from src.product.product_collector import ProductCollector
from src.product.product import Product


class PagePoller:

    FIVE_MINUTE_DELTA = timedelta(minutes=5)
    ONE_HOUR_DELTA = timedelta(hours=1)

    def __init__(self, show_non_mapping, config):
        self._show_non_mapping = show_non_mapping
        self._config = config

        logging.info("%s cards are usable" % len(self._config["usable_cards"]))

        self._product_collector = ProductCollector(config)

    def check_website(self):
        self.__scan_for_products_and_add_to()

        self.__check_new_cards()

        self._product_collector.print_result_to_console(self._show_non_mapping)
        self._product_collector.send_result_to_discord()

    def __scan_for_products_and_add_to(self):
        logging.info("opening page ...")

        # According to www.willhaben.at/robots.txt the following user agent has all rights.
        html = requests.get(self._config["url"], headers={'User-Agent': 'Mediapartners-Google'}).text

        parsed_html = lxml.html.fromstring(html)

        for div in parsed_html.cssselect('#skip-to-resultlist > div > div:nth-child(1)'):
            self.__parse_main_div_for_one_card(div)

    def __parse_main_div_for_one_card(self, div):
        div_id = div.get('id')
        if div_id:
            for inner_div in div.cssselect('a:nth-child(1)'):
                card_name = ''
                card_price = ''
                card_timestamp = ''

                card_href = inner_div.get('href')

                for header in inner_div.cssselect('div:nth-child(2) > span:nth-child(1) > h3:nth-child(1)'):
                    card_name = header.text

                for time in inner_div.cssselect('div:nth-child(2) > div:nth-child(3) > p:nth-child(1)'):
                    card_timestamp = time.text

                for card_price_element in inner_div.cssselect(
                        'div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'):
                    card_price = card_price_element.text

                self._product_collector.add_new_product(
                    Product(card_name, card_price, card_href, card_timestamp))

    def __check_new_cards(self):
        timestamp_to_check = datetime.now() - self.FIVE_MINUTE_DELTA + self.ONE_HOUR_DELTA

        self._product_collector.mapped_products_after_timestamp(timestamp_to_check)

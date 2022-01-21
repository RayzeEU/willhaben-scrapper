import logging
from typing import Optional

import lxml.html
import requests

from datetime import datetime
from datetime import timedelta

from src.product.product_collector import ProductCollector
from src.translator.currency_translator import CurrencyTranslator
from src.translator.timestamp_translator import TimestampTranslator


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
            timestamp_start = datetime.now()
            for inner_div in div.cssselect('a:nth-child(1)'):
                card_href = self.__card_href(inner_div)
                card_name = self.__card_name(inner_div)
                card_timestamp = self.__card_timestamp(inner_div)
                card_price = self.__card_price(inner_div)

                if not card_name or not card_timestamp or not card_price:
                    break

                self._product_collector.add_new_product(card_name, card_price, card_href, card_timestamp, timestamp_start)

    @staticmethod
    def __card_href(inner_div):
        return 'https://www.willhaben.at' + inner_div.get('href')

    @staticmethod
    def __card_name(inner_div) -> Optional[str]:
        for header in inner_div.cssselect('div:nth-child(2) > span:nth-child(1) > h3:nth-child(1)'):
            return header.text
        return None

    @staticmethod
    def __card_timestamp(inner_div) -> Optional[datetime]:
        for time in inner_div.cssselect('div:nth-child(2) > div:nth-child(3) > p:nth-child(1)'):
            return TimestampTranslator.text_to_timestamp_or_max_if_not_today(time.text)
        return None

    @staticmethod
    def __card_price(inner_div) -> Optional[int]:
        for card_price_element in inner_div.cssselect(
                'div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'):
            return CurrencyTranslator.text_to_int(card_price_element.text)
        return None

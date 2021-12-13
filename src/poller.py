import logging
import os

import lxml.html
import requests

from datetime import datetime
from datetime import timedelta

from discord import Webhook, RequestsWebhookAdapter

from src.product.product_collector import ProductCollector
from src.product.product import Product


class PagePoller:

    def __init__(self, show_non_mapping, config):
        self.show_non_mapping = show_non_mapping
        self.config = config

        logging.info("%s cards are usable" % len(self.config["usable_cards"]))

        self.product_collector = ProductCollector(config)

    def check_website(self):
        self.scan_for_products_and_add_to()

        self.check_new_cards()

        self.product_collector.print_result_to_console(self.show_non_mapping)
        self.product_collector.send_result_to_discord()

    def scan_for_products_and_add_to(self):
        logging.info("opening page ...")

        # According to www.willhaben.at/robots.txt the following user agent has all rights.
        html = requests.get(self.config["url"], headers={'User-Agent': 'Mediapartners-Google'}).text

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

                self.product_collector.add_new_product(
                    Product(card_name, card_price, card_href, card_timestamp))

    def check_new_cards(self):
        check_timestamp = datetime.now()
        minus_five_minutes = timedelta(minutes=5)
        plus_one_hour = timedelta(hours=1)

        webhook = Webhook.from_url(os.environ["Discord_Bot_Status"], adapter=RequestsWebhookAdapter())
        webhook.send((datetime.now() - minus_five_minutes + plus_one_hour).strftime("%Y-%m-%d %H:%M:%S"))

        self.product_collector.mapped_products_after_timestamp(check_timestamp - minus_five_minutes + plus_one_hour)

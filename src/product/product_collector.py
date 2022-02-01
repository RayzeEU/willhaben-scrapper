import logging
import os
from datetime import datetime

from typing import List

from discord import Webhook, RequestsWebhookAdapter
from src.background_colors import BackgroundColors
from src.product.product import Product

TEXT_RUNNING = "Running 1.0.1"


class ProductCollector:

    def __init__(self, config):
        self.products = []
        self.usable_cards = config["usable_cards"]
        self.webhook_latest_cards = Webhook.from_url(os.environ["Discord_Latest_Cards"], adapter=RequestsWebhookAdapter())
        self.webhook_bot_status = Webhook.from_url(os.environ["Discord_Bot_Status"], adapter=RequestsWebhookAdapter())

    def add_new_product(self, card_name: str, card_price: int, card_href: str, card_timestamp: datetime, timestamp_start: datetime):
        found_usable_card = next(filter(lambda usable_card: usable_card["name"].lower() in card_name.lower(), self.usable_cards), None)

        short_name = ""
        profit_per_month = 0

        if found_usable_card:
            short_name = found_usable_card["name"]
            profit_per_month = float(found_usable_card["monthly_income"])

        product = Product(card_name, short_name, card_price, profit_per_month, card_href, found_usable_card is not None, card_timestamp >= timestamp_start)
        self.products.append(product)

    def products_size(self):
        return len(self.products)

    def print_result_to_console(self, show_non_mapping):
        logging.info(BackgroundColors.OKCYAN + "Total products found: %s" % self.products_size() + BackgroundColors.ENDC)

        if show_non_mapping:
            self.__print_non_mapped_products()
        self.__print_mapped_products()

    def __print_non_mapped_products(self):
        products_not_mapped = self.__list_of_not_mapped_products_order_by_roi_asc()
        logging.info(BackgroundColors.WARNING + "Total products not matched: %s" % len(products_not_mapped) + BackgroundColors.ENDC)
        for product in products_not_mapped:
            logging.info(product.display_string_colored())

    def __list_of_not_mapped_products_order_by_roi_asc(self) -> List[Product]:
        return self.__list_of_products_by_filter_ordered_by_roi_asc(lambda x: not x.is_mapped())

    def __list_of_products_by_filter_ordered_by_roi_asc(self, lambda_function):
        filtered_list = list(filter(lambda_function, self.products))
        filtered_list.sort(key=lambda p: p.roi(), reverse=True)
        return filtered_list

    def __print_mapped_products(self):
        products_mapped = self.__list_of_mapped_products_order_by_roi_asc()
        logging.info(BackgroundColors.OKCYAN + "Total products mapped: %s" % len(products_mapped) + BackgroundColors.ENDC)
        for product in products_mapped:
            logging.info(product.display_string_colored())

    def __list_of_mapped_products_order_by_roi_asc(self) -> List[Product]:
        return self.__list_of_products_by_filter_ordered_by_roi_asc(lambda x: x.is_mapped())

    def send_result_to_discord(self):
        message = self.__build_discord_message()

        self.webhook_bot_status.send(TEXT_RUNNING)
        if message:
            self.webhook_latest_cards.send(message)

    def __build_discord_message(self):
        message = ""
        for product in self.__list_of_relevant_products_order_by_roi_asc():
            message = self.__add_line_break_if_message_not_empty(message)

            message = message + product.display_string_uncolored()
            if len(message) > 2000:
                message = message[:2000]
                break

        return message

    def __list_of_relevant_products_order_by_roi_asc(self) -> List[Product]:
        return self.__list_of_products_by_filter_ordered_by_roi_asc(lambda x: x.relevant_for_discord())

    @staticmethod
    def __add_line_break_if_message_not_empty(message):
        if message != "":
            message = message + "\r\n"
        return message

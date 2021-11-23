from typing import List

from discord import Webhook, RequestsWebhookAdapter

from src.background_colors import BackgroundColors
from src.product.product import Product

NOT_MAPPED = "Not mapped"


class ProductCollector:

    def __init__(self, config, private_config):
        self.products = []
        self.usable_cards = config["usable_cards"]
        self.blacklist_words = config["blacklist_words"]
        self.blacklist = config["blacklist"]
        self.webhook_latest_cards = private_config.get('Webhooks', 'latest-cards')

    def clear_collector(self):
        self.products = []

    def add_new_product(self, product):
        product_name_lowercase = product.name.replace(' ', '').lower()

        if product.name not in self.blacklist_words \
                and product.name not in self.blacklist:
            for usable_card in self.usable_cards:
                if usable_card["name"].lower() in product_name_lowercase:
                    product.set_product_properties(usable_card["name"], float(usable_card["monthly_income"]))
                    product.mark_as_mapped()
                    break
        self.products.append(product)

    def mapped_products_after_timestamp(self, timestamp):
        for product in self.products:
            if product.timestamp < timestamp:
                break
            product.mark_as_time_relevant()

    def products_size(self):
        return len(self.products)

    def print_result_to_console(self, show_non_mapping):
        print(BackgroundColors.OKCYAN + "Total products found: %s" % self.products_size() + BackgroundColors.ENDC)

        if show_non_mapping:
            self.__print_non_mapped_products()
        self.__print_mapped_products()

    def __print_non_mapped_products(self):
        products_not_mapped = self.__list_of_not_mapped_products_order_by_roi_asc()
        print(BackgroundColors.WARNING + "Total products not matched: %s" % len(products_not_mapped) + BackgroundColors.ENDC)
        for product in products_not_mapped:
            print(product.display_string_colored())

    def __list_of_not_mapped_products_order_by_roi_asc(self) -> List[Product]:
        return self.__list_of_products_by_filter_ordered_by_roi_asc(lambda x: not x.mapped, True)

    def __list_of_products_by_filter_ordered_by_roi_asc(self, lambda_function, asc):
        filtered_list = list(filter(lambda_function, self.products))
        filtered_list.sort(key=lambda p: p.roi, reverse=asc)
        return filtered_list

    def __print_mapped_products(self):
        products_mapped = self.__list_of_mapped_products_order_by_roi_asc()
        print(BackgroundColors.OKCYAN + "Total products mapped: %s" % len(products_mapped) + BackgroundColors.ENDC)
        for product in products_mapped:
            print(product.display_string_colored())

    def __list_of_mapped_products_order_by_roi_asc(self) -> List[Product]:
        return self.__list_of_products_by_filter_ordered_by_roi_asc(lambda x: x.mapped, True)

    def print_result_to_discord(self):
        message = self.__build_discord_message()
        if message != "":
            self.__send_message_to_discord(message)

    def __build_discord_message(self):
        message = ""
        for product in self.__list_of_relevant_products_order_by_roi_desc():
            message = self.__add_line_break_if_message_not_empty(message)

            message = message + product.display_string_uncolored()
            if len(message) > 1900:
                break

        return message

    def __list_of_relevant_products_order_by_roi_desc(self) -> List[Product]:
        return self.__list_of_products_by_filter_ordered_by_roi_asc(lambda x: x.time_relevant and x.mapped, False)

    def __send_message_to_discord(self, message):
        webhook = Webhook.from_url(self.webhook_latest_cards, adapter=RequestsWebhookAdapter())
        webhook.send(message)

    @staticmethod
    def __add_line_break_if_message_not_empty(message):
        if message != "":
            message = message + "\r\n"
        return message

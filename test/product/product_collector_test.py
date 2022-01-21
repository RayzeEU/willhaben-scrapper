import os
from datetime import datetime

from unittest import mock

from src.product.product_collector import ProductCollector

TEST_USABLE_CARD_NAME = "Karte 1660"
TEST_USABLE_SHORT_CARD_NAME = "1660"
TEST_UNUSABLE_CARD_NAME = "Karte 1060"
TEST_UNUSABLE_SHORT_CARD_NAME = "16XX"
TEST_CARD_PRICE = 100
TEST_LINK = "/link"
TEST_DATETIME_NOW = datetime.now()

_config = {
    'usable_cards': [{'name': 'HX90', 'monthly_income': 139.9, 'watt': 250, 'hash_power': 98},
                     {'name': '1660', 'monthly_income': 34.36, 'watt': 60, 'hash_power': 24}]}


def test__given_config__when_constructor__then_instance_with_right_values():
    product_collector = __test_product_collector()

    assert product_collector.products == []
    assert product_collector.usable_cards == _config["usable_cards"]
    assert product_collector.webhook_latest_cards is not None
    assert product_collector.webhook_bot_status is not None


def test__given_product_not_in_usable_cards__when_add_new_product__then_add_unmapped_card_to_products():
    product_collector = __test_product_collector()

    __add_product(product_collector, TEST_UNUSABLE_CARD_NAME)

    assert len(product_collector.products) == 1
    assert product_collector.products[0].is_mapped() is False


def __add_product(product_collector: ProductCollector, card_name: str = TEST_USABLE_CARD_NAME):
    product_collector.add_new_product(card_name, TEST_CARD_PRICE, TEST_LINK, TEST_DATETIME_NOW, TEST_DATETIME_NOW)


def test__given_usable_product__when_add_new_product__then_add_mapped_card_to_products():
    product_collector = __test_product_collector()

    __add_product(product_collector, TEST_USABLE_CARD_NAME)

    assert len(product_collector.products) == 1
    mapped_product = product_collector.products[0]
    assert mapped_product.is_mapped() is True
    assert mapped_product._short_name == TEST_USABLE_SHORT_CARD_NAME
    assert mapped_product.roi() == (TEST_CARD_PRICE / 34.36)


def test__given_two_cards__when_products_size__then_2():
    product_collector = __test_product_collector()
    __add_product(product_collector, TEST_USABLE_SHORT_CARD_NAME)
    __add_product(product_collector, TEST_USABLE_SHORT_CARD_NAME)

    assert product_collector.products_size() == 2


@mock.patch("src.product.product_collector.logging", return_value=None, autospec=True)
def test__given_two_cards__when_print_result_to_console__then_right_console_output(logging_mock):
    product_collector = __test_product_collector()
    __add_product(product_collector, TEST_USABLE_SHORT_CARD_NAME)
    __add_product(product_collector, TEST_UNUSABLE_SHORT_CARD_NAME)

    product_collector.print_result_to_console(True)

    assert len(logging_mock.method_calls) == 5


@mock.patch("src.product.product_collector.logging", return_value=None, autospec=True)
def test__given_two_cards_print_non_mapped_false__when_print_result_to_console__then_right_console_output(logging_mock):
    product_collector = __test_product_collector()
    __add_product(product_collector, TEST_USABLE_SHORT_CARD_NAME)
    __add_product(product_collector, TEST_UNUSABLE_SHORT_CARD_NAME)

    product_collector.print_result_to_console(False)

    assert len(logging_mock.method_calls) == 3


def test__given_two_cards__when_send_result_to_discord__then_right_discord_message():
    product_collector = __test_product_collector()
    __add_product(product_collector)
    __add_product(product_collector)

    product_collector.send_result_to_discord()

    # Webhook Mock for latest_cards and bot_status is the same, so method_calls are the sum count for both variables
    assert len(product_collector.webhook_latest_cards.method_calls) == 2


def test__given_cards_where_message_is_over_1999_chars__when_send_result_to_discord__then_message_length_is_maximum_1999():
    product_collector = __test_product_collector()
    for _ in range(100):
        __add_product(product_collector)

    product_collector.send_result_to_discord()

    # Webhook Mock for latest_cards and bot_status is the same, so method_calls are the sum count for both variables
    assert len(product_collector.webhook_latest_cards.method_calls) == 2


@mock.patch("src.product.product_collector.Webhook", return_value=None, autospec=True)
def __test_product_collector(_webhook_mock) -> ProductCollector:
    os.environ["Discord_Latest_Cards"] = "Webhook latest cards"
    os.environ["Discord_Bot_Status"] = "Webhook bot status"

    return ProductCollector(_config)

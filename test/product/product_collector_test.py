import os
from datetime import datetime
from unittest import mock

from src.product.product import Product
from src.product.product_collector import ProductCollector
from src.translator.timestamp_translator import TimestampTranslator

_config = {
    'blacklist': ['Blacklist 1', 'Blacklist 2'],
    'blacklist_words': ['defekt', 'kaputt'],
    'usable_cards': [{'name': 'HX90', 'monthly_income': 139.9, 'watt': 250, 'hash_power': 98},
                     {'name': '1660', 'monthly_income': 34.36, 'watt': 60, 'hash_power': 24}]}


def test__given_config__when_constructor__then_instance_with_right_values():
    product_collector = __test_product_collector()

    assert product_collector.products == []
    assert product_collector.usable_cards == _config["usable_cards"]
    assert product_collector.blacklist_words == _config["blacklist_words"]
    assert product_collector.blacklist == _config["blacklist"]
    assert product_collector.webhook_latest_cards == "Webhook latest cards"
    assert product_collector.webhook_bot_status == "Webhook bot status"


def test__given_blacklist_product__when_add_new_product__then_add_unmapped_card_to_products():
    product_collector = __test_product_collector()

    product_collector.add_new_product(__test_product("Blacklist 1"))

    assert len(product_collector.products) == 1
    assert product_collector.products[0].is_mapped() is False


def test__given_blacklist_word_product__when_add_new_product__then_add_unmapped_card_to_products():
    product_collector = __test_product_collector()

    product_collector.add_new_product(__test_product("Karte 1660 kaputt"))

    assert len(product_collector.products) == 1
    assert product_collector.products[0].is_mapped() is False


def test__given_product_not_in_usable_cards__when_add_new_product__then_add_unmapped_card_to_products():
    product_collector = __test_product_collector()

    product_collector.add_new_product(__test_product("Karte 1060"))

    assert len(product_collector.products) == 1
    assert product_collector.products[0].is_mapped() is False


def test__given_usable_product__when_add_new_product__then_add_mapped_card_to_products():
    product_collector = __test_product_collector()

    product_collector.add_new_product(__test_product("Karte 1660"))

    assert len(product_collector.products) == 1
    mapped_product = product_collector.products[0]
    assert mapped_product.is_mapped() is True
    assert mapped_product._short_name == "1660"
    assert mapped_product.roi() == (100 / 34.36)


def test__given_timestamp_before_card__when_mapped_products_after_timestamp__then_card_is_time_relevant():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))

    product_collector.mapped_products_after_timestamp(datetime.today().replace(month=12, day=16, hour=20, minute=32, second=0, microsecond=0))

    assert product_collector.products[0]._time_relevant is True


def test__given_timestamp_same_as_card__when_mapped_products_after_timestamp__then_card_is_time_relevant():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))

    product_collector.mapped_products_after_timestamp(datetime.today().replace(month=12, day=16, hour=20, minute=37, second=0, microsecond=0))

    assert product_collector.products[0]._time_relevant is True


def test__given_timestamp_after_card__when_mapped_products_after_timestamp__then_card_is_not_time_relevant():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))

    product_collector.mapped_products_after_timestamp(datetime.today().replace(month=12, day=16, hour=20, minute=42, second=0, microsecond=0))

    assert product_collector.products[0]._time_relevant is False


def test__given_two_cards__when_products_size__then_2():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))
    product_collector.add_new_product(__test_product("1660"))

    assert product_collector.products_size() == 2


@mock.patch("src.product.product_collector.logging", return_value=None, autospec=True)
def test__given_two_cards__when_print_result_to_console__then_right_console_output(logging_mock):
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))
    product_collector.add_new_product(__test_product("16XX"))

    product_collector.print_result_to_console(True)

    assert len(logging_mock.method_calls) == 5


@mock.patch("src.product.product_collector.logging", return_value=None, autospec=True)
def test__given_two_cards_print_non_mapped_false__when_print_result_to_console__then_right_console_output(logging_mock):
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))
    product_collector.add_new_product(__test_product("16XX"))

    product_collector.print_result_to_console(False)

    assert len(logging_mock.method_calls) == 3


@mock.patch("src.product.product_collector.Webhook", return_value=None, autospec=True)
def test__given_two_cards__when_send_result_to_discord__then_right_discord_message(webhook_mock):
    product_collector = __test_product_collector()
    __add_product_with_timestamp_now_to(product_collector)
    __add_product_with_timestamp_now_to(product_collector)

    product_collector.send_result_to_discord()

    assert len(webhook_mock.method_calls) == 1


@mock.patch("src.product.product_collector.Webhook", return_value=None, autospec=True)
def test__given_cards_where_message_is_over_1999_chars__when_send_result_to_discord__then_message_length_is_maximum_1999(webhook_mock):
    product_collector = __test_product_collector()
    for _ in range(100):
        __add_product_with_timestamp_now_to(product_collector)

    product_collector.send_result_to_discord()

    assert len(webhook_mock.method_calls) == 1


def __add_product_with_timestamp_now_to(product_collector):
    now = datetime.now()
    product = __test_product("1660", timestamp_text=f"Heute, {now.hour}:{now.minute} Uhr")
    product.mark_as_mapped()
    product.mark_as_time_relevant(TimestampTranslator.text_to_timestamp_or_max_if_not_today("16.12. - 20:34 Uhr"))
    product_collector.add_new_product(product)


def __test_product(name: str, timestamp_text="16.12. - 20:37 Uhr") -> Product:
    return Product(name, "100", "/Link", timestamp_text)


def __test_product_collector() -> ProductCollector:
    os.environ["Discord_Latest_Cards"] = "Webhook latest cards"
    os.environ["Discord_Bot_Status"] = "Webhook bot status"

    return ProductCollector(_config)

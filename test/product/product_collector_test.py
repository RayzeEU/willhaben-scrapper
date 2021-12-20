import os
from datetime import datetime

from src.product.product import Product
from src.product.product_collector import ProductCollector

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
    assert product_collector.products[0].mapped is False


def test__given_blacklist_word_product__when_add_new_product__then_add_unmapped_card_to_products():
    product_collector = __test_product_collector()

    product_collector.add_new_product(__test_product("Karte 1660 kaputt"))

    assert len(product_collector.products) == 1
    assert product_collector.products[0].mapped is False


def test__given_product_not_in_usable_cards__when_add_new_product__then_add_unmapped_card_to_products():
    product_collector = __test_product_collector()

    product_collector.add_new_product(__test_product("Karte 1060"))

    assert len(product_collector.products) == 1
    assert product_collector.products[0].mapped is False


def test__given_usable_product__when_add_new_product__then_add_mapped_card_to_products():
    product_collector = __test_product_collector()

    product_collector.add_new_product(__test_product("Karte 1660"))

    assert len(product_collector.products) == 1
    mapped_product = product_collector.products[0]
    assert mapped_product.mapped is True
    assert mapped_product.short_name == "1660"
    assert mapped_product.roi == (100 / 34.36)


def test__given_timestamp_before_card__when_mapped_products_after_timestamp__then_card_is_time_relevant():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))

    product_collector.mapped_products_after_timestamp(datetime.today().replace(month=12, day=16, hour=20, minute=32, second=0, microsecond=0))

    assert product_collector.products[0].time_relevant is True


def test__given_timestamp_same_as_card__when_mapped_products_after_timestamp__then_card_is_time_relevant():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))

    product_collector.mapped_products_after_timestamp(datetime.today().replace(month=12, day=16, hour=20, minute=37, second=0, microsecond=0))

    assert product_collector.products[0].time_relevant is True


def test__given_timestamp_after_card__when_mapped_products_after_timestamp__then_card_is_not_time_relevant():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))

    product_collector.mapped_products_after_timestamp(datetime.today().replace(month=12, day=16, hour=20, minute=42, second=0, microsecond=0))

    assert product_collector.products[0].time_relevant is False


def test__given_two_cards__when_products_size__then_2():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))
    product_collector.add_new_product(__test_product("1660"))

    assert product_collector.products_size() == 2


def test__given_two_cards__when_print_result_to_console__then_right_console_output():
    product_collector = __test_product_collector()
    product_collector.add_new_product(__test_product("1660"))
    product_collector.add_new_product(__test_product("1660"))

    product_collector.print_result_to_console(True)
    # TODO Verify console output -> not that important for now as it is only used for local testing.
    #  Should not throw an error for now.


def __test_product(name: str) -> Product:
    return Product(name, "100", "/Link", "16.12. - 20:37 Uhr")


def __test_product_collector() -> ProductCollector:
    os.environ["Discord_Latest_Cards"] = "Webhook latest cards"
    os.environ["Discord_Bot_Status"] = "Webhook bot status"

    return ProductCollector(_config)

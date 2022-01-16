import json
import os
from unittest import mock

import requests_mock

from src.poller import PagePoller


@mock.patch("src.poller.ProductCollector", autospec=True)
def test__given_config__when_constructor__then_right_initial_values_are_set(product_collector_mock):
    config = __load_test_config()

    page_poller = __test_page_poller(config)

    assert page_poller._show_non_mapping is True
    assert page_poller._config == config
    assert page_poller._product_collector is not None
    assert product_collector_mock.call_count == 1


def __test_page_poller(config):
    os.environ["Discord_Latest_Cards"] = "Webhook latest cards"
    os.environ["Discord_Bot_Status"] = "Webhook bot status"
    page_poller = PagePoller(True, config)
    return page_poller


def __load_test_config():
    with open("resources/config.json") as config_json:
        config = json.load(config_json)
    return config


@mock.patch("src.poller.ProductCollector", autospec=True)
def test__given_test_html_page__when_check_website__then_product_collector_in_page_poller_contains_25_products(product_collector_mock):
    config = __load_test_config()
    page_poller = __test_page_poller(config)

    with open("test/test_html.html") as html:
        test_html = html.read()

    with requests_mock.Mocker() as m:
        m.get(url=config["url"], text=test_html)

    page_poller.check_website()

    # constructor
    assert product_collector_mock.call_count == 1

    # add products
    call_count = 25
    # mapped_products_after_timestamp
    call_count = call_count + 1
    # print_result_to_console
    call_count = call_count + 1
    # send_result_to_discord
    call_count = call_count + 1

    assert len(page_poller._product_collector.method_calls) == call_count

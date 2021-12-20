import json
import os
from unittest import mock

import requests_mock

from src.poller import PagePoller


def test__given_config__when_constructor__then_right_initial_values_are_set():
    config = __load_test_config()

    page_poller = __test_page_poller(config)

    assert page_poller.show_non_mapping is True
    assert page_poller.config == config
    assert page_poller.product_collector is not None


def __test_page_poller(config):
    os.environ["Discord_Latest_Cards"] = "Webhook latest cards"
    os.environ["Discord_Bot_Status"] = "Webhook bot status"
    page_poller = PagePoller(True, config)
    return page_poller


def __load_test_config():
    with open("resources/config.json") as config_json:
        config = json.load(config_json)
    return config


@mock.patch("src.product.product_collector.Webhook", return_value=None, autospec=True)
def test__given_test_html_page__when_check_website__then_product_collector_in_page_poller_contains_25_products(webhook_mock):
    config = __load_test_config()
    page_poller = __test_page_poller(config)

    with open("test/test_html.html") as html:
        test_html = html.read()

    with requests_mock.Mocker() as m:
        m.get(url=config["url"], text=test_html)

    page_poller.check_website()

    assert len(page_poller.product_collector.products) == 25
    # TODO mock product_collector and just check the "add_new_product" method call count

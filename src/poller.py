import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from datetime import datetime

from product.product_collector import ProductCollector
from src.background_colors import BackgroundColors
from product.product import Product

GECKODRIVER_PATH = "../resources/geckodriver-v0.27.0-win64/geckodriver.exe"
LAST_CARD_TIMESTAMP_FILE = "../resources/last_card_timestamp.txt"


class PagePoller:

    def __init__(self, show_non_mapping, hide_selenium_browser, is_looping, private_config, config):
        self.show_non_mapping = show_non_mapping
        self.is_looping = is_looping
        self.private_config = private_config
        self.config = config

        print("%s cards are usable" % len(self.config["usable_cards"]))

        print("setting up firefox ...")
        firefox_options = Options()
        # --headless is for hiding the Firefox window, comment out to show again
        if hide_selenium_browser:
            firefox_options.add_argument("--headless")

        # set service log path to "nul" to disable logging - works only for windows
        self.driver = webdriver.Firefox(executable_path=os.path.join(os.path.dirname(__file__), GECKODRIVER_PATH),
                                        options=firefox_options,
                                        service_log_path="nul")

        print("opening page ...")
        self.driver.get(config["url"])
        time.sleep(1)
        self.accept_cookies()

        self.product_collector = ProductCollector(config, private_config)

    def accept_cookies(self):
        # Accept Cookies button
        try:
            self.driver.find_element_by_id('didomi-notice-agree-button').click()
        except NoSuchElementException:
            pass

    def check_website(self):
        self.driver.refresh()
        self.product_collector.clear_collector()

        self.scan_pages_for_products()

        if self.is_looping:
            self.check_new_cards()

        self.product_collector.print_result_to_console(self.show_non_mapping)
        self.product_collector.print_result_to_discord()

    def scan_pages_for_products(self):
        print("finding cards ...")

        self.scroll_to_bottom()
        self.scan_for_products_and_add_to()

    def scroll_to_bottom(self):
        scroll_pause_time = 0.1
        height_to_scroll = 1000

        while True:
            height_to_scroll = height_to_scroll + 1000

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, %s);" % height_to_scroll)

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if height_to_scroll > new_height:
                break

    def scan_for_products_and_add_to(self):
        # gERttF = css for the title
        elements = self.driver.find_elements_by_css_selector('.gERttF')
        # fwafsN = css for the price
        price_elements = self.driver.find_elements_by_css_selector('.fwafsN')
        # fGZgWF = css for the element with the link attribute
        links = self.driver.find_elements_by_css_selector(".fGZgWF")
        # fGZgWF = css for the element with the timestamp
        timestamps = self.driver.find_elements_by_css_selector(".bOajya > p")

        if len(elements) != len(price_elements) or len(elements) != len(links) or len(elements) != len(timestamps):
            print(BackgroundColors.WARNING + "Warning: There is a mismatch between the element data counters." + BackgroundColors.ENDC)
        else:
            print(BackgroundColors.OKCYAN + "No mismatches found." + BackgroundColors.ENDC)

        print("found %s cards ..." % len(elements))

        for element, price, link, timestamp in zip(elements, price_elements, links, timestamps):
            self.product_collector.add_new_product(
                Product(element.text, price.text, link.get_attribute("href"), timestamp.text))

    def check_new_cards(self):
        check_timestamp = datetime.now()

        with open(os.path.join(os.path.dirname(__file__), LAST_CARD_TIMESTAMP_FILE), "r",
                  encoding="UTF8") as last_card_timestamp_file:
            last_check_timestamp = datetime.strptime(last_card_timestamp_file.read(), "%d.%m.%Y %H:%M")
            self.product_collector.mapped_products_after_timestamp(last_check_timestamp)
            last_card_timestamp_file.close()

        with open(os.path.join(os.path.dirname(__file__), LAST_CARD_TIMESTAMP_FILE), "w",
                  encoding="UTF8") as last_card_timestamp_file:
            last_card_timestamp_file.write(check_timestamp.strftime("%d.%m.%Y %H:%M"))
            last_card_timestamp_file.close()

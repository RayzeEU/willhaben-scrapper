import configparser
import os
import time

from discord import Webhook, RequestsWebhookAdapter

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from src.background_colors import BackgroundColors
from src.product import Product

NOT_MAPPED = "Not mapped"

GECKODRIVER_PATH = "..\\drivers\\geckodriver-v0.27.0-win64\\geckodriver.exe"
PROPERTIES_FILE = "..\\config.properties"
BLACKLIST_FILE = "..\\blacklist.txt"
LAST_CARD_FILE = "..\\last_card.txt"
USABLE_CARDS_FILE = "../usable_cards.properties"


class PagePoller:
    """
    A class used to represent the web page which is crawled

    ...

    Attributes
    ----------
    config : ConfigParser
        the config of the tool
    products : list of src.product.Product
        a list of products listed on the website
    driver : Firefox
        the driver which is used by selenium to open/scrap the website

    Methods
    -------
    check_website()
        Loops through the webpage, adds products to the products list and close the browser
    accept_cookies()
        Creates the driver for the browser and clicks the cookies button
    refresh_page()
        Re-opens the browser
    scroll_to_bottom()
        Scrolls to the bottom of the page
    """

    def __init__(self, pages_to_scan, show_non_mapping, hide_selenium_browser, is_looping):
        self.pages_to_scan = pages_to_scan
        self.show_non_mapping = show_non_mapping
        self.is_looping = is_looping

        print("reading config ...")
        # Read config file, should contain 'url'
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), PROPERTIES_FILE))
        self.config = config

        print("reading blacklist ...")
        # Read the blacklist file, exact product names in this file will be ignored
        with open(os.path.join(os.path.dirname(__file__), BLACKLIST_FILE), "r", encoding="UTF8") as blacklist:
            self.blacklist = blacklist.read().splitlines()

        print("%s cards are blacklisted" % len(self.blacklist))

        # Read the usable cards file, exact card names with the monthly profit
        config.read(os.path.join(os.path.dirname(__file__), USABLE_CARDS_FILE))
        self.usable_cards = config

        print("%s cards are usable" % self.usable_cards.items("Cards"))

        print("setting up firefox ...")
        firefox_options = Options()
        # --headless is for hiding the Firefox window, comment out to show again
        if hide_selenium_browser:
            firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path=os.path.join(os.path.dirname(__file__), GECKODRIVER_PATH), options=firefox_options)

        print("opening page ...")
        self.driver.get(self.config.get('General', 'url'))
        time.sleep(1)
        self.accept_cookies()

        self.products = []
        self.products_not_mapped = []
        self.products_mapped = []

    def check_website(self):
        self.scan_pages_for_products()

        self.calculate_card_performances()

        if self.is_looping:
            self.check_new_cards()

        self.print_result_to_console()
        self.send_mapped_products_to_discord()

        self.driver.close()
        self.driver.quit()

    def scan_pages_for_products(self):
        index = 0
        while index < self.pages_to_scan:
            print("finding cards (page: %s) ..." % (index + 1))

            self.scroll_to_bottom()
            self.scan_for_products_and_add_to()

            self.driver.find_element_by_css_selector("a[data-testid=\"pagination-bottom-next-button\"]").click()

            print("finished finding cards (page: %s) ..." % (index + 1))
            index = index + 1

        print("found %s cards ..." % len(self.products))

    def print_result_to_console(self):
        products = self.products
        products_mapped = self.products_mapped
        products_not_mapped = self.products_not_mapped

        print(BackgroundColors.OKCYAN + "Total products found: %s" % len(products) + BackgroundColors.ENDC)

        if self.show_non_mapping:
            print(BackgroundColors.WARNING + "Total products not matched: %s" % len(
                products_not_mapped) + BackgroundColors.ENDC)
            products_not_mapped.sort(key=lambda p: p.roi, reverse=True)
            for product in products_not_mapped:
                print(product.display_string)

        print(BackgroundColors.OKCYAN + "Total products matched: %s" % len(products_mapped) + BackgroundColors.ENDC)
        products_mapped.sort(key=lambda p: p.roi, reverse=True)
        for product in products_mapped:
            print(product.display_string)

    def send_mapped_products_to_discord(self):
        return_message = ""

        products_mapped_discord = self.products_mapped.copy()
        products_mapped_discord.sort(key=lambda p: p.roi, reverse=False)
        for product in products_mapped_discord:
            if return_message != "":
                return_message = return_message + "\r\n"

            return_message = return_message + product.display_string
            if len(return_message) > 1900:
                break

        return_message = return_message.replace(BackgroundColors.OKGREEN, "").replace(BackgroundColors.OKCYAN, "").replace(BackgroundColors.OKBLUE, "").replace(BackgroundColors.ENDC, "")
        webhook = Webhook.from_url(self.private_config.get('Webhooks', 'latest-cards'), adapter=RequestsWebhookAdapter())
        webhook.send(return_message)

    def check_new_cards(self):
        products = self.products_mapped
        with open(os.path.join(os.path.dirname(__file__), LAST_CARD_FILE), "r", encoding="UTF8") as last_card_file:
            last_card = last_card_file.read()
            new_products = []
            last_card_file.close()

            if last_card == products[0].name:
                self.products_mapped = []
                print("No new cards found.")
                return

            for product in products:
                if product.name == last_card:
                    break
                new_products.append(product)

            with open(os.path.join(os.path.dirname(__file__), LAST_CARD_FILE), "w", encoding="UTF8") as last_card_file:
                last_card_file.write(new_products[0].name)

    def calculate_card_performances(self):
        print("calculating card performances ...")
        usable_cards = self.usable_cards.items("Cards")
        for product in self.products:
            product_name_lowercase = product.name.replace(' ', '').lower()

            if "defekt" not in product_name_lowercase\
                    and "kaputt" not in product_name_lowercase\
                    and "lhr" not in product_name_lowercase\
                    and product.name not in self.blacklist:
                found = False
                for usable_card in usable_cards:
                    if usable_card[0] in product_name_lowercase:
                        product.set_product_properties(usable_card[0], float(usable_card[1]))
                        self.products_mapped.append(product)
                        found = True

                if not found:
                    product.set_product_properties(NOT_MAPPED, 1)
                    self.products_not_mapped.append(product)

    def scan_for_products_and_add_to(self):
        products = self.products

        # gERttF = css for the title
        elements = self.driver.find_elements_by_css_selector('.gERttF')
        # fwafsN = css for the price
        price_elements = self.driver.find_elements_by_css_selector('.fwafsN')
        # fGZgWF = css for the element for one product
        links = self.driver.find_elements_by_css_selector(".fGZgWF")

        if len(elements) != len(price_elements) or len(elements) != len(links):
            print(BackgroundColors.WARNING + "Warning: There is a mismatch between element count, prices count and link count." + BackgroundColors.ENDC)
        else:
            print(BackgroundColors.OKCYAN + "No mismatches between element and price count found." + BackgroundColors.ENDC)

        for element, price, link in zip(elements, price_elements, links):
            products.append(
                Product(element.text, price.text.replace('€', '').replace(' ', '').replace(',', '.'), link.get_attribute("href")))

    def accept_cookies(self):
        # Accept Cookies button
        try:
            self.driver.find_element_by_id('didomi-notice-agree-button').click()
        except NoSuchElementException:
            pass

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

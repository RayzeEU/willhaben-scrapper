import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import configparser
import os

from src.product import Product

GECKODRIVER_PATH = "..\\drivers\\geckodriver-v0.27.0-win64\\geckodriver.exe"
PROPERTIES_FILE = "..\\config.properties"
BLACKLIST_FILE = "..\\blacklist.txt"


class BackgroundColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

    def __init__(self):
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

        print("setting up firefox ...")
        firefox_options = Options()
        # --headless is for hiding the Firefox window, comment out to show again
        firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path=os.path.join(os.path.dirname(__file__), GECKODRIVER_PATH), options=firefox_options)

        print("opening page ...")
        self.driver.get(self.config.get('General', 'url'))
        self.accept_cookies()

        self.products = []

    def check_website(self):
        index = 0
        products = self.products

        while index < 3:
            print("finding cards (page: %s) ..." % (index + 1))

            self.scroll_to_bottom()
            self.scan_for_products_and_add_to(products)

            self.driver.find_element_by_css_selector("a[data-testid=\"pagination-bottom-next-button\"]").click()

            print("finished finding cards (page: %s) ..." % (index + 1))
            index = index + 1

        count_products = len(products)
        count_matching = len(products)

        print("found %s cards ..." % count_products)

        count_matching = self.calculate_card_performances(count_matching, products)

        products.sort(key=lambda p: p.roi, reverse=True)

        for product in products:
            if product.display_string == "":
                continue
            print(product.display_string)

        print(BackgroundColors.OKCYAN + "Total Products matched/found: %s/%s" % (count_matching, count_products) + BackgroundColors.ENDC)

        self.driver.close()
        self.driver.quit()

    def calculate_card_performances(self, count_matching, products):
        print("calculating card performances ...")
        for product in products:
            product_name_uppercase = product.name.replace(' ', '').upper()

            if "DEFEKT" in product_name_uppercase or product.name in self.blacklist:
                count_matching = count_matching - 1
                continue

            if "1050TI" in product_name_uppercase:
                product.set_product_properties("1050 Ti", 12.3)

            elif "1060" in product_name_uppercase and "3GB" not in product_name_uppercase:
                product.set_product_properties("1060", 35.7)

            elif "1070TI" in product_name_uppercase:
                product.set_product_properties("1070 Ti", 47.1)
            elif "1070" in product_name_uppercase:
                product.set_product_properties("1070", 44.4)

            elif "1080TI" in product_name_uppercase:
                product.set_product_properties("1080 Ti", 68.1)
            elif "1080" in product_name_uppercase:
                product.set_product_properties("1080", 55.5)

            elif "1650SUPER" in product_name_uppercase:
                product.set_product_properties("1650 Super", 23.7)
            elif "1650" in product_name_uppercase:
                product.set_product_properties("1650", 25.5)

            elif "1660SUPER" in product_name_uppercase:
                product.set_product_properties("1660 Super", 50.4)
            elif "1660TI" in product_name_uppercase:
                product.set_product_properties("1660 Ti", 49.2)
            elif "1660" in product_name_uppercase:
                product.set_product_properties("1660", 41.1)

            elif "2060SUPER" in product_name_uppercase:
                product.set_product_properties("2060 Super", 66.9)
            elif "2060" in product_name_uppercase:
                product.set_product_properties("2060", 51.9)

            elif "2070SUPER" in product_name_uppercase:
                product.set_product_properties("2070 Super", 71.4)
            elif "2070" in product_name_uppercase:
                product.set_product_properties("2070", 67.8)

            elif "2080SUPER" in product_name_uppercase:
                product.set_product_properties("2080 Super", 72)
            elif "2080" in product_name_uppercase:
                product.set_product_properties("2080", 72.9)

            elif "P2200" in product_name_uppercase:
                product.set_product_properties("P2200", 30.3)

            elif "390" in product_name_uppercase:
                product.set_product_properties("390", 28.5)

            elif "4000" in product_name_uppercase:
                product.set_product_properties("4000", 59.1)

            elif "480" in product_name_uppercase:
                product.set_product_properties("480", 43.8)

            elif "5700XT" in product_name_uppercase:
                product.set_product_properties("5700 XT", 86.1)

            elif "590" in product_name_uppercase:
                product.set_product_properties("590", 44.4)

            elif "6600" in product_name_uppercase:
                product.set_product_properties("6600", 51.9)

            elif "6700" in product_name_uppercase:
                product.set_product_properties("6700", 70.8)

            elif "VEGA56" in product_name_uppercase:
                product.set_product_properties("VEGA 56", 51.6)
            elif "VEGA64" in product_name_uppercase:
                product.set_product_properties("VEGA 64", 66)

            elif "3090" in product_name_uppercase:
                product.set_product_properties("3090", 191.4)

            else:
                product.set_product_properties("Not mapped", 1)
                count_matching = count_matching - 1
        return count_matching

    def scan_for_products_and_add_to(self, products):
        # gERttF = css for the title
        # fwafsN = css for the price
        elements = self.driver.find_elements_by_css_selector('.gERttF')
        price_elements = self.driver.find_elements_by_css_selector('.fwafsN')
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


pagepoller = PagePoller()
pagepoller.check_website()

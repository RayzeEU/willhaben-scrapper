import time
from asyncio import wait_for
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import configparser
import os

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


class Product:
    """
    A class used to represent a product on Willhaben

    ...

    Attributes
    ----------
    name : str
        the name of the product
    price : str
        the price of the product
    roi : float
        the return-of-investment property of the product
    display_string : str
        this property combines important properties into a readable string which can be printed

    Methods
    -------
    set_product_properties(card_name, profit_per_month)
        Sets return of investment and display string properties
    """

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.roi = 0.00
        self.display_string = ""

    def set_product_properties(self, card_name, profit_per_month):
        if self.price == '':
            return

        return_of_investment = float(self.price) / profit_per_month
        self.roi = float(return_of_investment)

        self.display_string = "ROI {7}\'{6}\' - {1}€{8}: {4}{2}{5} (Full Name: {3})"\
            .format(self.name,
                    self.price,
                    '{0:.2f}'.format(return_of_investment),
                    self.name,
                    BackgroundColors.OKGREEN,
                    BackgroundColors.ENDC,
                    card_name,
                    BackgroundColors.OKBLUE,
                    BackgroundColors.ENDC)


class PagePoller:
    """
    A class used to represent the web page which is crawled

    ...

    Attributes
    ----------
    config : ConfigParser
        the config of the tool
    products : list of Product
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

        print("reading blacklist")
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
            self.scroll_to_bottom()

            print("finding cards (%s) ..." % index)

            # gERttF = css for the title
            # fwafsN = css for the price
            elements = self.driver.find_elements_by_css_selector('.gERttF')
            price_elements = self.driver.find_elements_by_css_selector('.fwafsN')

            for element, price_element in zip(elements, price_elements):
                products.append(
                    Product(element.text, price_element.text.replace('€', '').replace(' ', '').replace(',', '.')))

            with wait_for_page_load(self.driver):
                self.driver.find_element_by_css_selector("a[data-testid=\"pagination-bottom-next-button\"]").click()

            print("finished finding cards (%s) ..." % index)

            index = index + 1

        count_products = len(products)
        count_matching = len(products)

        print("found %s cards ..." % count_products)
        print("calculating card performances ...")
        for price_element in products:
            product_name_uppercase = price_element.name.replace(' ', '').upper()

            if "DEFEKT" in product_name_uppercase or price_element.name in self.blacklist:
                count_matching = count_matching - 1
                continue

            if "1050TI" in product_name_uppercase:
                price_element.set_product_properties("1050 Ti", 12.3)

            elif "1060" in product_name_uppercase and "3GB" not in product_name_uppercase:
                price_element.set_product_properties("1060", 35.7)

            elif "1070TI" in product_name_uppercase:
                price_element.set_product_properties("1070 Ti", 47.1)
            elif "1070" in product_name_uppercase:
                price_element.set_product_properties("1070", 44.4)

            elif "1080TI" in product_name_uppercase:
                price_element.set_product_properties("1080 Ti", 68.1)
            elif "1080" in product_name_uppercase:
                price_element.set_product_properties("1080", 55.5)

            elif "1650SUPER" in product_name_uppercase:
                price_element.set_product_properties("1650 Super", 23.7)
            elif "1650" in product_name_uppercase:
                price_element.set_product_properties("1650", 25.5)

            elif "1660SUPER" in product_name_uppercase:
                price_element.set_product_properties("1660 Super", 50.4)
            elif "1660TI" in product_name_uppercase:
                price_element.set_product_properties("1660 Ti", 49.2)
            elif "1660" in product_name_uppercase:
                price_element.set_product_properties("1660", 41.1)

            elif "2060SUPER" in product_name_uppercase:
                price_element.set_product_properties("2060 Super", 66.9)
            elif "2060" in product_name_uppercase:
                price_element.set_product_properties("2060", 51.9)

            elif "2070SUPER" in product_name_uppercase:
                price_element.set_product_properties("2070 Super", 71.4)
            elif "2070" in product_name_uppercase:
                price_element.set_product_properties("2070", 67.8)

            elif "2080SUPER" in product_name_uppercase:
                price_element.set_product_properties("2080 Super", 72)
            elif "2080" in product_name_uppercase:
                price_element.set_product_properties("2080", 72.9)

            elif "P2200" in product_name_uppercase:
                price_element.set_product_properties("P2200", 30.3)

            elif "390" in product_name_uppercase:
                price_element.set_product_properties("390", 28.5)

            elif "4000" in product_name_uppercase:
                price_element.set_product_properties("4000", 59.1)

            elif "480" in product_name_uppercase:
                price_element.set_product_properties("480", 43.8)

            elif "5700XT" in product_name_uppercase:
                price_element.set_product_properties("5700 XT", 86.1)

            elif "590" in product_name_uppercase:
                price_element.set_product_properties("590", 44.4)

            elif "6600" in product_name_uppercase:
                price_element.set_product_properties("6600", 51.9)

            elif "6700" in product_name_uppercase:
                price_element.set_product_properties("6700", 70.8)

            elif "VEGA56" in product_name_uppercase:
                price_element.set_product_properties("VEGA 56", 51.6)
            elif "VEGA64" in product_name_uppercase:
                price_element.set_product_properties("VEGA 64", 66)

            elif "3090" in product_name_uppercase:
                price_element.set_product_properties("3090", 191.4)

            else:
                price_element.set_product_properties("Not mapped", 1)
                count_matching = count_matching - 1

        products.sort(key=lambda p: p.roi, reverse=True)

        for price_element in products:
            if (price_element.display_string == ""):
                continue
            print(price_element.display_string)

        print(BackgroundColors.OKCYAN + "Total Products matched/found: %s/%s" % (count_matching, count_products) + BackgroundColors.ENDC)
        # if len(elements) != len(price_elements):
        #     print(BackgroundColors.WARNING + "Warning: There is a mismatch between element count and prices count." + BackgroundColors.ENDC)
        # else:
        #     print(BackgroundColors.OKCYAN + "No mismatches between element and price count found." + BackgroundColors.ENDC)

        self.driver.close()
        self.driver.quit()

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
            print("scrolling ...")

            height_to_scroll = height_to_scroll + 1000

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, %s);" % height_to_scroll)

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if height_to_scroll > new_height:
                break


class wait_for_page_load(object):
    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for(self.page_has_loaded, 60)


pagepoller = PagePoller()

pagepoller.check_website()

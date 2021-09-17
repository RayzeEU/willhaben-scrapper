import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import configparser

class bcolors:
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
    setProductProperties(card_name, profit_per_month)
        Sets return of investment and display string properties
    """

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.roi = 0.00
        self.display_string = ""

    def setProductProperties(self, card_name, profit_per_month):

        if (self.price == ''):
            return

        return_of_investment = float(self.price) / profit_per_month
        self.roi = float(return_of_investment)

        self.display_string =  "ROI {7}\'{6}\' - {1}€{8}: {4}{2}{5} (Full Name: {3})".format(self.name, self.price, '{0:.2f}'.format(return_of_investment), self.name, bcolors.OKGREEN, bcolors.ENDC, card_name, bcolors.OKBLUE, bcolors.ENDC)     

class PagePoller:
    """
    A class used to represent the web page which is crawled

    ...

    Attributes
    ----------
    config : ConfigParser
        the config of the tool
    url : str
        the website which should be scrapped
    products : list of Product
        a list of products listed on the website
    driver : Firefox
        the driver which is used by selenium to open/scrap the website

    Methods
    -------
    checkWebsite()
        Loops through the webpage, adds products to the products list and close the browser
    createBrowser()
        Creates the driver for the browser and clicks the cookies button
    refreshPage()
        Re-opens the browser
    scrollToBottom()
        Scrolls to the bottom of the page
    """

    def __init__(self):
        #Read config file, should contain 'url'
        config = configparser.ConfigParser()
        config.read('config.properties')
        self.config = config

        self.url = config.get('General', 'url')
        self.createBrowser()
        self.products = []
    
    def checkWebsite(self):
        #gERttF = css for the title
        #fwafsN = css for the price
        elements = self.driver.find_elements_by_css_selector('.gERttF')
        price_elements = self.driver.find_elements_by_css_selector('.fwafsN')

        for e, p in zip(elements, price_elements):        
            self.products.append(Product(e.text, p.text.replace('€', '').replace(' ', '').replace(',', '.')))
        
        for p in self.products:
            product_name_uppercase = p.name.replace(' ', '').upper()

            if "1060" in product_name_uppercase:
                p.setProductProperties("1060", 35.7)

            elif "1070" in product_name_uppercase:
                p.setProductProperties("1070", 44.4)

            elif "1080TI" in product_name_uppercase:
                p.setProductProperties("1080 Ti", 68.1)
            elif "1080" in product_name_uppercase:
                p.setProductProperties("1080", 55.5)

            elif "1660SUPER" in product_name_uppercase:
                p.setProductProperties("1660 Super", 50.4)
            elif "1660TI" in product_name_uppercase:
                p.setProductProperties("1660 Ti", 49.2)
            elif "1660" in product_name_uppercase:
                p.setProductProperties("1660", 41.1)

            elif "2060SUPER" in product_name_uppercase:
                p.setProductProperties("2060 Super", 66.9)
            elif "2060" in product_name_uppercase:
                p.setProductProperties("2060", 51.9)
                
            elif "2070SUPER" in product_name_uppercase:
                p.setProductProperties("2070 Super", 71.4)
            elif "2070" in product_name_uppercase:
                p.setProductProperties("2070", 67.8)

            elif "2080SUPER" in product_name_uppercase:
                p.setProductProperties("2080 Super", 72)
            elif "2080" in product_name_uppercase:
                p.setProductProperties("2080", 72.9)

            else:
                p.setProductProperties("Not mapped", 1)
        
        self.products.sort(key=lambda p: p.roi, reverse=True)

        for p in self.products:
            print(p.display_string)

        print(bcolors.OKCYAN + "Total Products found: %s" % len(self.products) + bcolors.ENDC)
        if (len(elements) != len(price_elements)):
            print(bcolors.WARNING + "Warning: There is a mismatch between element count and prices count." + bcolors.ENDC)
        else:
            print(bcolors.OKCYAN + "No mismatches between element and price count found." + bcolors.ENDC)
        
        self.driver.close()
        self.driver.quit()

    def createBrowser(self):
        self.driver = webdriver.Firefox(executable_path=self.config.get('General', 'driverPath'))
        self.driver.get(self.url)

        #Accept Cookies button
        try:
            self.driver.find_element_by_id('didomi-notice-agree-button').click()
        except NoSuchElementException:
            pass

    def refreshPage(self):
        self.driver.close()
        self.driver.quit()
        self.createBrowser()

    def scrollToBottom(self):
        SCROLL_PAUSE_TIME = 0.1

        height_to_scroll = 1000

        while True:
            
            height_to_scroll = height_to_scroll + 1000

            # Scroll down to bottom
            pagepoller.driver.execute_script("window.scrollTo(0, %s);" % height_to_scroll)

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = pagepoller.driver.execute_script("return document.body.scrollHeight")
            if height_to_scroll > new_height:
                break

pagepoller = PagePoller()

pagepoller.scrollToBottom()
pagepoller.checkWebsite()
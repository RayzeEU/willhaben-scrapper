from src.background_colors import BackgroundColors


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

    def __init__(self, name, price, link):
        self.name = name
        self.price = price
        self.roi = 0.00
        self.display_string = ""
        self.link = link

    def set_product_properties(self, card_name, profit_per_month):
        if self.price == '':
            return

        return_of_investment = float(self.price) / profit_per_month
        self.roi = float(return_of_investment)

        self.display_string = "ROI {6}\'{5}\' - {0}€{7}: {3}{1}{4} (Full Name: {2} -> {8})"\
            .format(self.price,
                    '{0:.2f}'.format(return_of_investment),
                    self.name,
                    BackgroundColors.OKGREEN,
                    BackgroundColors.ENDC,
                    card_name,
                    BackgroundColors.OKBLUE,
                    BackgroundColors.ENDC,
                    self.link)
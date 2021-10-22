from translator.currency_translator import CurrencyTranslator
from src.background_colors import BackgroundColors
from translator.timestamp_translator import TimestampTranslator


class Product:

    def __init__(self, name, price_text, link, timestamp_text):
        self.name = name
        self.short_name = ""
        self.price = CurrencyTranslator.text_to_float(price_text)
        self.roi = 0.00
        self.link = link
        self.timestamp = TimestampTranslator.text_to_timestamp_or_max_if_not_today(timestamp_text)
        self.mapped = False
        self.time_relevant = False

    def set_product_properties(self, card_name, profit_per_month):
        if self.price == '':
            return

        self.short_name = card_name

        return_of_investment = float(self.price) / profit_per_month
        self.roi = float(return_of_investment)

    def display_string_colored(self):
        return "{6}\'{5}\' - {0}{7} - ROI: {3}{1}{4} (Full Name: {2} -> {8})" \
            .format(self.__price_formatted(),
                    self.__roi_formatted(),
                    self.name,
                    BackgroundColors.OKGREEN,
                    BackgroundColors.ENDC,
                    self.name,
                    BackgroundColors.OKBLUE,
                    BackgroundColors.ENDC,
                    self.link)

    def __price_formatted(self):
        return CurrencyTranslator.float_to_text(self.price)

    def __roi_formatted(self):
        return '{0:.2f}'.format(self.roi)

    def display_string_uncolored(self):
        return "\'{3}\' - {0} - ROI: {1} (Full Name: {2} -> {4})" \
            .format(self.__price_formatted(),
                    self.__roi_formatted(),
                    self.name,
                    self.name,
                    self.link)

    def mark_as_mapped(self):
        self.mapped = True

    def mark_as_time_relevant(self):
        self.time_relevant = True

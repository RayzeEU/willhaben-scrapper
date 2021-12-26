from src.translator.currency_translator import CurrencyTranslator
from src.background_colors import BackgroundColors
from src.translator.timestamp_translator import TimestampTranslator


class Product:

    def __init__(self, name: str, price_text: str, link: str, timestamp_text: str):
        self._name = name
        self._short_name = ""
        self._price = CurrencyTranslator.text_to_int(price_text)
        self._roi = 0.00
        self._link = 'https://www.willhaben.at' + link
        self.timestamp = TimestampTranslator.text_to_timestamp_or_max_if_not_today(timestamp_text)
        self.mapped = False
        self.time_relevant = False

    def set_product_properties(self, card_name: str, profit_per_month: float):
        self._short_name = card_name

        return_of_investment = float(self._price) / profit_per_month
        self._roi = float(return_of_investment)

    def display_string_colored(self):
        return "{6}\'{5}\' - {0}{7} - ROI: {3}{1}{4} (Full Name: {2} -> {8})" \
            .format(self.__price_formatted(),
                    self.__roi_formatted(),
                    self._name,
                    BackgroundColors.OKGREEN,
                    BackgroundColors.ENDC,
                    self._short_name,
                    BackgroundColors.OKBLUE,
                    BackgroundColors.ENDC,
                    self._link)

    def __price_formatted(self):
        return CurrencyTranslator.int_to_text(self._price)

    def __roi_formatted(self):
        return '{0:.2f}'.format(self._roi)

    def display_string_uncolored(self):
        return "\'{3}\' - {0} - ROI: {1} (Full Name: [{2}]({4}))" \
            .format(self.__price_formatted(),
                    self.__roi_formatted(),
                    self._name,
                    self._short_name,
                    self._link)

    def mark_as_mapped(self):
        self.mapped = True

    def mark_as_time_relevant(self):
        self.time_relevant = True

    def name_lowercase(self) -> str:
        return self._name.replace(' ', '').lower()

    def is_blacklisted(self, blacklist_words, blacklist) -> bool:
        return any(word in self._name for word in blacklist_words) \
               or self._name in blacklist

    def roi(self) -> float:
        return self._roi

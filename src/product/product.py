from src.translator.currency_translator import CurrencyTranslator
from src.background_colors import BackgroundColors


class Product:

    def __init__(self, name: str, short_name: str, price: int, profit_per_month: float, link: str, mapped: bool, time_relevant: bool):
        self._name = name
        self._short_name = short_name
        self._price = price
        self._profit_per_month = profit_per_month
        self._link = link
        self._mapped = mapped
        self._time_relevant = time_relevant

    def display_string_colored(self) -> str:
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

    def __price_formatted(self) -> str:
        return CurrencyTranslator.int_to_text(self._price)

    def __roi_formatted(self) -> str:
        return '{0:.2f}'.format(self.roi())

    def display_string_uncolored(self) -> str:
        return "\'{3}\' - {0} - ROI: {1} (Full Name: [{2}]({4}))" \
            .format(self.__price_formatted(),
                    self.__roi_formatted(),
                    self._name,
                    self._short_name,
                    self._link)

    def roi(self) -> float:
        if self._profit_per_month:
            return float(float(self._price) / self._profit_per_month)
        return 0.0

    def is_mapped(self) -> bool:
        return self._mapped

    def relevant_for_discord(self) -> bool:
        return self._time_relevant and self._mapped

class CurrencyTranslator:
    @staticmethod
    def text_to_float(currency_text):
        if not isinstance(currency_text, str):
            return 0.0

        currency_text = currency_text.replace('€', '').replace(' ', '').replace(',', '.')

        if currency_text == '':
            return 0.0

        return float(currency_text)

    @staticmethod
    def float_to_text(currency_float):
        if not isinstance(currency_float, float):
            return ""

        return "{0}€".format(str(round(float(currency_float), 2)))

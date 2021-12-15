class CurrencyTranslator:
    @staticmethod
    def text_to_int(amount_text: str) -> int:
        amount_text = amount_text.replace('€', '').replace('.', '').replace(' ', '')

        if amount_text == '':
            return 0

        return int(amount_text)

    @staticmethod
    def int_to_text(amount: int) -> str:
        return "{0} €".format(amount)

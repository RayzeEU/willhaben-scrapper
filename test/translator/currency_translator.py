import unittest

from src.translator.currency_translator import CurrencyTranslator


class CurrencyTranslatorTestCase(unittest.TestCase):
    def test__given_float__when_float_to_text__then_correct_text_for_float(self):
        currency_text = CurrencyTranslator.float_to_text(99.11)
        self.assertEqual(currency_text, "99.11€")

    def test__given_int__when_float_to_text__then_empty_text(self):
        currency_text = CurrencyTranslator.float_to_text(99)
        self.assertEqual(currency_text, "")


if __name__ == '__main__':
    unittest.main()

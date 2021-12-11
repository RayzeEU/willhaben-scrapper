from src.translator.currency_translator import CurrencyTranslator


def test__given_float__when_float_to_text__then_correct_text_for_float():
    currency_text = CurrencyTranslator.float_to_text(99.11)
    assert currency_text == "99.11€"


def test__given_int__when_float_to_text__then_empty_text():
    currency_text = CurrencyTranslator.float_to_text(99)
    assert currency_text == ""

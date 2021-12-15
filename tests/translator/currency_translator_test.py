from src.translator.currency_translator import CurrencyTranslator


def test__given_int__when_int_to_text__then_empty_text():
    currency_text = CurrencyTranslator.int_to_text(99)
    assert currency_text == "99 €"


def test__given_int_over_thousand__when_int_to_text__then_empty_text():
    currency_text = CurrencyTranslator.int_to_text(1234)
    assert currency_text == "1234 €"


def test__given_empty_string__when_text_to_int__then_zero():
    currency = CurrencyTranslator.text_to_int("")
    assert currency == 0


def test__given_string_only_digits__when_text_to_int__then_digits_with_decimal_zero():
    currency = CurrencyTranslator.text_to_int("123")
    assert currency == 123


def test__given_string_digits_with_currency__when_text_to_int__then_digits_with_decimal_zero():
    currency = CurrencyTranslator.text_to_int("123€")
    assert currency == 123


def test__given_string_only_float__when_text_to_int__then_digits_with_decimal_zero():
    currency = CurrencyTranslator.text_to_int("1.235")
    assert currency == 1235


def test__given_string_float_with_some_spaces__when_text_to_int__then_digits_with_decimal_zero():
    currency = CurrencyTranslator.text_to_int("1  2  3 5")
    assert currency == 1235

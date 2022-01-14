from src.background_colors import BackgroundColors
from src.product.product import Product
from src.translator.currency_translator import CurrencyTranslator
from src.translator.timestamp_translator import TimestampTranslator


TEST_PRODUCT_SHORT_NAME = "Card name"
TEST_PRODUCT_NAME = "Name"
TEST_PRODUCT_PRICE_TEXT = "199"
TEST_PRODUCT_PRICE = CurrencyTranslator.text_to_int(TEST_PRODUCT_PRICE_TEXT)
TEST_PRODUCT_PROFIT_PER_MONTH = 20.0
TEST_PRODUCT_ROI = (float(TEST_PRODUCT_PRICE) / TEST_PRODUCT_PROFIT_PER_MONTH)
TEST_PRODUCT_LINK = "https://www.willhaben.at/Link"


def test__given_values__when_constructor__then_instance_with_values():
    product = __test_product()

    assert product._name == TEST_PRODUCT_NAME
    assert product._short_name == ""
    assert product._price == TEST_PRODUCT_PRICE
    assert product._roi == 0
    assert product._link == TEST_PRODUCT_LINK
    assert product._timestamp == TimestampTranslator.text_to_timestamp_or_max_if_not_today("16.12. - 20:37 Uhr")
    assert product._mapped is False
    assert product._time_relevant is False


def test__given_card_name_and_profit_per_month__when_set_product_properties__then_instance_with_new_values():
    product = __test_product()
    product.set_product_properties(TEST_PRODUCT_SHORT_NAME, TEST_PRODUCT_PROFIT_PER_MONTH)

    assert product._short_name == TEST_PRODUCT_SHORT_NAME
    assert product._roi == TEST_PRODUCT_ROI


def test__given_product__when_display_string_colored__then_string_with_values_from_product():
    product = __test_product()
    product.set_product_properties(TEST_PRODUCT_SHORT_NAME, TEST_PRODUCT_PROFIT_PER_MONTH)
    colored = product.display_string_colored()

    assert colored == __expected_display_string_colored()


def __expected_display_string_colored() -> str:
    return "{6}\'{5}\' - {0}{7} - ROI: {3}{1}{4} (Full Name: {2} -> {8})" \
        .format(__expected_price_formatted(TEST_PRODUCT_PRICE),
                __expected_roi_formatted(TEST_PRODUCT_ROI),
                TEST_PRODUCT_NAME,
                BackgroundColors.OKGREEN,
                BackgroundColors.ENDC,
                TEST_PRODUCT_SHORT_NAME,
                BackgroundColors.OKBLUE,
                BackgroundColors.ENDC,
                TEST_PRODUCT_LINK)


def __expected_price_formatted(price) -> str:
    return CurrencyTranslator.int_to_text(price)


def __expected_roi_formatted(roi) -> str:
    return '{0:.2f}'.format(roi)


def test__given_product__when_display_string_uncolored__then_string_with_values_from_product():
    product = __test_product()
    product.set_product_properties(TEST_PRODUCT_SHORT_NAME, TEST_PRODUCT_PROFIT_PER_MONTH)
    uncolored = product.display_string_uncolored()

    assert uncolored == __expected_display_string_uncolored()


def __expected_display_string_uncolored() -> str:
    return "\'{3}\' - {0} - ROI: {1} (Full Name: [{2}]({4}))" \
        .format(__expected_price_formatted(TEST_PRODUCT_PRICE),
                __expected_roi_formatted(TEST_PRODUCT_ROI),
                TEST_PRODUCT_NAME,
                TEST_PRODUCT_SHORT_NAME,
                TEST_PRODUCT_LINK)


def test__given_product_not_mapped__when_mark_as_mapped__then_product_is_marked_as_mapped():
    product = __test_product()
    product.mark_as_mapped()

    assert product._mapped is True


def test__given_product_not_time_relevant__when_mark_as_time_relevant__then_product_is_marked_as_time_relevant():
    product = __test_product()
    __mark_as_time_relevant(product)

    assert product._time_relevant is True


def __mark_as_time_relevant(product):
    product.mark_as_time_relevant(TimestampTranslator.text_to_timestamp_or_max_if_not_today("16.12. - 20:34 Uhr"))


def test__given_product__when_name_lowercase__then_name_as_lowercase():
    product = __test_product()
    name_lowercase = product.name_lowercase()

    assert name_lowercase == product._name.replace(" ", "").lower()


def __test_product() -> Product:
    return Product(TEST_PRODUCT_NAME, TEST_PRODUCT_PRICE_TEXT, "/Link", "16.12. - 20:37 Uhr")


def test__given_product_on_blacklist_words__when_is_blacklisted__then_true():
    product = __test_product()

    blacklist_words = [
        "Name",
        "kaputt",
        "tausch"
    ]

    assert product.is_blacklisted(blacklist_words, []) is True


def test__given_product_not_on_blacklist_words__when_is_blacklisted__then_false():
    product = __test_product()

    blacklist_words = [
        "kaputt",
        "tausch"
    ]

    assert product.is_blacklisted(blacklist_words, []) is False


def test__given_product_on_blacklist__when_is_blacklisted__then_true():
    product = __test_product()

    blacklist = [
        "Name",
        "kaputt",
        "tausch"
    ]

    assert product.is_blacklisted([], blacklist) is True


def test__given_product_not_on_blacklist__when_is_blacklisted__then_false():
    product = __test_product()

    blacklist = [
        "kaputt",
        "tausch"
    ]

    assert product.is_blacklisted([], blacklist) is False


def test__given_mapped_product__when_is_mapped__then_true():
    product = __test_product()
    product.mark_as_mapped()

    assert product.is_mapped() is True


def test__given_not_mapped_product__when_is_mapped__then_false():
    product = __test_product()

    assert product.is_mapped() is False


def test__given_mapped_and_time_relevant_product__when_relevant_for_discord__then_true():
    product = __test_product()
    product.mark_as_mapped()
    __mark_as_time_relevant(product)

    assert product.relevant_for_discord() is True


def test__given_not_mapped_and_time_relevant_product__when_relevant_for_discord__then_false():
    product = __test_product()
    __mark_as_time_relevant(product)

    assert product.relevant_for_discord() is False


def test__given_mapped_and_not_time_relevant_product__when_relevant_for_discord__then_false():
    product = __test_product()
    product.mark_as_mapped()

    assert product.relevant_for_discord() is False


def test__given_not_mapped_and_not_time_relevant_product__when_relevant_for_discord__then_false():
    product = __test_product()

    assert product.relevant_for_discord() is False

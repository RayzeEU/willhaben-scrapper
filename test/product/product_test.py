from src.background_colors import BackgroundColors
from src.product.product import Product
from src.translator.currency_translator import CurrencyTranslator
from src.translator.timestamp_translator import TimestampTranslator


def test__given_values__when_constructor__then_instance_with_values():
    product = __test_product()

    assert product._name == "Name"
    assert product.short_name == ""
    assert product.price == CurrencyTranslator.text_to_int("199")
    assert product.roi == 0
    assert product.link == "https://www.willhaben.at/Link"
    assert product.timestamp == TimestampTranslator.text_to_timestamp_or_max_if_not_today("16.12. - 20:37 Uhr")
    assert product.mapped is False
    assert product.time_relevant is False


def test__given_card_name_and_profit_per_month__when_set_product_properties__then_instance_with_new_values():
    product = __test_product()
    card_name = "Card name"
    product.set_product_properties(card_name, 20.0)

    assert product.short_name == card_name
    assert product.roi == (float(product.price) / 20)


def test__given_product__when_display_string_colored__then_string_with_values_from_product():
    product = __test_product()
    colored = product.display_string_colored()

    assert colored == __expected_display_string_colored(product)


def __expected_display_string_colored(product: Product) -> str:
    return "{6}\'{5}\' - {0}{7} - ROI: {3}{1}{4} (Full Name: {2} -> {8})" \
        .format(__expected_price_formatted(product.price),
                __expected_roi_formatted(product.roi),
                "Name",
                BackgroundColors.OKGREEN,
                BackgroundColors.ENDC,
                product.short_name,
                BackgroundColors.OKBLUE,
                BackgroundColors.ENDC,
                product.link)


def __expected_price_formatted(price) -> str:
    return CurrencyTranslator.int_to_text(price)


def __expected_roi_formatted(roi) -> str:
    return '{0:.2f}'.format(roi)


def test__given_product__when_display_string_uncolored__then_string_with_values_from_product():
    product = __test_product()
    uncolored = product.display_string_uncolored()

    assert uncolored == __expected_display_string_uncolored(product)


def __expected_display_string_uncolored(product: Product) -> str:
    return "\'{3}\' - {0} - ROI: {1} (Full Name: {2} -> {4})" \
        .format(__expected_price_formatted(product.price),
                __expected_roi_formatted(product.roi),
                "Name",
                product.short_name,
                product.link)


def test__given_product_not_mapped__when_mark_as_mapped__then_product_is_marked_as_mapped():
    product = __test_product()
    product.mark_as_mapped()

    assert product.mapped is True


def test__given_product_not_time_relevant__when_mark_as_time_relevant__then_product_is_marked_as_time_relevant():
    product = __test_product()
    product.mark_as_time_relevant()

    assert product.time_relevant is True


def test__given_product__when_name_lowercase__then_name_as_lowercase():
    product = __test_product()
    name_lowercase = product.name_lowercase()

    assert name_lowercase == product._name.replace(" ", "").lower()


def __test_product() -> Product:
    return Product("Name", "199", "/Link", "16.12. - 20:37 Uhr")


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

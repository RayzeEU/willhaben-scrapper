from src.background_colors import BackgroundColors
from src.product.product import Product
from src.translator.currency_translator import CurrencyTranslator


TEST_PRODUCT_SHORT_NAME = "Card name"
TEST_PRODUCT_NAME = "Name"
TEST_PRODUCT_PRICE = 199
TEST_PRODUCT_PROFIT_PER_MONTH = 20.0
TEST_PRODUCT_ROI = (float(TEST_PRODUCT_PRICE) / TEST_PRODUCT_PROFIT_PER_MONTH)
TEST_PRODUCT_LINK = "https://www.willhaben.at/Link"


def test__given_values__when_constructor__then_instance_with_values():
    product = __test_product(True, True)

    assert product._name == TEST_PRODUCT_NAME
    assert product._short_name == TEST_PRODUCT_SHORT_NAME
    assert product._price == TEST_PRODUCT_PRICE
    assert product._profit_per_month == TEST_PRODUCT_PROFIT_PER_MONTH
    assert product._link == TEST_PRODUCT_LINK
    assert product._mapped is True
    assert product.is_mapped() is True
    assert product._time_relevant is True


def __test_product(mapped: bool = False, time_relevant: bool = False, price: int = TEST_PRODUCT_PRICE, profit_per_month: float = TEST_PRODUCT_PROFIT_PER_MONTH) -> Product:
    return Product(TEST_PRODUCT_NAME, TEST_PRODUCT_SHORT_NAME, price, profit_per_month, TEST_PRODUCT_LINK, mapped, time_relevant)


def test__given_product__when_display_string_colored__then_string_with_values_from_product():
    product = __test_product()
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
    uncolored = product.display_string_uncolored()

    assert uncolored == __expected_display_string_uncolored()


def __expected_display_string_uncolored() -> str:
    return "\'{3}\' - {0} - ROI: {1} (Full Name: [{2}]({4}))" \
        .format(__expected_price_formatted(TEST_PRODUCT_PRICE),
                __expected_roi_formatted(TEST_PRODUCT_ROI),
                TEST_PRODUCT_NAME,
                TEST_PRODUCT_SHORT_NAME,
                TEST_PRODUCT_LINK)


def test__given_mapped_and_time_relevant_product__when_relevant_for_discord__then_true():
    product = __test_product(True, True)

    assert product.relevant_for_discord() is True


def test__given_not_mapped_and_time_relevant_product__when_relevant_for_discord__then_false():
    product = __test_product(False, True)

    assert product.relevant_for_discord() is False


def test__given_mapped_and_not_time_relevant_product__when_relevant_for_discord__then_false():
    product = __test_product(True, False)

    assert product.relevant_for_discord() is False


def test__given_not_mapped_and_not_time_relevant_product__when_relevant_for_discord__then_false():
    product = __test_product()

    assert product.relevant_for_discord() is False


def test__given_product_without_profit_per_month__when_roi__then_0():
    product = __test_product(profit_per_month=0)

    assert product.roi() == 0.0


def test__given_product_without_price__when_roi__then_0():
    product = __test_product(price=0)

    assert product.roi() == 0.0


def test__given_product_with_price_and_profit_per_month__when_roi__then_right_roi():
    product = __test_product(price=100, profit_per_month=10)

    assert product.roi() == 10.0

from src.translator.timestamp_translator import TimestampTranslator


def test__given_date_string_for_today__when_text_to_timestamp_or_max_if_not_today__then_right_date():
    datetime = TimestampTranslator.text_to_timestamp_or_max_if_not_today("Heute, 21:18 Uhr")
    assert datetime == datetime.today().replace(hour=21, minute=18, second=0, microsecond=0)


def test__given_date_string_for_today_without_text_uhr__when_text_to_timestamp_or_max_if_not_today__then_right_date():
    datetime = TimestampTranslator.text_to_timestamp_or_max_if_not_today("Heute, 21:18")
    assert datetime == datetime.today().replace(hour=21, minute=18, second=0, microsecond=0)


def test__given_invalid_date_string_for_today__when_text_to_timestamp_or_max_if_not_today__then_exception():
    datetime = TimestampTranslator.text_to_timestamp_or_max_if_not_today("Heute, 121:18")
    assert datetime == datetime.max


def test__given_date_string_not_for_today__when_text_to_timestamp_or_max_if_not_today__then_right_date():
    datetime = TimestampTranslator.text_to_timestamp_or_max_if_not_today("16.12. - 20:37 Uhr")
    assert datetime == datetime.today().replace(month=12, day=16, hour=20, minute=37, second=0, microsecond=0)


def test__given_date_string_not_for_today_without_text_uhr__when_text_to_timestamp_or_max_if_not_today__then_right_date():
    datetime = TimestampTranslator.text_to_timestamp_or_max_if_not_today("16.12. - 20:37")
    assert datetime == datetime.today().replace(month=12, day=16, hour=20, minute=37, second=0, microsecond=0)


def test__given_invalid_date_string_not_for_today__when_text_to_timestamp_or_max_if_not_today__then_exception():
    datetime = TimestampTranslator.text_to_timestamp_or_max_if_not_today("16.12. - 200:37 Uhr")
    assert datetime == datetime.max

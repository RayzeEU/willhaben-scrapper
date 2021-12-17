import logging
from datetime import date, datetime


class TimestampTranslator:
    @staticmethod
    def text_to_timestamp_or_max_if_not_today(timestamp_text: str) -> datetime:
        if "Heute" in timestamp_text:
            return TimestampTranslator.__convert_text_to_timestamp_for_today(timestamp_text)
        else:
            return TimestampTranslator.__convert_text_to_timestamp_not_for_today(timestamp_text)

    @staticmethod
    def __convert_text_to_timestamp_not_for_today(timestamp_text: str) -> datetime:
        try:
            return datetime.strptime(timestamp_text.replace(" Uhr", ""), "%d.%m. - %H:%M").replace(year=datetime.today().year)
        except ValueError:
            logging.error("Failed to parse date " + timestamp_text)
            return datetime.max

    @staticmethod
    def __convert_text_to_timestamp_for_today(timestamp_text: str) -> datetime:
        try:
            return datetime.strptime(timestamp_text.replace("Heute, ", date.today().strftime("%d.%m.%Y - ")).replace(" Uhr", ""), "%d.%m.%Y - %H:%M")
        except ValueError:
            logging.error("Failed to parse date " + timestamp_text)
            return datetime.max

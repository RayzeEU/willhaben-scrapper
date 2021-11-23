from datetime import date, datetime


class TimestampTranslator:
    @staticmethod
    def text_to_timestamp_or_max_if_not_today(timestamp_text):
        if "Heute" in timestamp_text:
            return TimestampTranslator.__convert_text_to_timestamp_for_today(timestamp_text)
        else:
            timestamp_text = timestamp_text + str(datetime.today().year)
            return datetime.strptime(timestamp_text.replace(" Uhr", ""), "%d.%m. - %H:%M%Y")

    @staticmethod
    def __convert_text_to_timestamp_for_today(timestamp_text):
        return datetime.strptime(timestamp_text.replace("Heute, ", date.today().strftime("%d.%m.%Y - ")).replace(" Uhr", ""), "%d.%m.%Y - %H:%M")

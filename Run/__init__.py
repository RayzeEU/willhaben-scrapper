import datetime
import logging
import json

import azure.functions as func

from src.poller import PagePoller


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    logging.info("reading config ...")
    with open("resources/config.json") as config_json:
        config = json.load(config_json)

    PagePoller(True, False, config).check_website()

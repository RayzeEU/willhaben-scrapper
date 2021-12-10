import json
import logging
import os

from src.poller import PagePoller

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("reading private config ...")
    with open("../resources/private_config.json") as private_config_json:
        private_config = json.load(private_config_json)
        os.environ["Discord_Latest_Cards"] = private_config["Discord_Latest_Cards"]
        os.environ["Discord_Bot_Status"] = private_config["Discord_Bot_Status"]

    logging.info("reading config ...")
    with open("../resources/config.json") as config_json:
        config = json.load(config_json)

    PagePoller(True, config).check_website()


if __name__ == '__main__':
    main()

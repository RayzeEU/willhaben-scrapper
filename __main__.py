import configparser
import os
import json
import time

from src.poller import PagePoller
from discord import Webhook, RequestsWebhookAdapter

PRIVATE_CONFIG_FILE = "private.config"

print(os.path.join(os.path.dirname(__file__), PRIVATE_CONFIG_FILE))
private_config = configparser.ConfigParser()
private_config.read(os.path.join(os.path.dirname(__file__), PRIVATE_CONFIG_FILE))

webhook = Webhook.from_url(private_config.get('Webhooks', 'bot-status'), adapter=RequestsWebhookAdapter())

print("reading config ...")
with open("config.json") as config_json:
    config = json.load(config_json)

pagepoller = PagePoller(False, False, True, private_config, config)

while True:
    webhook.send("Running...")

    pagepoller.check_website()

    time.sleep(30)

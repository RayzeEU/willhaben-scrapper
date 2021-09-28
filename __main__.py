import configparser
import os
from src.poller import PagePoller
from discord import Webhook, RequestsWebhookAdapter

import time

PRIVATE_CONFIG_FILE = "private.config"

print(os.path.join(os.path.dirname(__file__), PRIVATE_CONFIG_FILE))
private_config = configparser.ConfigParser()
private_config.read(os.path.join(os.path.dirname(__file__), PRIVATE_CONFIG_FILE))

webhook = Webhook.from_url(private_config.get('Webhooks', 'bot-status'), adapter=RequestsWebhookAdapter())

while True:
    webhook.send("Running...")

    pagepoller = PagePoller(False, True, True, private_config)
    pagepoller.check_website()

    time.sleep(30)

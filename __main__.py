import configparser
import os
import json
import time
import requests

from src.poller import PagePoller
from discord import Webhook, RequestsWebhookAdapter

PRIVATE_CONFIG_FILE = "private.config"

print(os.path.join(os.path.dirname(__file__), PRIVATE_CONFIG_FILE))
private_config = configparser.ConfigParser()
private_config.read(os.path.join(os.path.dirname(__file__), PRIVATE_CONFIG_FILE))

webhook = Webhook.from_url(private_config.get('Webhooks', 'bot-status'), adapter=RequestsWebhookAdapter())

print("reading config ...")
with open("resources/config.json") as config_json:
    config = json.load(config_json)

# ETH data
eth_data = requests.get("https://api.minerstat.com/v2/coins?list=eth").json()[0]
difficulty = eth_data["difficulty"]
reward = eth_data["reward_block"]
price = eth_data["price"]

# actual hashrate (all 4 cards together)
hash_rate = 141880000

# ((hash_rate [h/s] * reward) / difficulty) * (1 - pool_fee) * 3600 * 24
dollar_per_day = ((hash_rate * reward) / difficulty) * (1 - 0.02) * 3600 * 24 * price
print(dollar_per_day)

pagepoller = PagePoller(False, True, True, private_config, config)

while True:
    webhook.send("Running...")

    pagepoller.check_website()

    time.sleep(30)

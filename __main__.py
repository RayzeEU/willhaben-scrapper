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

price_kWh = 0.11

# actual mega hash rate (all 4 cards together)
mega_hash_rate = 141.88
watt = 325

# efficiency on NiceHash
efficiency = mega_hash_rate / watt
print(efficiency)

# ETH data from https://api.minerstat.com/
eth_data = requests.get("https://api.minerstat.com/v2/coins?list=eth").json()[0]
difficulty = eth_data["difficulty"]
reward = eth_data["reward_block"]
price = eth_data["price"]

# ((hash_rate [h/s] * reward) / difficulty) * (1 - pool_fee) * 3600 * 24
dollar_per_day = ((mega_hash_rate * 1000000 * reward) / difficulty) * (1 - 0.02) * 3600 * 24 * price
print(dollar_per_day)

# actual watt consumption (all 4 cards together)
kWh = watt * 24 / 1000
price = price_kWh * kWh
print(price)

pagepoller = PagePoller(False, True, True, private_config, config)

while True:
    webhook.send("Running...")

    pagepoller.check_website()

    time.sleep(30)

import logging
import requests

price_kWh = 0.19

# actual mega hash rate (all 4 cards together)
mega_hash_rate = 196.5
watt = 452

# efficiency on NiceHash
efficiency = mega_hash_rate / watt
logging.info("efficiency: {0} MH/J".format(round(efficiency, 4)))

# ETH data from https://api.minerstat.com/
eth_data = requests.get("https://api.minerstat.com/v2/coins?list=eth").json()[0]
difficulty = eth_data["difficulty"]
reward = eth_data["reward_block"]
price = eth_data["price"] / 1.16

# ((hash_rate [h/s] * reward) / difficulty) * (1 - pool_fee) * 3600 * 24
dollar_per_day = ((mega_hash_rate * 1000000 * reward) / difficulty) * (1 - 0.02) * 3600 * 24 * price
logging.info("daily: {0} €".format(round(dollar_per_day, 2)))

# actual watt consumption (all 4 cards together)
kWh = watt * 24 / 1000
price = price_kWh * kWh
logging.info("electricity daily: {0} €".format(round(price, 2)))

logging.info("daily after electricity: {0} €".format(round(dollar_per_day - price, 2)))
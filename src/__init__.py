from src.poller import PagePoller
from discord import Webhook, RequestsWebhookAdapter

import time

webhook = Webhook.from_url("https://discord.com/api/webhooks/[webhookUrl]", adapter=RequestsWebhookAdapter())
    
while True:
    webhook.send("Running...")

    pagepoller = PagePoller(1, True, True, True)
    pagepoller.check_website()

    time.sleep(180)
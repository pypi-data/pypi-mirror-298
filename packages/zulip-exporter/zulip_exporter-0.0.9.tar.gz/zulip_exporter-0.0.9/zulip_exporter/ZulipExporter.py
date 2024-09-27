import zulip
import logging
from os import environ
from sys import exit
from time import sleep
from prometheus_client import start_http_server, REGISTRY
from zulip_exporter import InfoCollector
from zulip_exporter import UserCollector
from zulip_exporter import SubscriptionCollector


httpport = environ.get('PORT', 9863)
frequency = environ.get('SLEEP', 120)
client = zulip.Client()

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def ZulipExporter():
  try:
    logging.info('Starting..')
    logging.info('Grabbing metrics..')
    REGISTRY.register(SubscriptionCollector())
    REGISTRY.register(InfoCollector())
    REGISTRY.register(UserCollector())
    start_http_server(int(httpport))
    while True:
      sleep(int(frequency))
  except KeyboardInterrupt:
    logging.info("Exit, keyboard interrupt")
    exit(0)

if __name__ == "__main__":
  ZulipExporter()
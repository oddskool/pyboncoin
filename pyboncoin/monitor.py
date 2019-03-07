import sys
import asyncio
import configparser
from datetime import datetime

from pyboncoin.browser import crawl
from pyboncoin.db import DB
from pyboncoin.mailer import send_mail
from pyboncoin.parser import parse

print("<<<", datetime.now())

config_file = sys.argv[1]
config = configparser.RawConfigParser()
config.read(config_file)

db = DB(config.get('database', 'filename'),
        config.get('database', 'reset', fallback=False))

for query, url in config.items('urls'):
    new_offers = []
    print("crawling", query)
    content = asyncio.get_event_loop().run_until_complete(crawl(url))
    offers = parse(content)
    print("read", len(offers), "offers")
    for offer in offers:
        if offer.url in db:
            pass
        else:
            db[offer.url] = offer
            new_offers.append(offer)
    print(len(new_offers), "new offers")
    db.save()
    if config.get('mailer', 'send', fallback=True) != 'false':
        send_mail(query, new_offers, dict(config.items('mailer')))

print(">>>")



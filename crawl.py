#!/usr/bin/python
import os, sys

from seosnap_cachewarmer import logging
import logging
from scrapy.cmdline import execute
from dotenv import load_dotenv

from seosnap_cachewarmer.service import SeosnapService

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# TODO: make formal cli (using click?)
if len(sys.argv) < 2: raise Exception('Missing website_id as argument')

if sys.argv[1] == 'clean':
    if len(sys.argv) < 3: raise Exception('Missing website_id as argument')
    service = SeosnapService()
    for website_id in sys.argv[2].split(','): service.clean_queue(int(website_id))
    logging.info(f'Cleaned the queue for websites: {sys.argv[2]}')
else:
    for website_id in sys.argv[1].split(','):
        execute(argv=[sys.argv[0], 'crawl', 'Seosnap', '-a', f'website_id={sys.argv[1]}'] + sys.argv[2:])

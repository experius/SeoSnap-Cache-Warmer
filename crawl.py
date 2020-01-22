#!/usr/bin/python
import os, sys

from seosnap_cachewarmer import logging
from scrapy.cmdline import execute
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

if len(sys.argv) < 2: raise Exception('Missing website_id as argument')
execute(argv=[sys.argv[0], 'crawl', 'Seosnap', '-a', f'website_id={sys.argv[1]}'] + sys.argv[2:])

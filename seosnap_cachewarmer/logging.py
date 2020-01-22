import logging
import os

from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs/cachewarmer.log'),
    level=os.getenv('CACHEWARMER_LOG_LEVEL')
)

#!/usr/bin/python
import os, sys, logging

import requests
import click
from functools import reduce
from dotenv import load_dotenv
from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from seosnap_cachewarmer.service import SeosnapService
from seosnap_cachewarmer.spider import SeosnapSpider
# from seosnap_cachewarmer.tagSpider import SeosnapTagSpider
from seosnap_cachewarmer.state import SeosnapState
from seosnap_cachewarmer.sitemap import SeoSnapSitemapRefresher
import xml.etree.ElementTree as ET

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
configure_logging(install_root_handler=False)
logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs/cachewarmer.log'),
    level=os.getenv('CACHEWARMER_LOG_LEVEL')
)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('website_ids')
def load(website_ids: str, **args):
    for website_id in website_ids.split(','):
        click.echo(f'Loading website: {website_id}')
        arg_tokens = reduce(lambda x, y: x + y, [['-a', f'{k}={v}'] for k, v in args.items()])
        execute(argv=[sys.argv[0], 'crawl', 'Seosnap', '-a', f'website_id={website_id}'] + arg_tokens)


# @cli.command()
# @click.argument('website_ids')
# @click.argument('tag')
# def tag(website_ids: str, tag: str, **args):
#     print("-- start recacheByTag --")
#     print("test1 ckasdhlasd")
#     print(website_ids)
#     print(tag)
#
#     try:
#         settings = get_project_settings()
#         process = CrawlerProcess(settings)
#         for website_id in website_ids.split(','):
#             process.crawl(
#                 SeosnapTagSpider,
#                 website_id=website_id,
#                 tag=tag,
#                 **args
#             )
#         process.start()
#     except Exception as e:
#         click.echo(str(e), err=True)



@cli.command()
@click.argument('website_ids')
@click.option('--follow_next', type=bool, default=True, help='Follows rel-next links if enabled')
@click.option('--recache', type=bool, default=True, help='Recached all pages instead of not yet cached ones')
@click.option('--clean_old_pages_after', type=bool, default=False, help='Remove all pages where updated_at lower then the start of the finished crawl')
@click.option('--use_queue', type=bool, default=False, help='Cache urls from the queue instead of the sitemap')
@click.option('--mobile', type=bool, default=False, help='Whether a mobile version should be rendered instead')
def cache(website_ids: str, **args):
    try:
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        for website_id in website_ids.split(','):
            process.crawl(
                SeosnapSpider,
                website_id=website_id,
                **args
            )
        process.start()
    except Exception as e:
        click.echo(str(e), err=True)


@cli.command()
@click.argument('website_id')
def sync(website_id: str, *args, **kwargs):
    print('Start test')
    service = SeosnapService()
    service.sync_pages(website_id)


@cli.command()
@click.argument('website_ids')
def clean(website_ids: str):
    service = SeosnapService()
    for website_id in website_ids.split(','):
        service.clean_queue(int(website_id))
        logging.info(f'Cleaned the queue for website: {website_id}')
    click.echo(f'Cleaned the queue for websites: {website_ids}')


if __name__ == '__main__':
    cli()

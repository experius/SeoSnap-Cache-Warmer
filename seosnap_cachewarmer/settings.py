import os

ITEM_PIPELINES = {
    'seosnap_cachewarmer.pipelines.SeosnapPipeline': 100
}

SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': None,
}

DOWNLOADER_MIDDLEWARES = {
    'seosnap_cachewarmer.middleware.CacheServerMiddleware': 543,
    'seosnap_cachewarmer.middleware.ErrorMiddleware': 543,
}

USER_AGENT = os.getenv('CACHEWARMER_USER_AGENT', 'Seosnap')
REACTOR_THREADPOOL_MAXSIZE = os.getenv('CACHEWARMER_THREADS', 16)
CONCURRENT_REQUESTS = os.getenv('CACHEWARMER_CONCURRENT_REQUESTS', 16)
SPIDER_MODULES = ['seosnap_cachewarmer.spider']

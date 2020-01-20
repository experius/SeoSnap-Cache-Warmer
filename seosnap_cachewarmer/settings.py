ITEM_PIPELINES = {
    'seosnap_cachewarmer.pipelines.SeosnapPipeline': 100
}

USER_AGENT = 'Seosnap'
SPIDER_MODULES = ['seosnap_cachewarmer.spider']

# Seosnap Cache Warmer

```
cp .env.example .env
# Edit default settings

docker-compose up -d --build
```

# Commands
### Cache
Handles caching of pages associated to given website
```
Usage: crawl.py cache [OPTIONS] WEBSITE_IDS

Options:
  --follow_next BOOLEAN  Follows rel-next links if enabled
  --recache BOOLEAN      Recached all pages instead of not yet cached ones
  --use_queue BOOLEAN    Cache urls from the queue instead of the sitemap
  --load BOOLEAN         Whether already loaded urls should be scraped instead
  --clean_old_pages_after BOOLEAN Remove all pages where updated_at lower then the start of the finished crawl
  --help                 Show this message and exit.
```

### Clean
Handles cleaning of the dashboard queue
```
Usage: crawl.py clean [OPTIONS] WEBSITE_IDS

Options:
  --help  Show this message and exit.
```

# Examples
```
# Cache the sitemap of website 1
docker-compose run cachewarmer cache 1

# Cache requests in queue for websites 1 and 2
 dc run cachewarmer cache 1,2 use_queue=true

# Clean the queue for websites 1 and 2
docker-compose run cachewarmer clean 1,2
```

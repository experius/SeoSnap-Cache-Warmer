# Seosnap Cache Warmer

```
cp .env.example .env
# Edit default settings

docker-compose up -d --build
```

# Examples
```
# Cache the sitemap of website 1
docker-compose run cachewarmer 1

# Cache requests in queue for websites 1 and 2
 dc run cachewarmer 1,2 -a use_queue=true

# Clean the queue for websites 1 and 2
docker-compose run cachewarmer clean 1,2
```
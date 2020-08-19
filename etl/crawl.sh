#!/bin/sh

source .venv/bin/activate

scrapy crawl serlo_spider &
scrapy crawl leifi_spider &
scrapy crawl planet_schule_spider &
scrapy crawl tutory_spider &
scrapy crawl br_rss_spider &
scrapy crawl zdf_rss_spider &
scrapy crawl digitallearninglab_spider &
scrapy crawl geogebra_spider &
scrapy crawl memucho_spider &
scrapy crawl wirlernenonline_spider &
scrapy crawl irights_spider &
scrapy crawl rlp_spider &
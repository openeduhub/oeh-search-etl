import os
import random
import sys
from pathlib import Path
import django
django_root = Path(__file__).resolve().parents[1]
sys.path.append(str(django_root))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler_ui.settings")
django.setup()


from crawls.models import CrawlJob, CrawledURL
from scripts.radix import RadixTree

def main():
    # job = CrawlJob.objects.get(pk=9)
    job = CrawlJob.objects.get(pk=6)
    urls = CrawledURL.objects.filter(crawl_job=job)
    
    # # generate 100 unique random numbers in range(0, len(urls))
    # indexes = set()
    # while len(indexes) < 100:
    #     indexes.add(random.randint(0, len(urls)))
    
    # # print the urls at the generated indexes
    # for i in indexes:
    #     print(urls[i].url)

    for url in urls[:100]:
        print(url.url)
    

if __name__ == "__main__":
    main()
import os
import sys
from pathlib import Path
import django
django_root = Path(__file__).resolve().parents[1]
sys.path.append(str(django_root))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler_ui.settings")
django.setup()


from crawls.models import CrawlJob, CrawledURL

def main():
    job = CrawlJob.objects.get(pk=6)
    urls = CrawledURL.objects.filter(crawl_job=job)
    # for url in urls[0:10]:
    #     print(url.url)
    
    find_patterns(u.url for u in urls[:10000])


def find_patterns(incoming_urls):
    urls = {}
    # make the tree
    for url in incoming_urls:
        atype = None
        # url, atype = line.strip().split("____")  # assuming incoming_urls is a list with each entry of type url__class
        if len(url) < 100:   # Take only the initial 100 characters to avoid building a sparse tree
            bound = len(url) + 1
        else:
            bound = 101
        for x in range(1, bound):
            prefix = url[:x].lower()
            if prefix not in urls:
                urls[prefix] = {'positive': 0, 'negative': 0, 'total': 0}
            if atype:
                urls[prefix][atype] += 1
            urls[prefix]['total'] += 1

    new_urls = {}
    # prune the tree
    for url, data in urls.items():
        if data['total'] < 5:  # For something to be called as common pattern, there should be at least 5 occurrences of it.
            continue
        data['negative_percentage'] = (float(data['negative']) * 100) / data['total']
        # if data['negative_percentage'] < 85.0: # Assuming I am interested in finding url patterns for negative class
        #     continue
        length = len(url)
        found = False
        # iterate to see if a len+1 url is present with same total count
        for second, seconddata in urls.items():
            if len(second) <= length:
                continue
            if url == second[:length] and data['total'] == seconddata['total']:
                found = True
                break
        # discard urls with length less than 20
        if not found: #  and len(url) > 20:
            new_urls[url] = data

    print("URL Pattern; Positive; Negative; Total; Negative (%)")
    for url, data in new_urls.items():
        print("%s; %d; %d; %d; %.2f" % (
            url, data['positive'], data['negative'], data['total'],
            data['negative_percentage']))

    # example prefix:
    # https://www.weltderphysik.de/gebiet/te; 0; 0; 161; 0.00
    # we want to find:
    # https://www.weltderphysik.de/gebiet/teilchen/; 0; 0; 117; 0.00
    # https://www.weltderphysik.de/gebiet/technik/; 0; 0; 44; 0.00
    # 117 + 44 = 161
    # so this one can be decomposed into to categories.
    # If the number of parts is low, then it is likely not a good prefix.
    search = "https://www.weltderphysik.de/gebiet/te"
    for url, data in new_urls.items():
        if url.startswith(search):
            print("Candidate:", url, data['total'])

if __name__ == "__main__":
    main()
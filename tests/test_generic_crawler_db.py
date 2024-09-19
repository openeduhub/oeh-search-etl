import sqlite3

from pytest import fixture

from converter.util.generic_crawler_db import fetch_urls_passing_filterset

@fixture
def example_db():
    """ Provides an example database with some test data. """

    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE "crawls_crawledurl" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(200) NOT NULL, "content" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "crawl_job_id" integer NOT NULL REFERENCES "crawls_crawljob" ("id") DEFERRABLE INITIALLY DEFERRED);
        CREATE TABLE "crawls_crawljob" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "start_url" varchar(200) NOT NULL, "follow_links" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
        CREATE TABLE "crawls_filterrule" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rule" text NOT NULL, "include" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "page_type" varchar(255) NOT NULL, "count" integer NOT NULL, "filter_set_id" integer NOT NULL REFERENCES "crawls_filterset" ("id") DEFERRABLE INITIALLY DEFERRED, "position" integer NOT NULL, "cumulative_count" integer NOT NULL);
        CREATE TABLE "crawls_filterset" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "crawl_job_id" integer NOT NULL REFERENCES "crawls_crawljob" ("id") DEFERRABLE INITIALLY DEFERRED, "remaining_urls" integer NOT NULL);
        
        INSERT INTO "crawls_filterset" ("id", "name", "created_at", "updated_at", "crawl_job_id", "remaining_urls") VALUES ('1', 'Test', '2024-06-14 08:29:08.592996', '2024-06-16 17:48:20.544330', '6', '18');
        INSERT INTO "crawls_crawljob" ("id", "start_url", "follow_links", "created_at", "updated_at") VALUES ('6', 'https://weltderphysik.de', '1', '2024-06-12 11:41:37.056465', '2024-06-12 11:41:37.058759');

        INSERT INTO "crawls_crawledurl" ("id", "url", "content", "created_at", "updated_at", "crawl_job_id") VALUES ('2', 'https://www.weltderphysik.de/', '', '2024-06-12 08:18:32.200353', '2024-06-12 08:18:32.200998', '6');
        INSERT INTO "crawls_crawledurl" ("id", "url", "content", "created_at", "updated_at", "crawl_job_id") VALUES ('3', 'https://www.weltderphysik.de/service/suche/', '', '2024-06-12 08:18:32.201805', '2024-06-12 08:18:32.202410', '6');
        INSERT INTO "crawls_crawledurl" ("id", "url", "content", "created_at", "updated_at", "crawl_job_id") VALUES ('6', 'https://www.weltderphysik.de/vor-ort/veranstaltungen/', '', '2024-06-12 08:18:32.206043', '2024-06-12 08:18:32.206612', '6');
        INSERT INTO "crawls_crawledurl" ("id", "url", "content", "created_at", "updated_at", "crawl_job_id") VALUES ('7', 'https://www.weltderphysik.de/vor-ort/physikatlas/', '', '2024-06-12 08:18:32.207530', '2024-06-12 08:18:32.208589', '6');
        INSERT INTO "crawls_crawledurl" ("id", "url", "content", "created_at", "updated_at", "crawl_job_id") VALUES ('8', 'https://www.weltderphysik.de/wir/', '', '2024-06-12 08:18:32.209382', '2024-06-12 08:18:32.209968', '6');
        INSERT INTO "crawls_crawledurl" ("id", "url", "content", "created_at", "updated_at", "crawl_job_id") VALUES ('9', 'https://www.weltderphysik.de/gebiet/teilchen/', '', '2024-06-12 08:18:32.210931', '2024-06-12 08:18:32.211555', '6');
        INSERT INTO "crawls_crawledurl" ("id", "url", "content", "created_at", "updated_at", "crawl_job_id") VALUES ('10', 'https://www.weltderphysik.de/gebiet/materie/', '', '2024-06-12 08:18:32.212289', '2024-06-12 08:18:32.213041', '6');
        INSERT INTO "crawls_crawledurl" ("id", "url", "content", "created_at", "updated_at", "crawl_job_id") VALUES ('11', 'https://www.weltderphysik.de/gebiet/leben/', '', '2024-06-12 08:18:32.213997', '2024-06-12 08:18:32.214522', '6');    

        INSERT INTO "crawls_filterrule" ("id", "rule", "include", "created_at", "updated_at", "page_type", "count", "filter_set_id", "position", "cumulative_count") VALUES ('33', 'https://www.weltderphysik.de/service', '1', '2024-06-16 19:00:11.295706', '2024-09-19 07:10:14.009816', 'Service', '254', '1', '1', '254');
        INSERT INTO "crawls_filterrule" ("id", "rule", "include", "created_at", "updated_at", "page_type", "count", "filter_set_id", "position", "cumulative_count") VALUES ('38', 'https://www.weltderphysik.de/vor-ort/veranstaltungen', '0', '2024-06-17 07:00:57.214537', '2024-06-19 11:49:12.969491', '?', '135', '1', '6', '135');
        INSERT INTO "crawls_filterrule" ("id", "rule", "include", "created_at", "updated_at", "page_type", "count", "filter_set_id", "position", "cumulative_count") VALUES ('41', 'https://www.weltderphysik.de/vor-ort', '1', '2024-06-19 12:28:24.250090', '2024-08-09 09:24:41.947964', 'Videos', '114', '1', '7', '114');
        INSERT INTO "crawls_filterrule" ("id", "rule", "include", "created_at", "updated_at", "page_type", "count", "filter_set_id", "position", "cumulative_count") VALUES ('42', 'https://www.weltderphysik.de/wir', '0', '2024-06-19 12:28:42.174048', '2024-08-09 09:24:41.953452', 'New row', '949', '1', '8', '835');
        INSERT INTO "crawls_filterrule" ("id", "rule", "include", "created_at", "updated_at", "page_type", "count", "filter_set_id", "position", "cumulative_count") VALUES ('44', 'https://www.weltderphysik.de/gebiet', '1', '2024-09-02 09:25:01.330596', '2024-09-02 09:51:29.487508', 'New row', '19', '1', '9', '19');

        -- an empty filterset (#2):
        INSERT INTO "crawls_filterset" ("id", "name", "created_at", "updated_at", "crawl_job_id", "remaining_urls") VALUES ('2', 'Test', '2024-06-14 08:29:08.592996', '2024-06-16 17:48:20.544330', '6', '18')
    ''')

    conn.commit()
    yield conn
    conn.close()


def test_inclusion(example_db):
    passing = fetch_urls_passing_filterset(example_db, 1)
    passing_urls = [url[0] for url in passing]

    assert 'https://www.weltderphysik.de/service/suche/' in passing_urls
    assert 'https://www.weltderphysik.de/vor-ort/physikatlas/' in passing_urls
    assert 'https://www.weltderphysik.de/gebiet/teilchen/' in passing_urls
    assert 'https://www.weltderphysik.de/gebiet/materie/' in passing_urls
    assert 'https://www.weltderphysik.de/gebiet/leben/' in passing_urls


def test_exclusion(example_db):
    passing = fetch_urls_passing_filterset(example_db, 1)
    passing_urls = [url[0] for url in passing]

    assert 'https://www.weltderphysik.de/' not in passing_urls
    assert 'https://www.weltderphysik.de/vor-ort/veranstaltungen/' not in passing_urls
    assert 'https://www.weltderphysik.de/wir/' not in passing_urls


def test_empty_filterset(example_db):
    passing = fetch_urls_passing_filterset(example_db, 2)
    assert len(passing) == 0
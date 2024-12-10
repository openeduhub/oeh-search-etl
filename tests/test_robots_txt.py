import pytest
import requests

from converter.util.robots_txt import fetch_robots_txt, is_ai_usage_allowed


class MockResponseURLNotFound:
    """Mocks a ``requests.Response`` object for an unavailable URL."""

    status_code = 404
    reason = "Not Found"

    @staticmethod
    def get():
        return None


class MockResponseRestrictive:
    """Mocks a ``requests.Response`` object for a website with a restrictive ``robots.txt`` file."""

    # this example was inspired by https://schule.uni-erfurt.de/robots.txt
    # (which is part of the OERSI dataset, provided by "digiLL")
    status_code = 200
    reason = "OK"
    text = """
User-agent: *
Disallow: /
    """

    @staticmethod
    def get(*args, **kwargs):
        return MockResponseRestrictive()


class MockResponseRestrictiveMixed:
    """Mocks a ``requests.Response`` object for a restrictive ``robots.txt`` file
    that generally disallows any robots from doing anything, but allows some AI user agents.
    """

    status_code = 200
    reason = "OK"
    text = """
User-agent: *
Disallow: /

User-agent: anthropic-ai
Disallow: 

User-agent: ChatGPT-User
Disallow: /
    """

    @staticmethod
    def get(*args, **kwargs):
        return MockResponseRestrictiveMixed()


class MockResponseAIScrapersForbidden:
    """Mocks a ``requests.Response`` for a website with a ``robots.txt``-file that forbids AI scraping.
    (This real example was found on golem.de)"""

    status_code = 200
    reason = "OK"
    text = """
User-agent: Twitterbot
Disallow: /mail.php
Disallow: /search.php
Disallow: /trackback/
Disallow: /news/*.amp.html

User-agent: GPTBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: *
Disallow: /mail.php
Disallow: /search.php
Disallow: /trackback/


Sitemap: https://www.golem.de/gsiteindex.xml

# Legal notice: golem.de expressly reserves the right to use its content for commercial text and data mining (§ 44 b UrhG).
# The use of robots or other automated means to access golem.de or collect or mine data without the express permission of golem.de is strictly prohibited.
# golem.de may, in its discretion, permit certain automated access to certain golem.de pages.
# If you would like to apply for permission to crawl golem.de, collect or use data, please email recht@golem.de
        """

    @staticmethod
    def get(*args, **kwargs):
        return MockResponseAIScrapersForbidden()


@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param(
            "https://wirlernenonline.de/robots.txt",
            str,
            id="if WLO is reachable, this function should return a string",
        )
    ],
)
def test_fetch_robots_txt_from_wlo(test_input: str, expected: str | None):
    assert isinstance(fetch_robots_txt(test_input), str)


def test_fetch_robots_txt(monkeypatch):
    """Mocks a ``requests.Response`` for a robots.txt file that forbids AI scrapers."""

    def mock_get(*args, **kwargs):
        return MockResponseAIScrapersForbidden()

    monkeypatch.setattr(requests, "get", mock_get)
    result = fetch_robots_txt("https://www.golem.de/robots.txt")
    assert isinstance(result, str)


def test_fetch_robots_txt_from_an_unreachable_website_with_warning(monkeypatch):
    """Mocks a ``requests.Response`` for a website that's unreachable."""

    # see: https://docs.pytest.org/en/stable/how-to/monkeypatch.html#monkeypatching-returned-objects-building-mock-classes
    def mock_get(*args, **kwargs):
        return MockResponseURLNotFound()

    monkeypatch.setattr(requests, "get", mock_get)
    result = fetch_robots_txt("https://fake.url")
    assert result is None


def test_if_ai_usage_is_allowed_on_malformed_url(monkeypatch):
    """Mocks a ``requests.Response`` for a malformed URL."""

    def mock_get(*args, **kwargs):
        return MockResponseURLNotFound()

    monkeypatch.setattr(requests, "get", mock_get)
    with pytest.raises(ValueError):
        # if the provided URL is malformed, we expect the function to raise a ValueError
        is_ai_usage_allowed("https://malformed-url/robots.txt")


def test_if_ai_usage_is_allowed_on_website_without_robots_txt(monkeypatch):
    """Mocks a ``requests.Response`` for a (available) website that has no ``robots.txt``"""

    def mock_get(*args, **kwargs):
        return MockResponseURLNotFound()

    monkeypatch.setattr(requests, "get", mock_get)
    ai_usage_allowed = is_ai_usage_allowed(
        url="https://www.this-domain-does-not-exist.dev/robots.txt",
    )
    assert ai_usage_allowed is True


def test_if_ai_usage_is_allowed_with_robots_txt_that_forbids_ai_scraping(monkeypatch):
    """Mocks a robots.txt file that explicitly forbids several AI scrapers from crawling the website."""

    def mock_get(*args, **kwargs):
        return MockResponseAIScrapersForbidden()

    monkeypatch.setattr(requests, "get", mock_get)
    ai_usage_allowed: bool = is_ai_usage_allowed(
        url="https://www.golem.de/robots.txt",
    )
    assert ai_usage_allowed is False


def test_if_ai_usage_is_allowed_with_restrictive_robots_txt(monkeypatch):
    """Mocks a ``robots.txt`` file that generally forbids every user agent from scraping anything."""

    def mock_get(*args, **kwargs):
        return MockResponseRestrictive()

    monkeypatch.setattr(requests, "get", mock_get)
    ai_usage_allowed: bool = is_ai_usage_allowed(
        url="https://schule.uni-erfurt.de/robots.txt",
    )
    # Attention: this behavior was implemented deliberately in contrast to normal robots.txt behavior.
    # This implementation follows our use-case of determining if webmasters explicitly disallow AI scrapers,
    # by assuming that robots.txt files with
    # wildcard user agents that forbid all robots from doing anything
    # haven't updated their robots.txt directives w.r.t. AI scrapers yet.
    assert ai_usage_allowed is True

def test_if_ai_usage_is_allowed_with_restrictive_but_mixed_robots_txt(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponseRestrictiveMixed()
    monkeypatch.setattr(requests, "get", mock_get)
    # the mocked response should mimic a test-case where a webmaster (for some reason):
    # - disallowed all robots from interacting with the site (-> ignored)
    # - does not like ChatGPT to crawl its content (-> expected: False)
    # - but for some reason likes to be part of the anthropic AI dataset (-> expected: True)
    # the expected end result, according to our current 1-hit-KO implementation should be: ``False``
    ai_usage_allowed: bool = is_ai_usage_allowed(
        url="https://this-case-is-of-theoretical-nature.de/robots.txt",
    )
    assert ai_usage_allowed is False

# to run these tests, comment out the ``pytest.mark.skip``-decorator
@pytest.mark.skip(
    reason="These tests fire HTTP requests and should only be run on-demand within your IDE for debugging purposes. "
    "They are flaky by nature and could break without notice, therefore they are skipped in the CI/CD pipelines!"
)
@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param(
            "https://www.zum.de/robots.txt",
            True,
            # ZUM.de does not forbid AI scrapers. Last checked on: 2024-12-05
        ),
        pytest.param(
            "https://www.dilertube.de/robots.txt",
            True,
            # DiLerTube does not forbid AI scrapers. Last checked on: 2024-12-05
        ),
        pytest.param(
            "https://www.lehrer-online.de/robots.txt",
            True,
            # Lehrer-Online does not forbid AI scrapers. Last checked on: 2024-12-05
        ),
        pytest.param(
            "https://www.scienceinschool.org/robots.txt",
            True,
            # Science in School does not forbid AI scrapers. Last checked on: 2024-12-05
        ),
        pytest.param(
            "https://www.leifiphysik.de/robots.txt",
            False,
            # Leifi-Physik disallows (a lot) of AI scrapers. Last checked on: 2024-12-05
        ),
        pytest.param(
            "https://www.golem.de/robots.txt",
            False,
            # Golem.de disallows several AI scrapers. Last checked on: 2024-12-05
        ),
        pytest.param(
            "https://taz.de/robots.txt",
            False,
            # taz.de disallows several AI scrapers (GPTBot, Bytespider). Last checked on: 2024-12-05
        ),
    ],
)
def test_if_ai_usage_is_allowed_with_live_examples(test_input: str, expected: bool):
    """This test is flaky by nature as it uses third-party ``robots.txt``-files, which might change without notice,
    and should only be run when you want to debug with live examples."""
    assert is_ai_usage_allowed(url=test_input) is expected

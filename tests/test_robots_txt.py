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

class MockResponseAIScrapersForbidden:
    """Mocks a ``requests.Response`` for a website with a ``robots.txt``-file that forbids AI scraping.
    (This real example was found on golem.de)"""
    status_code = 200
    reason = "OK"
    text = (
        """
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
    )
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
import re
from functools import lru_cache

import requests
import tldextract
from loguru import logger
from protego import Protego
from tldextract.tldextract import ExtractResult

AI_USER_AGENTS: list[str] = [
    "anthropic-ai",
    "Claude-Web",
    "Applebot-Extended",
    "Bytespider",
    "CCBot",
    "ChatGPT-User",
    "cohere-ai",
    "Diffbot",
    "FacebookBot",
    "GoogleOther",
    "Google-Extended",
    "GPTBot",
    "ImagesiftBot",
    "PerplexityBot",
    "OmigiliBot",
    "Omigili",
]
# this non-exhaustive list of known (AI) web crawlers is used to check if the robots.txt file explicitly allows or forbids AI usage
# for reference: https://www.foundationwebdev.com/2023/11/which-web-crawlers-are-associated-with-ai-crawlers/
# ToDo: the list of known AI user agents could be refactored into a SkoHub Vocab


@lru_cache(maxsize=512)
def fetch_robots_txt(url: str) -> str | None:
    """
    Fetch the robots.txt file from the given URL.

    :param url: URL string pointing towards a ``robots.txt``-file.
    :return: The file content of the ``robots.txt``-file as a ``str``, otherwise returns ``None`` if the HTTP ``GET``-request failed.
    """
    response: requests.Response = requests.get(url=url)
    if response.status_code != 200:
        logger.warning(
            f"Could not fetch robots.txt from {url} . "
            f"Response code: {response.status_code} "
            f"Reason: {response.reason}"
        )
        return None
    else:
        # happy-case: the content of the robots.txt file should be available in response.text
        return response.text


def _remove_wildcard_user_agent_from_robots_txt(robots_txt: str) -> str:
    """
    Remove the wildcard user agent part of a string from the given ``robots.txt``-string.

    :param robots_txt: text content of a ``robots.txt``-file
    :return: ``robots.txt``-file content without the wildcard user agent. If no wildcard user agent was found, return the original string without alterations.
    """
    # the user agent directive can appear in different forms and spellings
    # (e.g. "user agent:", "useragent:", "user-agent:", "User-agent:" etc.)
    # and is followed by a newline with "disallow: /"
    _wildcard_pattern: re.Pattern = re.compile(
        r"(?P<user_agent_directive>[u|U]ser[\s|-]?[a|A]gent:\s*[*]\s*)"
        r"(?P<disallow_directive>[d|D]isallow:\s*/\s+)"
    )
    _wildcard_agent_match: re.Match | None = _wildcard_pattern.search(robots_txt)
    if _wildcard_agent_match:
        # remove the wildcard user agent from the parsed robots.txt string
        robots_txt_without_wildcard_agent: str = robots_txt.replace(_wildcard_agent_match.group(), "")
        return robots_txt_without_wildcard_agent
    else:
        # if no wildcard user agent was detected, do nothing.
        return robots_txt


def _parse_robots_txt_with_protego(robots_txt: str) -> Protego | None:
    """
    Parse a ``robots.txt``-string with ``Protego``.

    :param robots_txt: text content of a ``robots.txt``-file
    :return: returns a ``Protego``-object if the string could be parsed successfully, otherwise returns ``None``
    """
    if robots_txt and isinstance(robots_txt, str):
        robots_txt = _remove_wildcard_user_agent_from_robots_txt(robots_txt)
        protego_object: Protego = Protego.parse(robots_txt)
        return protego_object
    else:
        return None


def _check_protego_object_against_list_of_known_ai_user_agents(protego_object: Protego, url: str) -> bool:
    """
    Check if the given ``url`` is allowed to be scraped by AI user agents.

    :param protego_object: ``Protego``-object holding ``robots.txt``-information
    :param url: URL to be checked against a list of known AI user agents
    :return: Returns ``True`` if the given ``url`` is allowed to be scraped by AI user agents. If the ``robots.txt``-file forbids AI scrapers, returns ``False``.
    """
    if url is None:
        raise ValueError(f"url cannot be None. (Please provide a valid URL string!)")
    if protego_object is None:
        raise ValueError(f"This method requires a valid protego object.")
    else:
        ai_usage_allowed: bool = True  # assumption: if not explicitly disallowed by the robots.txt, AI usage is allowed
        for user_agent in AI_USER_AGENTS:
            _allowed_for_current_user_agent: bool = protego_object.can_fetch(
                url=url,
                user_agent=user_agent,
            )
            if _allowed_for_current_user_agent is False:
                ai_usage_allowed = False
                # as soon as one AI user agent is disallowed, we assume that AI usage is generally disallowed,
                # therefore, we can skip the rest of the iterations.
                break
        return ai_usage_allowed


def is_ai_usage_allowed(url: str, robots_txt: str = None) -> bool:
    """
    Check if the given ``url`` is allowed to be scraped by AI user agents.

    :param url: URL to be checked against a list of known AI user agents
    :param robots_txt: string value of a ``robots.txt`` file. If no ``robots.txt``-string is provided, fallback to HTTP Request: ``https://<fully_qualified_domain_name>/robots.txt``
    :return: Returns ``True`` if the given ``url`` is allowed to be scraped by AI user agents. If the URL target forbids any of the known AI scrapers, returns ``False``.
    """
    if robots_txt is None:
        # Fallback:
        # if no robots_txt string was provided, fetch the file from "<fully qualified domain name>/robots.txt"
        _extracted: ExtractResult = tldextract.extract(url=url)
        # using tldextract instead of python's built-in ``urllib.parse.urlparse()``-method was a conscious decision!
        # tldextract is more forgiving/reliable when it comes to incomplete urls (and provides a neat "fqdn"-attribute)
        if _extracted.fqdn:
            # use the fully qualified domain name to build the robots.txt url
            _most_probable_robots_url_path: str = f"https://{_extracted.fqdn}/robots.txt"
            robots_txt: str = fetch_robots_txt(url=_most_probable_robots_url_path)
            if robots_txt is None:
                # if the website provides no robots.txt, assume that everything is allowed
                return True
        else:
            # this covers edge-cases for completely malformed URLs like "https://fakeurl"
            raise ValueError(f"The URL {url} does not exist (and therefore contains no robots.txt).")
    if robots_txt:
        # happy case: check the current url against the provided robots.txt ruleset
        po = _parse_robots_txt_with_protego(robots_txt=robots_txt)
        _ai_usage_allowed: bool = _check_protego_object_against_list_of_known_ai_user_agents(
            protego_object=po,
            url=url,
        )
        return _ai_usage_allowed

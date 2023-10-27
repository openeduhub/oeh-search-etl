import logging

import pytest

from .language_mapper import LanguageMapper


class TestLanguageMapper:
    @pytest.mark.parametrize(
        "test_input, expected_result",
        [
            ("en-US", "en"),
            ("de-DE", "de"),
            ("de_DE", "de"),
            ("fr-FR", "fr"),
            ("Deutsch", None),
            ("this string is invalid", None),
        ],
    )
    def test_normalize_string_to_language_code(self, test_input, expected_result):
        test_mapper = LanguageMapper()
        assert test_mapper._normalize_string_to_language_code(test_input) == expected_result

    @pytest.mark.parametrize(
        "test_input, expected_result",
        [
            (["en-US"], ["en"]),
            (["en-GB"], ["en"]),
            (["en_UK"], ["en"]),
            (["en"], ["en"]),
            (["de-DE"], ["de"]),
            (["de_DE"], ["de"]),
            (["de"], ["de"]),
            (["DE"], ["de"]),
            (["deu"], ["de"]),
            (["ger"], ["de"]),
            (["fr"], ["fr"]),
            (["fra"], ["fr"]),
            (["fre"], ["fr"]),
            # some websites and APIs provide languages as natural languages:
            (["französisch"], ["fr"]),
            (["deutsch"], ["de"]),
            (["German", "german"], ["de"]),
            (["englisch"], ["en"]),
            (["English"], ["en"]),
            (["Spanish"], ["es"]),
            (["español"], ["es"]),
            (["chinese"], ["zh"]),
            # keep only the 3 correct, unique language codes:
            (["de-DE", "en_GB", "fr-FR", "", " en ", "german"], ["de", "en", "fr"]),
            # These codes don't exist:
            (["no_NO", "fa_IL"], None),
        ],
    )
    def test_normalize_list_of_language_strings(self, test_input, expected_result):
        test_mapper = LanguageMapper(languages=test_input)
        assert test_mapper.normalize_list_of_language_strings() == expected_result

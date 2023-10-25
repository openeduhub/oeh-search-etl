import logging
import re

import babel
import langcodes


class LanguageMapper:
    """Helper class to detect ISO-639-1 language codes from potentially malformed strings and natural language."""

    def __init__(self, languages: list[str] = None):
        self.languages = languages

    logging.basicConfig(
        format="%(asctime)s\t%(levelname)s: %(message)s",
        level=logging.DEBUG,
    )

    @staticmethod
    def _normalize_string_to_language_code(raw_string: str) -> str | None:
        """
        Transform raw string to language code if a mapping was possible. If no mapping was possible, return None.

        (Please don't use this private method from outside. It is basically a wrapper for parsing ambiguous, but
        pre-formatted strings with babel.)

        :param raw_string: a string which might or might not contain a language code
        :return: string of mapped language code (2-letter) or None
        """
        regex_lang_code = re.compile(r"^(?P<lang_code_1st>\w{2,3})" r"((?P<separator>[_-])(?P<lang_code_2nd>\w{2}))?$")
        regex_result = regex_lang_code.search(raw_string)
        separator: str | None = None
        if regex_result:
            regex_result_dict = regex_result.groupdict()
            if "separator" in regex_result_dict:
                separator: str = regex_result_dict["separator"]
        else:
            logging.debug(f"The raw string {raw_string} does not look like a typical Locale string.")

        if regex_result and separator:
            # this case happens when the raw string looks like "de_DE" or "en-US"
            # if there is a separator in the provided string, we need to provide it to Babel as a parameter
            try:
                locale_parsed = babel.Locale.parse(raw_string, sep=separator)
                if locale_parsed:
                    language_code = locale_parsed.language
                    return language_code
            except ValueError:
                return None
            except babel.UnknownLocaleError:
                return None
        elif regex_result:
            # this is the default case for 2-letter-codes like "de" or "EN"
            try:
                locale_parsed = babel.Locale.parse(raw_string)
                if locale_parsed:
                    language_code = locale_parsed.language
                    return language_code
            except ValueError:
                return None
            except babel.UnknownLocaleError:
                return None
        else:
            return None

    def normalize_list_of_language_strings(self) -> list[str] | None:
        """
        Transform list of (raw/potential) language strings into ISO-639-1 normalized 2-letter-codes.
        If not a single mapping was possible, return None.

        (Please use only this method if you want to use this helper class from outside!)

        :return: alphabetically sorted list[str] containing all successfully mapped 2-letter language codes or None if
            no mapping was possible.
        """
        if self.languages and isinstance(self.languages, str):
            # since every step from here on expects a list of strings, typecasting to list[str] provides some minor
            # Quality of Life
            logging.debug(f"LanguageMapper was instantiated with a string, converting to Type list[str]...")
            self.languages: list[str] = [self.languages]

        if self.languages and isinstance(self.languages, list):
            normalized_set: set[str] = set()  # normalized strings are saved to a set to mitigate potential duplicates
            edge_cases: set[str] = set()  # helper set to print out all encountered edge-cases during mapping

            for language_item in self.languages:
                # making sure the list items are actually strings:
                if language_item and isinstance(language_item, str):
                    # if the string has (accidental) whitespaces, strip them before parsing:
                    language_item = language_item.strip()

                    if len(language_item) < 2:
                        # logging.debug(
                        #     f"LanguageMapper detected an INVALID language string: '{language_item}' (string length is "
                        #     f"too short to be valid. Dropping string...)"
                        # )
                        edge_cases.add(language_item)
                        # strings which are shorter than 2 chars cannot be valid ISO 639-1
                        # this case might happen if there are typos or empty whitespace strings (e.g. " ")
                    if 2 <= len(language_item) <= 5 and len(language_item) != 4:
                        # this case covers the majority of pre-formatted language-codes, e.g.:
                        # "de", "EN", "de-DE", "de_DE", "en_US" or "sgn"
                        # logging.debug(
                        #     f"LanguageMapper detected a potential 2-to-4-letter language code: '{language_item}'"
                        # )
                        normalized_str: str | None = self._normalize_string_to_language_code(language_item)
                        if normalized_str:
                            normalized_set.add(normalized_str)
                        else:
                            edge_cases.add(language_item)
                    if len(language_item) == 4 or len(language_item) > 5:
                        # natural language edge-cases like "Deutsch", "german", "englisch" are handled here
                        # logging.debug(
                        #     f"LanguageMapper detected a POTENTIALLY INVALID language string: '{language_item}'. "
                        #     f"(String is too long to be a 2- or 4-letter-code). "
                        #     f"Trying to match natural language string to language code..."
                        # )
                        try:
                            langcodes_result: langcodes.Language = langcodes.find(language_item)
                            # using the langcodes Package as a fallback for ambiguous strings
                            # see: https://github.com/rspeer/langcodes/tree/master#recognizing-language-names-in-natural-language
                            if langcodes_result:
                                langcode_detected = langcodes_result.to_tag()
                                # logging.debug(
                                #     f"Detected language code '{langcode_detected}' from string '{language_item}'."
                                # )
                                # ToDo - optional: maybe compare distance between 'langcodes' and 'babel' result?
                                #  see: https://github.com/rspeer/langcodes/tree/master#comparing-and-matching-languages
                                #
                                normalized_str: str | None = self._normalize_string_to_language_code(langcode_detected)
                                normalized_set.add(normalized_str)
                        except LookupError:
                            # if langcodes couldn't find a natural language description, it will throw a LookupError
                            # in that case we can't map the value and add it to our collected edge-cases
                            edge_cases.add(language_item)

            if edge_cases:
                logging.info(
                    f"LanguageMapper could NOT map the following edge-cases to a normalized language code: "
                    f"{list(edge_cases)}"
                )
            if normalized_set:
                # happy case: all recognized and normalized language codes were collected in our result set
                # -> now we need to typecast them as list[str] so they can be used within Scrapy's Field class
                result_list: list[str] = list(normalized_set)
                # to make testing easier, sort the result list before returning it
                result_list.sort()
                return result_list
            else:
                # sad case: if not a single mapping was possible, our result set is empty
                return None
        else:
            logging.warning(f"LanguageMapper expected list[str] but received unexpected type {type(self.languages)} ")
            return None


if __name__ == "__main__":
    # creating a LanguageMapper object for debugging with specific cases that we observed over the years:
    language_candidates: list[str] = [
        "de",
        "de-DE",
        "en_US",
        "Deutsch",
        "fr-FR",
        "",
        "failed string input",  # random string
        "no_NO",  # does not exist
        "Englisch",
    ]
    lm = LanguageMapper(languages=language_candidates)
    normalized_langs = lm.normalize_list_of_language_strings()
    print(f"LanguageMapper result (language codes): {normalized_langs}")

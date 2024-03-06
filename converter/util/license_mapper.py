import logging
import re

from converter.constants import Constants

logger = logging.getLogger(__name__)


class LicenseMapper:
    """
    This (rudimentary) LicenseMapper is intended to help you provide (correct) values for the 'LicenseItem'-fields
    'internal' and 'url'.

    Usage scenario:
    1) Try to map a string for the 'url'-field
        2) If result is None: Try to map the string to the 'internal'-field
            3) If 'internal'-result is None:
            Use this information to set 'internal' to 'CUSTOM' and save the string as a custom license description.
    """

    logging.basicConfig(level=logging.DEBUG)  # ToDo: remove me after debugging

    cc_pattern = re.compile(
        r"(?<=c{2}.)(?P<CC_TYPE>by(.[acdns]{2}){0,3})"
        r".?(?P<CC_VERSION>\d.\d)?"
        r"|(?P<PDM>public.?domain|pdm|gemeinfrei)"
        r"|(?P<CC_ZERO>c{2}.?0|cc.zero|creative.?commons.?zero)"
    )

    # ToDo:
    #  - gather more license string edge-cases from debug crawlers for test cases:
    #    - DiLerTube edge-cases that cannot be handled by the above RegEx yet:
    #      - "Creative Commons (CC) BY-NC-ND Namensnennung-Nicht kommerziell-Keine Bearbeitungen 4.0 International"
    #      - "Creative Commons (CC) BY-SA Namensnennung-Weitergabe unter gleichen Bedingungen 4.0 International"
    #      - "Creative Commons (CC) BY Namensnennung 4.0 International"
    #    - add these edge-cases to the test-suite before trying to improve the RegEx!

    # ToDo:
    #  - feature-idea: fill up provided 'LicenseItemLoader' automatically?
    #       flow: try 'url'
    #           -> fallback: try 'internal'
    #               -> fallback: set 'internal' to 'CUSTOM' & save string to 'description'-field?

    def get_license_url(self, license_string: str = None) -> str | None:
        """
        This method can be used to extract a value intended for the 'LicenseItem'-field 'url'.
        If no license could be mapped, it will return None.
        """
        license_string: str = license_string
        if license_string:
            return self.identify_cc_license(license_string)
        else:
            logger.debug(f"LicenseMapper ('url'): The provided '{license_string}' does not seem to be a valid string.")
            return None

    def get_license_internal_key(self, license_string: str = None) -> str | None:
        """
        This method is intended as a fallback for the 'LicenseItem'-field 'internal'.
        (This might be the case when license strings are provided that don't have a specific CC Version)
        It will return None if no mapping was possible.
        """
        license_string: str = license_string
        if license_string:
            license_string = license_string.lower()
            copyright_hit = self.identify_if_string_contains_copyright(license_string)
            internal_hit = self.fallback_to_license_internal_key(license_string)
            if copyright_hit:
                return Constants.LICENSE_COPYRIGHT_LAW
            if internal_hit:
                return internal_hit
        else:
            logger.debug(
                f"LicenseMapper ('internal'): Could not map '{license_string}' to 'license.internal'-key since it "
                f"doesn't seem to be a valid string."
            )
            return None

    @staticmethod
    def identify_if_string_contains_copyright(license_string: str = None) -> bool:
        """
        Checks a provided string if the word 'copyright' or copyright-indicating unicode symbols are mentioned within
        it.
        @param license_string: string that might or might not contain any 'copyright'-indicating words
        @return: Returns True if 'copyright' was mentioned within a string.
        """
        if license_string:
            license_string = license_string.lower()
            if "copyright" in license_string or "©" in license_string:
                return True
        return False

    @staticmethod
    def identify_if_string_contains_url_pattern(license_string: str = None) -> bool:
        """
        Returns True if URL patterns are found within the string, otherwise returns False.
        """
        license_string: str = license_string
        if license_string:
            license_stripped: str = license_string.strip()
            if "http://" in license_stripped or "https://" in license_stripped:
                # ToDo: use RegEx for more precise URL patterns?
                return True
        else:
            return False

    def fallback_to_license_internal_key(self, license_string: str = None) -> str | None:
        license_string = license_string
        if license_string:
            if self.identify_if_string_contains_copyright(license_string):
                return Constants.LICENSE_COPYRIGHT_LAW
            if self.cc_pattern.search(license_string):
                result_dict = self.cc_pattern.search(license_string).groupdict()
                cc_type = result_dict.get("CC_TYPE")
                cc_zero = result_dict.get("CC_ZERO")
                public_domain = result_dict.get("PDM")
                if cc_zero:
                    logger.debug(
                        f"LicenseMapper: Fallback to 'license.internal' for '{license_string}' successful: " f"CC_0"
                    )
                    return "CC_0"
                if public_domain:
                    logger.debug(
                        f"Licensemapper: Fallback to 'license.internal' for '{license_string}' successful: "
                        f"Public Domain "
                    )
                    return "PDM"
                if cc_type:
                    cc_string_internal: str = f"CC_{result_dict.get('CC_TYPE')}".upper()
                    if "-" in cc_string_internal or " " in cc_string_internal:
                        cc_string_internal = cc_string_internal.replace("-", "_")
                        cc_string_internal = cc_string_internal.replace(" ", "_")
                    if cc_string_internal in Constants.LICENSE_MAPPINGS_INTERNAL:
                        logger.debug(
                            f"LicenseMapper: Fallback to 'license.internal' for '{license_string}' successful: "
                            f"{cc_string_internal}"
                        )
                        return cc_string_internal
                    else:
                        logger.debug(
                            f"LicenseMapper: Fallback to 'license.internal' failed for string "
                            f"'{license_string}' . The extracted string_internal value was: "
                            f"{cc_string_internal}"
                        )
        else:
            return None

    def identify_cc_license(self, license_string: str) -> str | None:
        """
        Checks the provided string if it can be mapped to one of the known URL-strings of Constants.py.
        If no mapping is possible, returns None.
        """
        # ToDo (refactor): check string validity first? - warn otherwise
        license_string_original: str = license_string
        if self.identify_if_string_contains_url_pattern(license_string_original):
            license_url_candidate = license_string_original.lower()
            logger.debug(f"LicenseMapper: The string '{license_url_candidate}' was recognized as a URL.")
            if "http://" in license_url_candidate:
                license_url_candidate = license_url_candidate.replace("http://", "https://")
            if "deed" in license_url_candidate:
                # licenses with a deed suffix could appear in two variations, e.g.:
                # - "deed.de" / "deed.CA" (2-char language code)
                # - "deed.es_ES" (4-char language code)
                regex_deed = re.compile(r"deed\.\w{2}(_?\w{2})?")
                regex_deed_hit = regex_deed.search(license_url_candidate)
                if regex_deed_hit:
                    deed_hit = regex_deed_hit.group()
                    license_url_candidate = license_url_candidate[: -len(deed_hit)]
            url_ending_in_two_char_language_code_regex = re.compile(r"/([a-z]{2}/?)$")
            # RegEx pattern for handling URLs that end in "/de", "/de/", "/fr", "/es/" etc.
            two_char_language_code_hit = url_ending_in_two_char_language_code_regex.search(license_url_candidate)
            if two_char_language_code_hit:
                # checks if the URL pattern ends in "/de", "/de/" or any other type of 2-char language code, e.g.:
                # http://creativecommons.org/licenses/by/3.0/de or https://creativecommons.org/licenses/by/3.0/es/
                # and only keeps the part of the string that can be recognized by the pipeline
                url_language_code_trail: str = two_char_language_code_hit.group()
                if url_language_code_trail:
                    # the url_language_code_trail will typically look like "/de/" or "/de", but we only want to cut off
                    # the 2-char language code and its trailing slash, but keep the first slash intact
                    license_url_candidate = license_url_candidate[: -len(url_language_code_trail) + 1]
            for valid_license_url in Constants.VALID_LICENSE_URLS:
                if license_url_candidate in valid_license_url:
                    return valid_license_url
        elif license_string:
            license_string = license_string.lower()
            logger.debug(f"LicenseMapper: Received license string '{license_string}'")
            if self.cc_pattern.search(license_string):
                result_dict: dict = self.cc_pattern.search(license_string).groupdict()
                cc_type = result_dict.get("CC_TYPE")
                cc_version = result_dict.get("CC_VERSION")
                cc_zero = result_dict.get("CC_ZERO")
                public_domain = result_dict.get("PDM")
                if cc_zero:
                    return Constants.LICENSE_CC_ZERO_10
                if cc_type and cc_version:
                    partial_url = (
                        f"/{str(result_dict.get('CC_TYPE')).lower().strip()}"
                        f"/{str(result_dict.get('CC_VERSION')).lower().strip()}/"
                    )
                    logger.debug(f"partial_url: {partial_url}")
                    for valid_license_url in Constants.VALID_LICENSE_URLS:
                        if partial_url in valid_license_url:
                            logger.debug(
                                f"LicenseMapper: License string '{license_string}' was recognized as "
                                f"{valid_license_url}"
                            )
                            return valid_license_url
                if public_domain:
                    return Constants.LICENSE_PDM
                elif cc_type:
                    logger.debug(
                        f"LicenseMapper: Couldn't recognize a (valid) CC Version within {license_string} - "
                        f"Trying fallback method for 'license.internal' next..."
                    )
                    return None
        else:
            logger.debug(f"LicenseMapper: Couldn't detect a CC license within {license_string}")
            return None


if __name__ == "__main__":
    test_mapper = LicenseMapper()
    # test-cases for debugging purposes
    # print(test_mapper.get_license_internal_key("CC BY-NC-ND"))
    # print(test_mapper.get_license_internal_key("zufälliger CC BY lizenzierter Freitext-String"))
    # print(test_mapper.get_license_url("a random CC-BY 4.0 string"))
    # print(test_mapper.get_license_url("https://creativecommons.org/licenses/by-nc/3.0/de/"))
    # print(test_mapper.identify_cc_license("https://creativecommons.org/licenses/by-nc/3.0/deed.de"))
    print(test_mapper.identify_cc_license("http://creativecommons.org/licenses/by-nc-nd/2.5/ch/deed.en"))

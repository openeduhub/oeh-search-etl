import logging
import re

from converter.constants import Constants


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
    #  - gather more license string edge-cases from debug crawlers for test cases
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
            logging.debug(f"LicenseMapper ('url'): The provided '{license_string}' does not seem to be a valid string.")
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
            logging.debug(
                f"LicenseMapper ('internal'): Could not map '{license_string}' to 'license.internal'-key since it doesn't "
                f"seem to be a valid string."
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
                    return "CC_0"
                if public_domain:
                    return "PDM"
                if cc_type:
                    cc_string_internal: str = f"CC_{result_dict.get('CC_TYPE')}".upper()
                    if "-" in cc_string_internal or " " in cc_string_internal:
                        cc_string_internal = cc_string_internal.replace("-", "_")
                        cc_string_internal = cc_string_internal.replace(" ", "_")
                    if cc_string_internal in Constants.LICENSE_MAPPINGS_INTERNAL:
                        return cc_string_internal
                    else:
                        logging.debug(
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
            license_url_candidate = license_string_original
            logging.info(f"LicenseMapper: {license_url_candidate} was recognized as a URL")
            if "http://" in license_url_candidate:
                license_url_candidate = license_url_candidate.replace("http://", "https://")
            if license_url_candidate.endswith("deed.de"):
                license_url_candidate = license_url_candidate[: -len("deed.de")]
            if license_url_candidate.endswith("/de/"):
                license_url_candidate = license_url_candidate[: -len("de/")]
            for valid_license_url in Constants.VALID_LICENSE_URLS:
                if license_url_candidate in valid_license_url:
                    return valid_license_url
        elif license_string:
            license_string = license_string.lower()
            logging.debug(f"LicenseMapper: Recognized license string '{license_string}'")
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
                    logging.debug(f"partial_url: {partial_url}")
                    for valid_license_url in Constants.VALID_LICENSE_URLS:
                        if partial_url in valid_license_url:
                            logging.debug(
                                f"LicenseMapper: License string '{license_string}' was recognized as "
                                f"{valid_license_url}"
                            )
                            return valid_license_url
                if public_domain:
                    return Constants.LICENSE_PDM
                elif cc_type:
                    logging.debug(
                        f"LicenseMapper: Couldn't recognize a (valid) CC Version within {license_string} - "
                        f"Trying fallback method..."
                    )
                    return None
        else:
            logging.debug(f"LicenseMapper: Couldn't detect a CC license within {license_string}")
            return None


if __name__ == "__main__":
    test_mapper = LicenseMapper()
    # test-cases for debugging purposes
    print(test_mapper.get_license_internal_key("CC BY-NC-ND"))
    print(test_mapper.get_license_internal_key("zufälliger CC BY lizenzierter Freitext-String"))
    print(test_mapper.get_license_url("a random CC-BY 4.0 string"))
    print(test_mapper.get_license_url("https://creativecommons.org/licenses/by-nc/3.0/de/"))
    print(test_mapper.identify_cc_license("https://creativecommons.org/licenses/by-nc/3.0/deed.de"))
    pass

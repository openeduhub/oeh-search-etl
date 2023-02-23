import pytest

from converter.constants import Constants
from .license_mapper import LicenseMapper


class TestLicenseMapper:
    @pytest.mark.parametrize(
        "test_input, expected_result",
        [
            ("a random CC-BY 4.0 string", Constants.LICENSE_CC_BY_40),
            ("CC-0", Constants.LICENSE_CC_ZERO_10),
            ("the license CC0 is mentioned somewhere", Constants.LICENSE_CC_ZERO_10),
            ("CC-Zero", Constants.LICENSE_CC_ZERO_10),
            ("Creative Commons Zero", Constants.LICENSE_CC_ZERO_10),
            ("CC-BY-SA-4.0", Constants.LICENSE_CC_BY_SA_40),
            ("CC-BY-NC-SA 3.0", Constants.LICENSE_CC_BY_NC_SA_30),
            (" CC BY 4.0 ", Constants.LICENSE_CC_BY_40),
            (
                "https://creativecommons.org/licenses/by-sa/4.0",
                Constants.LICENSE_CC_BY_SA_40,
            ),
            (
                "https://creativecommons.org/licenses/by-nd/3.0/",
                Constants.LICENSE_CC_BY_ND_30,
            ),
            ("https://creativecommons.org/licenses/by-nc/3.0/deed.de", Constants.LICENSE_CC_BY_NC_30),
            ("https://creativecommons.org/licenses/by-nc/3.0/de/", Constants.LICENSE_CC_BY_NC_30),
            (
                "Copyright Zweites Deutsches Fernsehen, ZDF",
                None,
            ),
            ("Public Domain", Constants.LICENSE_PDM),
        ],
    )
    def test_get_license_url(self, test_input, expected_result):
        test_mapper = LicenseMapper()
        assert LicenseMapper.get_license_url(test_mapper, license_string=test_input) == expected_result

    @pytest.mark.parametrize(
        "test_input, expected_result",
        [
            ("Copyright Zweites Deutsches Fernsehen, ZDF", Constants.LICENSE_COPYRIGHT_LAW),
            (" © ", Constants.LICENSE_COPYRIGHT_LAW),
            # ToDo: regularly check if new enums for the 'internal' field need to be added here or in Constants.py
            ("jemand erwähnt CC0 in einem Freitext", "CC_0"),
            ("CC-0", "CC_0"),
            ("zufälliger CC BY lizensierter Freitext-String ohne Versionsnummer", "CC_BY"),
            ("CC-BY-NC ohne Version", "CC_BY_NC"),
            ("CC BY-NC-ND", "CC_BY_NC_ND"),
            (" CC BY NC SA", "CC_BY_NC_SA"),
            (" CC BY ND ", "CC_BY_ND"),
            (" CC BY SA ", "CC_BY_SA"),
            ("dieser Text ist public domain", "PDM"),
            ("Gemeinfrei", "PDM"),
            ("Frei nutzbares Material", None),
            (" ", None),
            ("", None),
        ],
    )
    def test_get_license_internal_key(self, test_input, expected_result):
        test_mapper = LicenseMapper()
        assert LicenseMapper.get_license_internal_key(test_mapper, license_string=test_input) == expected_result

import pytest

from converter.constants import Constants
from .license_mapper import LicenseMapper


class TestLicenseMapper:
    @pytest.mark.parametrize(
        "test_input, expected_result",
        [
            ("a random CC-BY 4.0 string", Constants.LICENSE_CC_BY_40),
            ("CC-0", Constants.LICENSE_CC_ZERO_10),
            ("https://creativecommons.org/publicdomain/zero/1.0/deed.de", Constants.LICENSE_CC_ZERO_10),
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
            ("https://creativecommons.org/publicdomain/mark/1.0/deed.de", Constants.LICENSE_PDM),
            ("https://creativecommons.org/licenses/by-nc-nd/3.0/deed.DE", Constants.LICENSE_CC_BY_NC_ND_30),
            ("https://creativecommons.org/licenses/by-nc-nd/2.0/deed.CA", Constants.LICENSE_CC_BY_NC_ND_20),
            ("https://creativecommons.org/licenses/by-sa/4.0/deed.es_ES", Constants.LICENSE_CC_BY_SA_40),
            # ToDo: Apache / BSD / GNU GPL licenses can't be mapped at the moment
            ("https://www.gnu.org/licenses/gpl-3.0", None),
            ("https://opensource.org/licenses/MIT", None),
            ("http://creativecommons.org/licenses/by/3.0/de", Constants.LICENSE_CC_BY_30),
            ("https://creativecommons.org/licenses/by/3.0/es/", Constants.LICENSE_CC_BY_30),
            ("https://creativecommons.org/licenses/by/3.0/fr", Constants.LICENSE_CC_BY_30),
            ("http://creativecommons.org/licenses/by-nc-nd/2.5/ch/deed.en", Constants.LICENSE_CC_BY_NC_ND_25),
            ("https://creativecommons.org/licenses/by/1.0/deed.de", Constants.LICENSE_CC_BY_10),
            ("https://creativecommons.org/licenses/by-sa/1.0/deed.de", Constants.LICENSE_CC_BY_SA_10),
            ("Creative Commons (CC) CC0 gemeinfrei (public domain - no rights reserved)", Constants.LICENSE_CC_ZERO_10)
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
            # ToDo: find valid test-cases for LICENSE.COPYRIGHT_FREE
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
            ("Gemeinfrei / public domain", "PDM"),
            ("Frei nutzbares Material", None),
            (" ", None),
            ("", None),
            ("Creative Commons (CC) CC0 gemeinfrei (public domain - no rights reserved)", "CC_0")
        ],
    )
    def test_get_license_internal_key(self, test_input, expected_result):
        test_mapper = LicenseMapper()
        assert LicenseMapper.get_license_internal_key(test_mapper, license_string=test_input) == expected_result

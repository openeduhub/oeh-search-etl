import pytest

from converter.pipelines import determine_duration_and_convert_to_seconds


@pytest.mark.parametrize("test_input, expected_result",
                         [
                             ("", None),
                             ("0", 0),
                             ("12:30:55", 45055),  # 43200s + 1800s + 55s = 45055s
                             ("08:25:24", 30324),  # 28800s + 1500s + 24s = 30324s
                             ("8:8:8", 29288),  # 28800s + 480s + 8s = 29288
                             ("86", 86),  # typically found in RSS feeds
                             ("  120 ", 120),  # input contains unnecessary whitespace
                             ("120.0", 120),  # float edge-case
                             ("P7W", 4233600),  # MOOCHub (v3) 'duration'-attribute uses a ISO-8601 format
                             ("P12W", 7257600),
                             ("P0.5D", 43200),  # one decimal fraction is allowed according to ISO 8601 durations
                             ("P0,5D", 43200),
                             ("P1Y", None),
                             ("P6M", None),
                             (30.5, 30),
                             (30.0, 30),
                          ]
                         )
def test_determine_duration_and_convert_to_seconds(test_input, expected_result):
    """
    Test the conversion from "duration"-values (of unknown type) to seconds (int).
    """
    # ToDo:
    #  - ISO-8601 edge-cases: "P6M" or "P1Y" cannot be converted to total seconds!
    #  - NLP not yet implemented: "12 Stunden" / "6 Monate" etc. (German or English strings)
    assert determine_duration_and_convert_to_seconds(time_raw=test_input, item_field_name="TestItem") == expected_result

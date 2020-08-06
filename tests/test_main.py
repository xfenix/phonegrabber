"""Tests module."""
import os

import pytest

from phonegrabber.base import extract_phone_numbers, normalize_phone_number


FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


@pytest.mark.parametrize(
    "one_case",
    (
        ("hands.ru.html", {"84951377767"}),
        ("msota.ru.html", {"88007007009", "84957899559"}),
        ("repetitors.info.html", {"88005555676", "84955405676", "88005057283", "88005057284"}),
        ("yandex.ru.html", {"89139095489"}),  # +79139095489 number really there
    ),
)
def test_extract_phone_numbers_fixtures(one_case):
    """Test phone extraction from real files."""
    full_path = os.path.join(FIXTURES_DIR, one_case[0])
    if os.path.exists(full_path):
        with open(full_path, "r") as fixture_data:
            fn_result = extract_phone_numbers(fixture_data.read())
            assert fn_result == one_case[1], "Current case {}, fn output {}".format(one_case[0], fn_result)
    else:
        raise OSError("No fixture :(")


@pytest.mark.parametrize(
    "one_case",
    (
        ("Testing +7 495 111-33-00", {"84951113300"}),
        ("Whoops 890133344 55", {"89013334455"}),
        ("Hola +7 (905) 531-01 45", {"89055310145"}),
        ("How about this?8(905) 531-01 45", {"89055310145"}),
        ('<a href="tel:89055310145">8(905) 531-01 45</a>', {"89055310145"}),
        ('<a href="tel:89055310145">   8(905) 531-01 45</a>', {"89055310145"}),
        ('<a href="tel:89055310145">   +7 905) 531-01 45</a>', {"89055310145"}),
        ('<a href="tel:89055310145">   +7 905) 531-01 45</a> 8(916)5310145', {"89055310145", "89165310145"}),
        ("Whoops 890133344 55", {"89013334455"}),
        ("Debugging this case +79055310145", {"89055310145"}),
        ("Жили были in this case:89055310145", {"89055310145"}),
        ("Какой-то текст и внезапно, 89055310145 где-то тут", {"89055310145"}),
        ("Какой-то текст и внезапно,89055310145", {"89055310145"}),
        ("Мой телефон -89055310145 что-то там", {"89055310145"}),
        ("Мой телефон -+79055310145", {"89055310145"}),
        ("<span>89055310145</a>", {"89055310145"}),
        ("?param=89055310145", set()),
    ),
)
def test_extract_phone_numbers_raw_input(one_case):
    """Test phone extraction with only phones."""
    fn_result = extract_phone_numbers(one_case[0])
    assert fn_result == one_case[1], "Current case {}, fn output {}".format(one_case[0], fn_result)


@pytest.mark.parametrize(
    "one_case",
    (
        ("  +7 495 531 01 45", "84955310145"),
        ("   890133344 55", "89013334455"),
        ("8           90133344 55", "89013334455"),
        ("8(905) 531-01 45", "89055310145"),
    ),
)
def test_phone_normalization(one_case):
    """Phone normalization."""
    fn_result = normalize_phone_number(one_case[0])
    assert fn_result == one_case[1], "Current case {}, fn output {}".format(one_case[0], fn_result)

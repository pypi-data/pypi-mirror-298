import pytest

from milgeo.color import ColorFinder


@pytest.fixture
def color_finder():
    color_finder = ColorFinder()
    return color_finder


def test_hex_color(color_finder):
    assert color_finder.find_hex_color("Here is a color: #ff5733") == "#ff5733"
    assert color_finder.find_hex_color("<color>#ff0000ff</color>") == "#ff0000"
    assert color_finder.find_hex_color("<color>#7fff0000</color>") == "#7fff00"
    assert color_finder.find_hex_color("<color>#40ff00ff</color>") == "#40ff00"
    assert color_finder.find_hex_color("<color>#ffff00ff</color>") == "#ffff00"
    assert color_finder.find_hex_color("<color>#bf00ff00</color>") == "#bf00ff"
    assert color_finder.find_hex_color("<color>#7fffff00</color>") == "#7fffff"


def test_rgb_color(color_finder):
    assert color_finder.find_hex_color("Here is a color: rgb(255, 87, 51)") == "#ff5733"


def test_named_color(color_finder):
    assert color_finder.find_hex_color("Here is a color: bLueasdsad") == "#0000ff"


def test_no_color(color_finder):
    assert color_finder.find_hex_color("There are no colors here.") is None


def test_mixed_colors(color_finder):
    assert color_finder.find_hex_color("Color in hex: #123456 and rgb: rgb(18, 52, 86)") == "#123456"


def test_kml_color_format(color_finder):
    assert color_finder.find_hex_color("<color>ff0000ff</color>") == "#ff0000"
    assert color_finder.find_hex_color("<color>7fff0000</color>") == "#0000ff"
    assert color_finder.find_hex_color("<color>40ff00ff</color>") == "#ff00ff"
    assert color_finder.find_hex_color("<color>ffff00ff</color>") == "#ff00ff"
    assert color_finder.find_hex_color("<color>bf00ff00</color>") == "#00ff00"
    assert color_finder.find_hex_color("<color>7fffff00</color>") == "#00ffff"

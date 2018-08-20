from gc3_query.lib.utils import camelcase_to_snake


def test_camelcase_to_snake():
    assert camelcase_to_snake("snakesOnAPlane") == "snakes_on_a_plane"
    assert camelcase_to_snake("SnakesOnAPlane") == "snakes_on_a_plane"
    assert camelcase_to_snake("snakes_on_a_plane") == "snakes_on_a_plane"
    assert camelcase_to_snake("IPhoneHysteria") == "i_phone_hysteria"
    assert camelcase_to_snake("iPhoneHysteria") == "i_phone_hysteria"

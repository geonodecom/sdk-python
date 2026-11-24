import geonode_scraper_sdk


def test_configuration_defaults_to_the_production_api():
    # The host comes from `servers` in openapi.json; a regeneration that loses it points the client at localhost.
    assert geonode_scraper_sdk.Configuration().host == "https://scraper.geonode.io"

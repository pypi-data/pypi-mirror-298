import os
import pytest
from geo2zip import Geo2Zip

# Defined the coordinates for some well-known American cities and their expected ZIP codes
# This can be extended if needed
cities = [
    ('New York, NY', 40.7128, -74.0060, '10007', 'US'),
    ('Los Angeles, CA', 34.0522, -118.2437, '90013', 'US'),
    ('Chicago, IL', 41.8781, -87.6298, '60604', 'US'),
    ('Houston, TX', 29.7604, -95.3698, '77002', 'US'),
    ('Phoenix, AZ', 33.4484, -112.0740, '85003', 'US'),
    ('Philadelphia, PA', 39.9526, -75.1652, '19102', 'US'),
    ('San Antonio, TX', 29.4241, -98.4936, '78205', 'US'),
    ('San Diego, CA', 32.7157, -117.1611, '92132', 'US'),
    ('Dallas, TX', 32.7767, -96.7970, '75270', 'US'),
    ('San Francisco, CA', 37.7749, -122.4194, '94102', 'US'),
    # Canadian cities
    ('Toronto, ON', 43.65107, -79.347015, 'M5A1C3', 'CA'),
    ('Vancouver, BC', 49.2827, -123.1207, 'V6Z2H7', 'CA'),
    ('Montreal, QC', 45.5017, -73.5673, 'H3A1T9', 'CA'),
    ('Calgary, AB', 51.0447, -114.0719, 'T2P1L4', 'CA'),
    ('Edmonton, AB', 53.5461, -113.4938, 'T5J4X1', 'CA'),
    ('Ottawa, ON', 45.4215, -75.6972, 'K1P5G2', 'CA'),
    ('Winnipeg, MB', 49.8951, -97.1384, 'R3C4H5', 'CA'),
    ('Quebec City, QC', 46.8139, -71.2082, 'G1C2W3', 'CA'),
    ('Hamilton, ON', 43.2557, -79.8711, 'L8S4N9', 'CA'),
    ('Victoria, BC', 48.4284, -123.3656, 'V8W1N8', 'CA'),
]


@pytest.fixture(scope='module')
def geo2zip():
    file_path = os.path.join(os.path.dirname(__file__), '../geo2zip/data/')
    return Geo2Zip(file_path)


@pytest.mark.parametrize('city, lat, lon, expected_zip, expected_country', cities)
def test_find_closest_zip(geo2zip, city, lat, lon, expected_zip, expected_country):
    closest_zip = geo2zip.find_closest_zip(lat, lon)
    assert closest_zip == expected_zip, f"Expected {expected_zip} but got {closest_zip} for {city}"


def test_find_closest_zip_with_distance_threshold(geo2zip):
    # Using Barcelona (Spain) coordinates with a limit of 100 kms to the closest postal code
    with pytest.raises(ValueError, match="distance: .* threshold: 100"):
        geo2zip.find_closest_zip(41.3851, 2.1734, distance_threshold=100)


@pytest.mark.parametrize('city, lat, lon, expected_zip, expected_country', cities)
def test_find_closest_zip_with_aggressive_distance_threshold(geo2zip, city, lat, lon, expected_zip, expected_country):
    with pytest.raises(ValueError, match="distance: .* threshold: 0.001"):
        closest_zip = geo2zip.find_closest_zip(lat, lon, distance_threshold=0.001)


@pytest.mark.parametrize('city, lat, lon, expected_zip, expected_country', cities)
def test_find_closest_zip_and_country(geo2zip, city, lat, lon, expected_zip, expected_country):
    closest_zip, country = geo2zip.find_closest_zip_and_country(lat, lon)
    assert closest_zip == expected_zip, f"Expected {expected_zip} but got {closest_zip} for {city}"
    assert country == expected_country, f"Expected {expected_country} but got {country} for {city}"


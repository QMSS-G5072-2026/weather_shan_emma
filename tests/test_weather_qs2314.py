"""Tests for the weather_qs2314 package."""

import weather_qs2314
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_qs2314 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

def test_version_is_defined():
    assert isinstance(weather_qs2314.__version__, str)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================

@pytest.mark.parametrize("celsius, expected", [
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6),
    (-273.15, -459.67)
])

def test_celsius_to_fahrenheit(celsius, expected):
    """Test Celsius-to-Fahrenheit conversion for five temperatures."""
    # Act
    result = celsius_to_fahrenheit(celsius)
    # Assert
    assert result == pytest.approx(expected)

@pytest.mark.parametrize('bad_input, expected_error', [
    ('A string', TypeError),
    (None, TypeError),
    (-300, ValueError),
    ('Another string', TypeError)
])

def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Test that invalid inputs raise the expected exceptions."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)

def test_summarize_temperatures():
    """Test temperature summaries with one missing value."""
    # Arrange
    temps = [15.0, 21.0, float("nan")]
    # Act
    result = summarize_temperatures(temps)
    # Assert
    assert result["mean"] == 18.0
    assert result["min"] == 15.0
    assert result["max"] == 21.0
    assert result["n_missing"] == 1

# =============================================================================
# PART 2: FIXTURES
# =============================================================================

@pytest.fixture
def raw_readings():
    """Provide sample weather station readings for testing."""
    return pd.DataFrame({
    "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
    "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
    "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
})
    
def test_raw_readings_fixture(raw_readings):
    """Check the columns, rows, and missing values."""
    #convert to a list for comparison
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    #number of rows
    assert len(raw_readings) == 5
    #missing value
    assert raw_readings["temp_c"].isna().sum() == 1

# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================

def test_clean_readings(raw_readings):
    """Test that readings are cleaned, converted, and sorted correctly."""
    #Arrange - Create input data
    expected = pd.DataFrame({
    "station": ["CPK", "JFK", "LGA"],
    "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
    "temp_c": [25.0, 30.0, 28.0],
    "temp_f": [77.0, 86.0, 82.4]
})
    
    #Act: clean the raw readings
    result = clean_readings(raw_readings)
    
    # Assert: compare
    assert_frame_equal(result, expected, atol=0.01) 


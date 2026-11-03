# read version from installed package
from importlib.metadata import version
__version__ = version("weather_qs2314")

from .weather_qs2314 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)
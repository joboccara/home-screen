from datetime import datetime
import os
import pytest
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)

from src.rain_hour_scraping import parse_rain_labels, parse_scraped_data

def test_rain_labels_are_mapped():
  rain_labels = ['Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie modérée', 'Pluie faible', 'Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie faible']
  assert parse_rain_labels(rain_labels) == [3, 0, 0, 2, 1, 3, 0, 0, 1]

def test_unknown_label_throws_exception():
  rain_labels = ['XXXXXXX', 'Pas de pluie', 'Pas de pluie', 'Pluie modérée', 'Pluie faible', 'Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie faible']
  with pytest.raises(Exception):
    parse_rain_labels(rain_labels)

def test_datetimes_are_associated_to_rain_labels():
  rain_labels = ['Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie modérée', 'Pluie faible', 'Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie faible']
  assert parse_scraped_data("18 : 25", rain_labels) == {
    datetime(1900, 1, 1, 18, 25): 3,
    datetime(1900, 1, 1, 18, 30): 0,
    datetime(1900, 1, 1, 18, 35): 0,
    datetime(1900, 1, 1, 18, 40): 2,
    datetime(1900, 1, 1, 18, 45): 1,
    datetime(1900, 1, 1, 18, 50): 3,
    datetime(1900, 1, 1, 18, 55): 0,
    datetime(1900, 1, 1, 19, 5): 0,
    datetime(1900, 1, 1, 19, 15): 1,
  }

def test_invalid_start_time_format_throws_exception():
  rain_labels = ['Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie modérée', 'Pluie faible', 'Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie faible']
  with pytest.raises(Exception):
    parse_scraped_data("14: 52", rain_labels)

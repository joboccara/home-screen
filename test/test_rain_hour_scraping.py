import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_dir)

from src.rain_hour_scraping import parse_rain_labels

def test_rain_labels_are_mapped():
  rain_labels = ['Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie modérée', 'Pluie faible', 'Pluie forte', 'Pas de pluie', 'Pas de pluie', 'Pluie faible']
  assert parse_rain_labels(rain_labels) == [3, 0, 0, 2, 1, 3, 0, 0, 1]

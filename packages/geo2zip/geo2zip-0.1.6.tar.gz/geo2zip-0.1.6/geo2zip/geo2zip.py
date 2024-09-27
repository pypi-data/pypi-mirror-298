import csv
import math
import os

from typing import List, Dict, Optional, Tuple

from haversine import haversine
from scipy.spatial import KDTree


class Geo2Zip:
    def __init__(self, path: Optional[str] = None):
        """
        Initializes the Geo2Zip object and builds the KDTree from CSV files in the provided path.

        :param path: Path to the CSV file or directory containing CSV files with geo-coordinates and zip codes.
        """
        if path is None:
            path = os.path.join(os.path.dirname(__file__), 'data')

        if os.path.isdir(path):
            self.data = self._read_csv_files(path)
        elif os.path.isfile(path):
            self.data = self._read_csv(path)
        else:
            raise ValueError(f"The provided path '{path}' is neither a directory nor a file.")

        self.tree, self.geoids, self.countries = self._build_kdtree(self.data)

    def _read_csv_files(self, directory_path: str) -> List[Dict[str, str]]:
        """
        Reads all CSV files in the given directory and returns a list of dictionaries representing the rows.

        :param directory_path: Path to the directory containing CSV files.
        :return: List of dictionaries with CSV data.
        """
        all_data = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory_path, filename)
                all_data.extend(self._read_csv(file_path))
        return all_data

    def _read_csv(self, file_path: str) -> List[Dict[str, str]]:
        """
        Reads a single CSV file and returns a list of dictionaries representing the rows.

        :param file_path: Path to the CSV file.
        :return: List of dictionaries with CSV data.
        """
        try:
            with open(file_path, mode='r', newline='') as csvfile:
                sample = csvfile.read(1024)
                csvfile.seek(0)
                dialect = csv.Sniffer().sniff(sample)
                reader = csv.DictReader(csvfile, dialect=dialect)
                return [row for row in reader]
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found at path: {file_path}")
        except csv.Error as e:
            raise Exception(f"Error detecting CSV dialect: {e}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {e}")

    def _build_kdtree(self, data: List[Dict[str, str]]) -> Tuple[KDTree, List[str], List[str]]:
        """
        Builds a KDTree from the provided data.

        :param data: List of dictionaries containing geo-coordinates, zip codes, and country names.
        :return: A tuple containing the KDTree, a list of Zip/Postal codes, and a list of countries
        """
        coordinates, geoids, countries = [], [], []

        for row in data:
            try:
                lat = float(row['LAT'])
                lon = float(row['LONG'])
                coordinates.append((lat, lon))
                geoids.append(row['GEOID'])
                countries.append(row['COUNTRY'])
            except ValueError:
                # Skip rows with invalid coordinates
                continue

        tree = KDTree(coordinates)
        return tree, geoids, countries

    def _find_closest_zip_index(self, lat: float, lon: float, distance_threshold: Optional[float] = None) -> int:
        """
        Finds the closest zip / postal code index on the kdtree for the given latitude and longitude using the KDTree.

        :param lat: Latitude of the query point.
        :param lon: Longitude of the query point.
        :param distance_threshold: Optional; Maximum allowed distance to the closest zip code in kilometers. If exceeded, return None.
        :return: A string containing the Zip/Postal code 
        """
        distance, index = self.tree.query((lat, lon))
        real_distance = haversine((lat, lon), self.tree.data[index])

        if distance_threshold is not None and real_distance > distance_threshold:
            raise ValueError(f"Points are too far away (distance: {distance:.2f}, threshold: {distance_threshold}).")

        return index

    def find_closest_zip(self, lat: float, lon: float, distance_threshold: Optional[float] = None) -> str:
        """
        Finds the closest zip / postal code for the given latitude and longitude using the KDTree.

        :param lat: Latitude of the query point.
        :param lon: Longitude of the query point.
        :param distance_threshold: Optional; Maximum allowed distance to the closest zip code in kilometers. If exceeded, return None.
        :return: A string containing the Zip/Postal code
        """
        index = self._find_closest_zip_index(lat, lon, distance_threshold)
        return self.geoids[index]

    def find_closest_zip_and_country(self, lat: float, lon: float, distance_threshold: Optional[float] = None) -> Tuple[str, str]:
        """
        Finds the closest zip code and country name for the given latitude and longitude using the KDTree.

        :param lat: Latitude of the query point.
        :param lon: Longitude of the query point.
        :param distance_threshold: Optional; Maximum allowed distance to the closest zip code in kilometers. If exceeded, return None.
        :return: A tuple containing the Zip/Postal code and the country name of the closest point.
        """
        index = self._find_closest_zip_index(lat, lon, distance_threshold)
        return self.geoids[index], self.countries[index]

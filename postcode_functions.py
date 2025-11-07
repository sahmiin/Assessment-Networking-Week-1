"""Functions that interact with the Postcode API."""

import os
import json
import requests as req

CACHE_FILE = "./postcode_cache.json"

def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        return json.dump(cache, f)


def validate_postcode(postcode: str) -> bool:
    """Returns a boolean as a check for valid postcodes."""
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")
    cache = load_cache()
    if postcode in cache and 'valid' in cache[postcode]:
        return cache[postcode]['valid']
    response = req.get(f"https://api.postcodes.io/postcodes/{postcode}/validate", timeout=10)
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    if response.status_code == 200:
        cache[postcode] = {}
        cache[postcode]['valid'] = response.json().get('result', False)
        save_cache(cache)
        return response.json()['result']


def get_postcode_for_location(lat: float, long: float) -> str:
    """Returns a postcode based on longitudinal and latitudinal location."""
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")
    response = req.get(f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}", timeout=10)
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    if response.json()['result'] is None:
        raise ValueError("No relevant postcode found.")
    return response.json()['result'][0]['postcode']


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Returns a full postcode based on the beginning of a known postcode."""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")
    cache = load_cache()
    if postcode_start in cache and 'completions' in cache[postcode_start]:
        return cache[postcode_start]['completions']
    response = req.get(f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete",
                        timeout=10)
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    if response.status_code == 200:
        cache[postcode_start] = {}
        cache[postcode_start]['completions'] = response.json().get('result', False)
        save_cache(cache)
        return response.json()['result']


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Returns the details of given list of postcodes."""
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")
    for item in postcodes:
        if not isinstance(item, str):
            raise TypeError("Function expects a list of strings.")
    response = req.post("https://api.postcodes.io/postcodes",
                        json={'postcodes': postcodes}, timeout=10)
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    return response.json()

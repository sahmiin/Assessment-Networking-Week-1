"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"

def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
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
    response = req.get(f"https://api.postcodes.io/postcodes/{postcode}/validate")
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")  
    if response.status_code == 200:
        return response.json()['result']


def get_postcode_for_location(lat: float, long: float) -> str:
    """Returns a postcode based on longitudinal and latitudinal location."""
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")
    response = req.get(f"https://api.postcodes.io/postcodes?lon={long}&lat={lat}")
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    if response.json()['result'] == None:
        raise ValueError("No relevant postcode found.")
    return response.json()['result'][0]['postcode']


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Returns a full postcode based on the beginning of a known postcode."""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")
    response = req.get(f"https://api.postcodes.io/postcodes/{postcode_start}/autocomplete")
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    return response.json()['result']


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Returns"""
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")
    for item in postcodes:
        if not isinstance(item, str):
            raise TypeError("Function expects a list of strings.") 
    response = req.post(f"https://api.postcodes.io/postcodes",
                        json={'postcodes': postcodes})
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")
    return response.json()

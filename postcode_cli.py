"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import get_postcode_completions, get_postcode_for_location, get_postcodes_details

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", required=True, choices=["validate", "complete"],
                        help="Choose a specific mode: 'validate' or 'complete'.")
    parser.add_argument("postcode", "-p", type=str, help="The postcode string.")
    args = parser.parse_args()
    postcode = args.postcode.strip().upper()
    
    
    
    
"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--mode", "-m", required=True, choices=["validate", "complete"],
                        help="Choose a mode: 'validate' or 'complete'.")
    parser.add_argument("postcode", type=str, help="The postcode string.")
    args = parser.parse_args()
    postcode = args.postcode.strip().upper()
    if args.mode == "validate":
        if validate_postcode(postcode):
            print(f"{postcode} is a valid postcode.")
        else:
            print(f"{postcode} is not a valid postcode.")
    if args.mode == "complete":
        results = get_postcode_completions(postcode)
        if results:
            for result in results[:5]:
                print(result.upper())
        else:
            print(f"No matches for {postcode}.")

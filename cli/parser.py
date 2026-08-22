import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--students",
        required=True,
        help="Path to students JSON file"
    )

    parser.add_argument(
        "--rooms",
        required=True,
        help="Path to rooms JSON file"
    )

    parser.add_argument(
        "--format",
        choices=["json", "xml"],
        required=True,
        help="Output format"
    )

    return parser.parse_args()
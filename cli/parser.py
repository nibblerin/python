import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--students",
        help="Path to students JSON file"
    )

    parser.add_argument(
        "--rooms",
        help="Path to rooms JSON file"
    )

    parser.add_argument(
        "--format",
        choices=["json", "xml"],
        required=True,
        help="Output format"
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Output file name. The extension is always taken from "
        "" "--format," \
        " so it can be omitted or will be corrected " "if it doesn't match.")

    parser.add_argument(
        "--use-indexes",
        action="store_true",
        help="Create additional indexes"
    )

    parser.add_argument(
        "--export-only",
        action="store_true",
        help="Export existing database data without reloading (WARNING: without this flag, existing tables are dropped and recreated)"
    )

    args = parser.parse_args()

    if not args.export_only and (not args.students or not args.rooms):
        parser.error(
            "--students and --rooms are required unless --export-only is used"
        )

    return args
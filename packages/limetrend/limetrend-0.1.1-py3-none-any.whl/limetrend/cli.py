import argparse
import asyncio

from limetrend import dynamodb


def create_parser():
    parser = argparse.ArgumentParser(description="Generate AWS cost reports")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    cost_parser = subparsers.add_parser("cost", help="Generate cost report")
    cost_parser.add_argument(
        "report", choices=["dynamodb"], help="Type of report to generate"
    )
    cost_parser.add_argument(
        "--days", type=int, default=30, help="Number of days to include in the report"
    )

    subparsers.add_parser("list-tables", help="List DynamoDB tables in all regions")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "cost":
        if args.report == "dynamodb":
            dynamodb.dynamodb_costs(args.days)
    elif args.command == "list-tables":
        asyncio.run(dynamodb.list_tables_all_regions())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

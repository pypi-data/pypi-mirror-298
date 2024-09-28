import asyncio
import datetime

from limetrend import aws_client, report


def dynamodb_costs(days=30):
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=days)
    result = aws_client.get_dynamodb_costs(start_date.isoformat(), end_date.isoformat())
    tables = asyncio.run(aws_client.get_dynamodb_tables_all_regions())

    processed_data = report.process_dynamodb_costs(result, start_date, end_date, tables)
    report_content = report.render_report(processed_data)
    print(report_content)


async def list_tables_all_regions():
    tables = await aws_client.get_dynamodb_tables_all_regions()
    table_to_regions = {}
    for region, region_tables in tables.items():
        for table in region_tables:
            if table not in table_to_regions:
                table_to_regions[table] = []
            table_to_regions[table].append(region)

    for table in sorted(table_to_regions.keys()):
        for region in sorted(table_to_regions[table]):
            print(f"{table:<40} {region}")

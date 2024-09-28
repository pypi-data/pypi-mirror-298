import asyncio

import boto3


async def get_dynamodb_tables_for_region(region):
    session = boto3.Session(region_name=region)
    client = session.client("dynamodb")
    response = await asyncio.to_thread(client.list_tables)
    return region, response.get("TableNames", [])


async def get_dynamodb_tables_all_regions():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    regions = [
        region["RegionName"] for region in ec2_client.describe_regions()["Regions"]
    ]

    semaphore = asyncio.Semaphore(15)

    async def bounded_get_tables(region):
        async with semaphore:
            return await get_dynamodb_tables_for_region(region)

    tasks = [bounded_get_tables(region) for region in regions]
    results = await asyncio.gather(*tasks)

    return {region: tables for region, tables in results if tables}


def get_dynamodb_costs(start_date, end_date):
    client = boto3.client("ce", region_name="us-east-1")
    response = client.get_cost_and_usage(
        TimePeriod={"Start": start_date, "End": end_date},
        Granularity="DAILY",
        Metrics=["BlendedCost", "UsageQuantity"],
        GroupBy=[
            {"Type": "DIMENSION", "Key": "USAGE_TYPE"},
            {"Type": "DIMENSION", "Key": "REGION"},
        ],
        Filter={"Dimensions": {"Key": "SERVICE", "Values": ["Amazon DynamoDB"]}},
    )
    return response

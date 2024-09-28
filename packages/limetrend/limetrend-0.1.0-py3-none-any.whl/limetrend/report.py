import datetime

import jinja2


def process_dynamodb_costs(result, start_date, end_date, tables):
    total_cost = 0
    usage_types = {}
    region_costs = {}
    table_costs = {
        table: 0 for region_tables in tables.values() for table in region_tables
    }
    daily_data = []

    def find_table_name(usage_type, region):
        # Check if the usage type contains a table name
        for table in tables.get(region, []):
            if table.lower() in usage_type.lower():
                return table
        # If no match, return None instead of "Unallocated"
        return None

    for period in result["ResultsByTime"]:
        start = datetime.datetime.strptime(
            period["TimePeriod"]["Start"], "%Y-%m-%d"
        ).date()
        days_ago = (end_date - start).days

        daily_cost = 0
        daily_usage_types = []

        for group in period["Groups"]:
            usage_type, region = group["Keys"]
            cost = float(group["Metrics"]["BlendedCost"]["Amount"])
            usage = float(group["Metrics"]["UsageQuantity"]["Amount"])

            daily_cost += cost
            total_cost += cost

            if usage_type not in usage_types:
                usage_types[usage_type] = 0
            usage_types[usage_type] += cost

            if region not in region_costs:
                region_costs[region] = 0
            region_costs[region] += cost

            table_name = find_table_name(usage_type, region)
            if table_name:
                if table_name not in table_costs:
                    table_costs[table_name] = 0
                table_costs[table_name] += cost

            daily_usage_types.append(
                {
                    "usage_type": usage_type,
                    "region": region,
                    "table_name": table_name,
                    "cost": cost,
                    "usage": usage,
                }
            )

        daily_data.append(
            {
                "date": start,
                "days_ago": days_ago,
                "cost": daily_cost,
                "estimated": period["Estimated"],
                "usage_types": daily_usage_types,
            }
        )

    usage_type_summary = [
        {"usage_type": ut, "cost": cost}
        for ut, cost in sorted(usage_types.items(), key=lambda x: x[1], reverse=True)
    ]

    region_cost_summary = [
        {"region": region, "cost": cost}
        for region, cost in sorted(
            region_costs.items(), key=lambda x: x[1], reverse=True
        )
    ]

    table_cost_summary = [
        {"table_name": table, "cost": cost}
        for table, cost in sorted(table_costs.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_cost": total_cost,
        "daily_data": daily_data,
        "usage_type_summary": usage_type_summary,
        "region_cost_summary": region_cost_summary,
        "table_cost_summary": table_cost_summary,
    }


def render_report(data):
    template = jinja2.Template("""
DynamoDB Costs and Usage:
Period: {{ data.start_date }} to {{ data.end_date }}

Detailed Results:
{% for day in data.daily_data %}
Date: {{ day.date }} ({{ day.days_ago }} days ago)
{% for ut in day.usage_types %}
  Usage Type: {{ ut.usage_type }}
    Region: {{ ut.region }}
    {% if ut.table_name %}Table: {{ ut.table_name }}{% else %}Table: Not specified{% endif %}
    Cost: ${{ "%.2f"|format(ut.cost) }}
    Usage Quantity: {{ "%.2f"|format(ut.usage) }}
{% endfor %}
Total Daily Cost: ${{ "%.2f"|format(day.cost) }}
Estimated: {{ "Yes" if day.estimated else "No" }}
{% endfor %}

Total Cost Breakdown by Usage Type:
{% for ut in data.usage_type_summary %}
{{ "%-40s"|format(ut.usage_type) }}: ${{ "%8.2f"|format(ut.cost) -}}
{% endfor %}

Total Cost Breakdown by Region:
{% for region in data.region_cost_summary %}
{{ "%-40s"|format(region.region) }}: ${{ "%8.2f"|format(region.cost) -}}
{% endfor %}

Total Cost Breakdown by Table:
{% for table in data.table_cost_summary %}
{{ "%-40s"|format(table.table_name) }}: ${{ "%8.2f"|format(table.cost) -}}
{% endfor %}

Total Cost for the period: ${{ "%.2f"|format(data.total_cost) }}
  """)

    return template.render(data=data)

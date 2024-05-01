# lens_data_extract.py

import requests


def extract_lens_prices(league_name):
    base_url = f"https://poe.ninja/api/data/currencyoverview?league={league_name}&type=Currency"

    try:
        response = requests.get(base_url)
        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data: {e}")

    for item in data["lines"]:
        if "currencyTypeName" in item:
            if item["currencyTypeName"] == "Prime Regrading Lens":
                cost_lens_primary = item["chaosEquivalent"]
            if item["currencyTypeName"] == "Secondary Regrading Lens":
                cost_lens_secondary = item["chaosEquivalent"]

    return cost_lens_primary, cost_lens_secondary


import csv
import io
from collections import Counter


def get_dashboard_statistics(donors, donations, requests, inventory):

    return {
        "total_donors": len(donors),
        "total_donations": len(donations),
        "total_requests": len(requests),
        "available_units": sum(inventory.values())
    }


def get_blood_group_statistics(donors):

    return dict(
        Counter(
            donor.get("blood_group", "Unknown")
            for donor in donors
        )
    )


def get_monthly_donations(donations):

    monthly_data = Counter()

    for donation in donations:

        date = donation.get("donation_date", "")

        if len(date) >= 7:
            month = date[:7]
            monthly_data[month] += 1

    return dict(sorted(monthly_data.items()))


def get_request_statistics(requests):

    return dict(
        Counter(
            request.get("status", "Unknown")
            for request in requests
        )
    )


def get_city_statistics(donors):

    return dict(
        Counter(
            donor.get("city", "Unknown")
            for donor in donors
        )
    )


def convert_to_csv(records):

    if not records:
        return ""

    output = io.StringIO()

    fieldnames = list(records[0].keys())

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
        extrasaction="ignore"
    )

    writer.writeheader()
    writer.writerows(records)

    return output.getvalue()

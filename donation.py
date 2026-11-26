
import json
import os
from datetime import datetime

DONATION_FILE = "data/donations.json"


def load_donations():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DONATION_FILE):
        save_donations([])
        return []

    try:

        with open(DONATION_FILE, "r") as file:

            content = file.read().strip()

            if not content:
                save_donations([])
                return []

            donations = json.loads(content)

            if isinstance(donations, list):
                return donations

            return []

    except json.JSONDecodeError:

        return []


def save_donations(donations):

    os.makedirs("data", exist_ok=True)

    with open(DONATION_FILE, "w") as file:
        json.dump(donations, file, indent=4)


def generate_donation_id():

    donations = load_donations()

    numbers = []

    for donation in donations:

        donation_id = donation.get("donation_id", "")

        if donation_id.startswith("DN"):

            try:
                numbers.append(int(donation_id[2:]))
            except ValueError:
                pass

    next_number = max(numbers, default=0) + 1

    return f"DN{next_number:03d}"


def add_donation(donation):

    donations = load_donations()

    donations.append(donation)

    save_donations(donations)


def search_donations(keyword):

    donations = load_donations()

    return [
        donation for donation in donations
        if keyword.lower() in donation.get("donation_id", "").lower()
        or keyword.lower() in donation.get("donor_id", "").lower()
        or keyword.lower() in donation.get("donor_name", "").lower()
    ]


def update_donation_status(donation_id, new_status):

    donations = load_donations()

    for donation in donations:

        if donation.get("donation_id") == donation_id:

            donation["status"] = new_status

            save_donations(donations)

            return True

    return False

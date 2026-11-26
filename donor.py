
import json
import os
from datetime import datetime

DATA_FILE = "data/donors.json"


class Donor:

    def __init__(self, donor_id, name, age, gender, blood_group, phone, city):

        self.donor_id = donor_id
        self.name = name
        self.age = age
        self.gender = gender
        self.blood_group = blood_group
        self.phone = phone
        self.city = city

    def to_dict(self):

        return {
            "donor_id": self.donor_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "blood_group": self.blood_group,
            "phone": self.phone,
            "city": self.city
        }


def save_donors(donors):

    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(donors, file, indent=4)


def load_donors():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        save_donors([])
        return []

    try:

        with open(DATA_FILE, "r") as file:
            content = file.read().strip()

            if not content:
                save_donors([])
                return []

            donors = json.loads(content)

        if not isinstance(donors, list):
            raise ValueError("Donor data must be a JSON list")

        valid_donors = []
        invalid_donors = []

        required_fields = [
            "donor_id",
            "name",
            "age",
            "gender",
            "blood_group",
            "phone",
            "city"
        ]

        for donor in donors:

            if (
                isinstance(donor, dict)
                and all(field in donor for field in required_fields)
            ):
                valid_donors.append(donor)

            else:
                invalid_donors.append(donor)

        # Backup invalid records before cleaning
        if invalid_donors:

            backup_file = (
                "data/invalid_donors_backup_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".json"
            )

            with open(backup_file, "w") as file:
                json.dump(invalid_donors, file, indent=4)

            save_donors(valid_donors)

        return valid_donors

    except (json.JSONDecodeError, ValueError):

        # Preserve the original file before recovery
        backup_file = (
            "data/donors_corrupt_backup_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".txt"
        )

        with open(DATA_FILE, "r") as original:
            original_content = original.read()

        with open(backup_file, "w") as backup:
            backup.write(original_content)

        save_donors([])

        return []


def save_donor(donor):

    donors = load_donors()

    donors.append(donor.to_dict())

    save_donors(donors)


def generate_donor_id():

    donors = load_donors()

    numbers = []

    for donor in donors:

        donor_id = donor.get("donor_id", "")

        if donor_id.startswith("DON"):

            try:
                numbers.append(int(donor_id[3:]))
            except ValueError:
                pass

    next_number = max(numbers, default=0) + 1

    return f"DON{next_number:03d}"


def search_donor(keyword):

    donors = load_donors()

    result = []

    for donor in donors:

        name = str(donor.get("name", ""))
        donor_id = str(donor.get("donor_id", ""))

        if (
            keyword.lower() in name.lower()
            or keyword.lower() in donor_id.lower()
        ):
            result.append(donor)

    return result


def update_donor(donor_id, updated_data):

    donors = load_donors()

    for donor in donors:

        if donor.get("donor_id") == donor_id:

            donor.update(updated_data)

            save_donors(donors)

            return True

    return False


def delete_donor(donor_id):

    donors = load_donors()

    updated_donors = [
        donor for donor in donors
        if donor.get("donor_id") != donor_id
    ]

    if len(updated_donors) == len(donors):
        return False

    save_donors(updated_donors)

    return True

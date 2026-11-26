
import json
import os

INVENTORY_FILE = "data/inventory.json"

BLOOD_GROUPS = [
    "A+", "A-", "B+", "B-",
    "AB+", "AB-", "O+", "O-"
]


def load_inventory():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(INVENTORY_FILE):
        inventory = {group: 0 for group in BLOOD_GROUPS}
        save_inventory(inventory)
        return inventory

    try:
        with open(INVENTORY_FILE, "r") as file:

            content = file.read().strip()

            if not content:
                inventory = {group: 0 for group in BLOOD_GROUPS}
                save_inventory(inventory)
                return inventory

            inventory = json.loads(content)

            for group in BLOOD_GROUPS:
                inventory.setdefault(group, 0)

            return inventory

    except json.JSONDecodeError:

        inventory = {group: 0 for group in BLOOD_GROUPS}
        save_inventory(inventory)

        return inventory


def save_inventory(inventory):

    os.makedirs("data", exist_ok=True)

    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)


def add_blood(group, units):

    inventory = load_inventory()

    inventory[group] += units

    save_inventory(inventory)


def remove_blood(group, units):

    inventory = load_inventory()

    if inventory[group] >= units:

        inventory[group] -= units

        save_inventory(inventory)

        return True

    return False


import json
import os

REQUEST_FILE = "data/requests.json"


class BloodRequest:

    def __init__(self, patient_name, blood_group, units, hospital, contact):
        self.request_id = generate_request_id()
        self.patient_name = patient_name
        self.blood_group = blood_group
        self.units = units
        self.hospital = hospital
        self.contact = contact
        self.status = "Pending"

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "patient_name": self.patient_name,
            "blood_group": self.blood_group,
            "units": self.units,
            "hospital": self.hospital,
            "contact": self.contact,
            "status": self.status
        }


def load_requests():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(REQUEST_FILE):
        save_requests([])
        return []

    try:
        with open(REQUEST_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_requests(requests):
    os.makedirs("data", exist_ok=True)

    with open(REQUEST_FILE, "w", encoding="utf-8") as file:
        json.dump(requests, file, indent=4)


def generate_request_id():
    requests = load_requests()
    numbers = []

    for item in requests:
        request_id = item.get("request_id", "")

        if request_id.startswith("REQ"):
            try:
                numbers.append(int(request_id[3:]))
            except ValueError:
                continue

    next_number = max(numbers, default=0) + 1

    return f"REQ{next_number:03d}"


def save_request(request):
    requests = load_requests()

    if isinstance(request, BloodRequest):
        request_data = request.to_dict()
    else:
        request_data = request

    requests.append(request_data)
    save_requests(requests)


def update_request_status(request_id, new_status):
    requests = load_requests()

    for item in requests:
        if item.get("request_id") == request_id:
            item["status"] = new_status
            save_requests(requests)
            return True

    return False

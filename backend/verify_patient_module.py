import requests
import uuid
from datetime import datetime

BASE_URL = "http://localhost:8000/v1"


def verify_patient_module():
    print("Starting Patient Module Verification...")

    # 1. Create Adult Patient
    print("\n1. Creating Adult Patient...")
    adult_patient_data = {
        "first_name": f"John_{uuid.uuid4().hex[:8]}",
        "last_name": "Doe",
        "date_of_birth": "1980-01-01",
        "age": 44,
        "gender": "Male",
        "phone_number": f"555-{uuid.uuid4().hex[:8]}",
        "email": "john.doe@example.com",
        "address": "123 Main St",
        "patient_type": "ADULT",
    }
    response = requests.post(f"{BASE_URL}/patient", json=adult_patient_data)
    if response.status_code == 200:
        adult_patient = response.json()
        print(f"Success: Created Adult Patient ID: {adult_patient['patient_id']}")
    else:
        print(f"Failed: {response.status_code} - {response.text}")
        return

    # 2. Create Pediatric Patient
    print("\n2. Creating Pediatric Patient...")
    pediatric_patient_data = {
        "first_name": f"Baby_{uuid.uuid4().hex[:8]}",
        "last_name": "Doe",
        "date_of_birth": "2020-01-01",
        "age": 4,
        "gender": "Female",
        "phone_number": f"555-{uuid.uuid4().hex[:8]}",  # Guardian's phone usually, but unique for now
        "email": "baby.doe@example.com",
        "address": "123 Main St",
        "patient_type": "PEDIATRIC",
        "guardian_name": "Jane Doe",
        "guardian_phone": "555-9999",
    }
    response = requests.post(f"{BASE_URL}/patient", json=pediatric_patient_data)
    if response.status_code == 200:
        pediatric_patient = response.json()
        print(
            f"Success: Created Pediatric Patient ID: {pediatric_patient['patient_id']}"
        )
        assert pediatric_patient["guardian_name"] == "Jane Doe"
        assert pediatric_patient["patient_type"] == "PEDIATRIC"
    else:
        print(f"Failed: {response.status_code} - {response.text}")
        return

    # 3. List Patients
    print("\n3. Listing Patients...")
    response = requests.get(f"{BASE_URL}/patients")
    if response.status_code == 200:
        patients = response.json()
        print(f"Success: Retrieved {len(patients)} patients")
        found_adult = any(
            p["patient_id"] == adult_patient["patient_id"] for p in patients
        )
        found_pediatric = any(
            p["patient_id"] == pediatric_patient["patient_id"] for p in patients
        )
        if found_adult and found_pediatric:
            print("Verified both patients are in the list.")
        else:
            print("Error: Could not find created patients in list.")
    else:
        print(f"Failed: {response.status_code} - {response.text}")

    # 4. Get Patient By ID
    print("\n4. Getting Pediatric Patient by ID...")
    response = requests.get(f"{BASE_URL}/patient/{pediatric_patient['patient_id']}")
    if response.status_code == 200:
        fetched_patient = response.json()
        print(f"Success: Retrieved Patient {fetched_patient['first_name']}")
        assert fetched_patient["guardian_name"] == "Jane Doe"
    else:
        print(f"Failed: {response.status_code} - {response.text}")

    # 5. Update Patient
    print("\n5. Updating Adult Patient...")
    update_data = {"first_name": f"JohnUpdated_{uuid.uuid4().hex[:4]}"}
    response = requests.put(
        f"{BASE_URL}/patient/{adult_patient['patient_id']}", json=update_data
    )
    if response.status_code == 200:
        updated_patient = response.json()
        print(f"Success: Updated name to {updated_patient['first_name']}")
        assert updated_patient["first_name"] == update_data["first_name"]
    else:
        print(f"Failed: {response.status_code} - {response.text}")

    # 6. Delete Patient
    print("\n6. Deleting Adult Patient...")
    response = requests.delete(f"{BASE_URL}/patient/{adult_patient['patient_id']}")
    if response.status_code == 200:
        print("Success: Deleted Adult Patient")
    else:
        print(f"Failed: {response.status_code} - {response.text}")

    # Verify Deletion
    print("\n7. Verifying Deletion...")
    response = requests.get(f"{BASE_URL}/patient/{adult_patient['patient_id']}")
    if response.status_code == 404:
        print("Success: Patient not found as expected.")
    else:
        print(
            f"Failed: Patient still exists or other error. Status: {response.status_code}"
        )


if __name__ == "__main__":
    verify_patient_module()

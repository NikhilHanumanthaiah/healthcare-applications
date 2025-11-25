"""
Test script to verify patient module is working correctly
"""

import requests
import json

BASE_URL = "http://localhost:8000/v1"


def test_create_patient():
    """Test creating a new patient"""
    patient_data = {
        "first_name": "Ravi",
        "last_name": "Kumar",
        "date_of_birth": "1993-05-14",
        "age": 32,
        "gender": "Male",
        "phone_number": "+91-9876543211",  # Changed to avoid duplicate
        "email": "ravi.kumar@example.com",
        "address": "12 MG Road, Bengaluru",
        "patient_type": "ADULT",
        "guardian_name": None,
        "guardian_phone": None,
    }

    print("🧪 Testing Patient Creation...")
    print(f"📤 Sending: {json.dumps(patient_data, indent=2)}")

    response = requests.post(f"{BASE_URL}/patient", json=patient_data)

    print(f"\n📥 Response Status: {response.status_code}")
    print(f"📥 Response Body: {json.dumps(response.json(), indent=2, default=str)}")

    if response.status_code == 200:
        print("✅ Patient created successfully!")
        return response.json()
    else:
        print("❌ Failed to create patient")
        return None


def test_list_patients():
    """Test listing patients"""
    print("\n🧪 Testing List Patients...")
    response = requests.get(f"{BASE_URL}/patients")

    print(f"📥 Response Status: {response.status_code}")
    print(f"📥 Found {len(response.json())} patients")

    if response.status_code == 200:
        print("✅ Successfully retrieved patients list!")
        for patient in response.json():
            print(
                f"  - {patient['first_name']} {patient['last_name']} (ID: {patient['patient_id']})"
            )
        return response.json()
    else:
        print("❌ Failed to list patients")
        return None


def test_get_patient(patient_id):
    """Test getting a specific patient"""
    print(f"\n🧪 Testing Get Patient (ID: {patient_id})...")
    response = requests.get(f"{BASE_URL}/patient/{patient_id}")

    print(f"📥 Response Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ Successfully retrieved patient!")
        print(f"📥 Response: {json.dumps(response.json(), indent=2, default=str)}")
        return response.json()
    else:
        print("❌ Failed to get patient")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("🏥 PATIENT MODULE TEST SUITE")
    print("=" * 60)

    # Test 1: Create patient
    created_patient = test_create_patient()

    # Test 2: List patients
    patients = test_list_patients()

    # Test 3: Get specific patient
    if created_patient:
        test_get_patient(created_patient["patient_id"])

    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

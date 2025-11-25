"""
Simple test to verify patient creation works
"""

import requests
import json

BASE_URL = "http://localhost:8000/v1"

# Test data
patient_data = {
    "first_name": "Ravi",
    "last_name": "Kumar",
    "date_of_birth": "1993-05-14",
    "age": 32,
    "gender": "Male",
    "phone_number": "+91-9876543299",
    "email": "ravi.kumar@example.com",
    "address": "12 MG Road, Bengaluru",
    "patient_type": "ADULT",
}

print("Testing Patient Creation...")
print(f"Data: {json.dumps(patient_data, indent=2)}\n")

try:
    response = requests.post(f"{BASE_URL}/patient", json=patient_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}\n")

    if response.status_code == 200:
        print("✅ SUCCESS! Patient created successfully!")
        patient = response.json()
        print(f"Patient ID: {patient['patient_id']}")
        print(f"Name: {patient['first_name']} {patient['last_name']}")
        print(f"Gender: {patient['gender']}")
        print(f"Email: {patient['email']}")
    else:
        print("❌ FAILED!")

except Exception as e:
    print(f"❌ Error: {e}")

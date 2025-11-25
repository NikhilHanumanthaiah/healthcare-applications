"""
Comprehensive Patient Module Test Suite
Tests all CRUD operations: Create, Read, Update, Delete
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/v1"


def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_create_patient():
    """Test creating a new patient"""
    print_section("TEST 1: CREATE PATIENT")

    patient_data = {
        "first_name": "Priya",
        "last_name": "Sharma",
        "date_of_birth": "1995-08-20",
        "age": 29,
        "gender": "Female",
        "phone_number": f"+91-98765{datetime.now().microsecond % 100000:05d}",  # Unique phone
        "email": "priya.sharma@example.com",
        "address": "45 Brigade Road, Bengaluru",
        "patient_type": "ADULT",
    }

    print(
        f"\n📤 Creating patient: {patient_data['first_name']} {patient_data['last_name']}"
    )

    try:
        response = requests.post(f"{BASE_URL}/patient", json=patient_data)

        if response.status_code == 200:
            patient = response.json()
            print(f"✅ SUCCESS! Patient created")
            print(f"   Patient ID: {patient['patient_id']}")
            print(f"   Name: {patient['first_name']} {patient['last_name']}")
            print(f"   Gender: {patient['gender']}")
            print(f"   Email: {patient['email']}")
            print(f"   Phone: {patient['phone_number']}")
            return patient["patient_id"]
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None


def test_get_patient(patient_id):
    """Test retrieving a specific patient"""
    print_section("TEST 2: GET PATIENT BY ID")

    print(f"\n📤 Fetching patient: {patient_id}")

    try:
        response = requests.get(f"{BASE_URL}/patient/{patient_id}")

        if response.status_code == 200:
            patient = response.json()
            print(f"✅ SUCCESS! Patient retrieved")
            print(f"   Name: {patient['first_name']} {patient['last_name']}")
            print(f"   Age: {patient['age']}")
            print(f"   Gender: {patient['gender']}")
            print(f"   Email: {patient['email']}")
            return True
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_list_patients():
    """Test listing all patients"""
    print_section("TEST 3: LIST ALL PATIENTS")

    print("\n📤 Fetching patient list...")

    try:
        response = requests.get(f"{BASE_URL}/patients?skip=0&limit=10")

        if response.status_code == 200:
            patients = response.json()
            print(f"✅ SUCCESS! Found {len(patients)} patients")
            for i, patient in enumerate(patients[:5], 1):  # Show first 5
                print(
                    f"   {i}. {patient['first_name']} {patient['last_name']} - {patient['gender']}"
                )
            if len(patients) > 5:
                print(f"   ... and {len(patients) - 5} more")
            return True
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_update_patient(patient_id):
    """Test updating a patient"""
    print_section("TEST 4: UPDATE PATIENT")

    update_data = {
        "email": "priya.sharma.updated@example.com",
        "address": "New Address: 100 MG Road, Bengaluru",
    }

    print(f"\n📤 Updating patient: {patient_id}")
    print(f"   New email: {update_data['email']}")
    print(f"   New address: {update_data['address']}")

    try:
        response = requests.put(f"{BASE_URL}/patient/{patient_id}", json=update_data)

        if response.status_code == 200:
            patient = response.json()
            print(f"✅ SUCCESS! Patient updated")
            print(f"   Email: {patient['email']}")
            print(f"   Address: {patient['address']}")
            return True
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_delete_patient(patient_id):
    """Test soft-deleting a patient"""
    print_section("TEST 5: DELETE PATIENT")

    print(f"\n📤 Deleting patient: {patient_id}")

    try:
        response = requests.delete(f"{BASE_URL}/patient/{patient_id}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! {result['message']}")
            return True
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_verify_deletion(patient_id):
    """Verify patient is soft-deleted (not in active list)"""
    print_section("TEST 6: VERIFY DELETION")

    print(f"\n📤 Verifying patient {patient_id} is deleted...")

    try:
        response = requests.get(f"{BASE_URL}/patient/{patient_id}")

        if response.status_code == 404:
            print(f"✅ SUCCESS! Patient is no longer accessible (soft-deleted)")
            return True
        else:
            print(
                f"⚠️  WARNING: Patient still accessible (Status: {response.status_code})"
            )
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "🏥 " * 30)
    print("     HEALTHCARE APPLICATION - PATIENT MODULE TEST SUITE")
    print("🏥 " * 30)

    results = []

    # Test 1: Create
    patient_id = test_create_patient()
    results.append(("Create Patient", patient_id is not None))

    if patient_id:
        # Test 2: Get by ID
        results.append(("Get Patient", test_get_patient(patient_id)))

        # Test 3: List
        results.append(("List Patients", test_list_patients()))

        # Test 4: Update
        results.append(("Update Patient", test_update_patient(patient_id)))

        # Test 5: Delete
        results.append(("Delete Patient", test_delete_patient(patient_id)))

        # Test 6: Verify deletion
        results.append(("Verify Deletion", test_verify_deletion(patient_id)))

    # Summary
    print_section("TEST SUMMARY")
    print()
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}  {test_name}")

    print(f"\n   Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n   🎉 ALL TESTS PASSED! Patient module is fully functional!")
    else:
        print(f"\n   ⚠️  {total - passed} test(s) failed. Please review.")

    print("\n" + "=" * 60 + "\n")

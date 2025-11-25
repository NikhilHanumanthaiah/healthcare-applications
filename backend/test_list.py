import requests

r = requests.get("http://localhost:8000/v1/patients")
print(f"Status: {r.status_code}")
if r.status_code == 200:
    patients = r.json()
    print(f"Count: {len(patients)} patients")
    for p in patients[:3]:
        print(
            f"  - {p['first_name']} {p.get('last_name', '')} ({p.get('gender', 'N/A')})"
        )
else:
    print(f"Error: {r.text}")

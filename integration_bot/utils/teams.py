import os
import requests

# Disable SSL warnings when verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_teams_with_factions(token: str) -> list:
    url = os.getenv("API_URL") + "/team/admin/teamswithfactions"
    headers = {"Authorization": f"Bearer {token}"}
    print(f"[FETCH] Fetching teams with factions...")
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json().get('data', [])
        print(f"[FETCH] Retrieved {len(data)} teams.")
        return data
    else:
        print(f"[FETCH] Failed to fetch teams. Status: {response.status_code}, Response: {response.text}")
        raise Exception("Failed to fetch teams.")
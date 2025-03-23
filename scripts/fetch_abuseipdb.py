import requests
import pandas as pd

# API Key of AbuseIPDB
API_KEY = "API_KEY_FROM_AbuseIPDB"

# Endpoint of AbuseIPDB for fetching IP addresses
url = "https://api.abuseipdb.com/api/v2/blacklist"

headers = {
    "Key": API_KEY,
    "Accept": "application/json"
}

# Parameters to get the confidence abuse score 97
params = {
    "confidenceMinimum": 97
}

# API request
response = requests.get(url, headers=headers, params=params)

# Checking the response of above API request
if response.status_code == 200:
    data = response.json()

    ip_list = []
    for report in data.get('data', []):  # Ensure data key exists
        ip_list.append({
                "IP Address": report["ipAddress"],
                "Abuse Score": report["abuseConfidenceScore"],
                "Country": report["countryCode"],
            })

    # Exporting the data (response) to Excel file
    if ip_list:
        df = pd.DataFrame(ip_list)
        df.to_excel("AbuseIPDB_Report_Raw.xlsx", index=False)
        print("AbuseIPDB Raw Report saved successfully!")
    else:
        print("No IPs found with an abuse score > 97.")
else:
    print(f"Error: {response.status_code}: {response.text}")

import requests
import pandas as pd
from setup_mongodb import collection

# API Key of VirusTotal
VT_API_KEY = "API_KEY_FROM_VirusTotal"

# VirusTotal Endpoint
VT_URL = "https://www.virustotal.com/api/v3/ip_addresses/"

headers = {"x-apikey": VT_API_KEY}

excel_data = []     # List to store data for Excel


excel_file = "AbuseIPDB_Sample_100_rows.xlsx"           # File name / path
df = pd.read_excel(excel_file, engine='openpyxl')       # Reading the file, containing sample (first) 100 IPs


# Fetching VirusTotal data for each IP address and store in MongoDB
for index, row in df.iterrows():
    response = requests.get(VT_URL + row["IP Address"], headers=headers)
    vt_data = response.json()

    entry = {
        "IP Address": row["IP Address"],
        "Reputation Score": vt_data.get("data", {}).get("attributes", {}).get("reputation"),
        "Country": vt_data.get("data", {}).get("attributes", {}).get("country"),
        "Detected Samples": vt_data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0),
        "Undetected Samples": vt_data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("undetected", 0),
        "Detected URLs": vt_data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0),
        "Undetected URLs": vt_data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("undetected", 0),

    }

    collection.insert_one(entry)       # Insert into MongoDB

    # Create entry for Excel (excluding URLs)
    excel_entry = {
        "IP Address": row["IP Address"],
        "Reputation Score": entry["Reputation Score"],
        "Country": entry["Country"],
        "Detected Samples": entry["Detected Samples"],
        "Undetected Samples": entry["Undetected Samples"],
    }

    excel_data.append(excel_entry)


# Convert list (excel_data created in above line (line no: 13)) to DataFrame
df_output = pd.DataFrame(excel_data)

# Save dataframe to Excel
output_file = "VirusTotal_Output.xlsx"
df_output.to_excel(output_file, index=False, engine="openpyxl")

print(f"VirusTotal response is stored in MongoDB and saved to {output_file}.")

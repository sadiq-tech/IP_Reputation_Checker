import requests
import pandas as pd
import time

# API Key of AbuseIPDB
API_KEY = "693fcf1d104b444c14a1db9bef098e8f5aed8e9f177bb0571b88c599404b84502ac31315dfecd249"

# Endpoint of AbuseIPDB for enrichment of IP Address
CHECK_URL = "https://api.abuseipdb.com/api/v2/check"

input_file = "AbuseIPDB_Report_Raw.xlsx"        # Input file with IPs
output_file = "AbuseIPDB_Enriched_Report.xlsx"  # Output file after enrichment


# Extracting the 100 rows of data (100 IPs) from the Input_file (AbuseIPDB_Report_Raw.xlsx)
df1 = pd.read_excel(input_file, engine='openpyxl')

df_sample_100 = df1.head(100)
#print(df_sample_100)

sample_100_output_file = "AbuseIPDB_Sample_100_rows.xlsx"
df_sample_100.to_excel(sample_100_output_file, index=False)

print(f"The sample of 100 rows saved successfully to : {sample_100_output_file}")

df = pd.read_excel("AbuseIPDB_Sample_100_rows.xlsx", engine="openpyxl")

# Checking IP Address column exists
if "IP Address" not in df.columns:
    raise ValueError("❌ 'IP Address' column is missing in the Excel file.")

# Creating new columns for enrichment
df["ISP"] = ""
df["Domain"] = ""
df["IP Version"] = ""
df["Is Whitelisted"] = ""
df["Usage Type"] = ""
df["Distinct Users"] = ""

headers = {
    "Key": API_KEY,
    "Accept": "application/json"
}


for index, row in df.iterrows():
    ip = row["IP Address"]

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90      # Fetch reports from the last 90 days
    }

    response = requests.get(CHECK_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get("data", {})

        # Updating DataFrame with enriched values
        df.at[index, "ISP"] = data.get("isp", "N/A")
        df.at[index, "Domain"] = data.get("domain", "N/A")
        df.at[index, "IP Version"] = data.get("ipVersion", "N/A")
        df.at[index, "Is Whitelisted"] = data.get("isWhitelisted", "N/A")
        df.at[index, "Usage Type"] = data.get("usageType", "N/A")
        df.at[index, "Distinct Users"] = data.get("numDistinctUsers", "N/A")

    else:
        print(f"Error fetching details for {ip}: {response.status_code}")

    time.sleep(1)  # delay to prevent API rate limiting

# Saving the Enriched data to output (AbuseIPDB_Enriched_Report.xlsx) file
df.to_excel(output_file, index=False)

print(f"Enriched data saved successfully to : {output_file}")

# **IP Reputation Check & Threat Intelligence**

This project automates the process of checking IP reputation using **VirusTotal** and **AbuseIPDB** APIs. The results and enriched data of IPs are stored in a **MongoDB** database, exported to an **Excel file**, and visualized in a **PDF file** (Bar Chart & Heatmap). Additionally, an automated email report is sent with relevant data visualizations.

## **Features**
- Fetches IP reputation data from VirusTotal.
- Stores data in MongoDB.
- Generates an Excel report.
- Sends automated email reports with attachments.
- Includes visual charts for better insights.

## **Technologies Used**
- **Python** (`requests`, `os`, `subprocess`, `time`, `pymongo`, `pandas`, `smtplib`, `matplotlib`, `seaborn`)
- **AbuseIPDB API** for fetching IP addresses  
- **VirusTotal API** for IP analysis  
- **MongoDB** for storing results  
- **Excel File Handling** using `pandas`  
- **Data Visualization** using `matplotlib` & `seaborn`  
- **Email Automation** with `SMTP`  

## **Note**
- The script fetches **10,000 IP addresses** using the **AbuseIPDB API**.  
- To optimize computation and save time, **only the first 100 IPs** are selected for enrichment and reputation analysis.  
- The **automated email report** includes a tabular summary of the reputation analysis for these **100 IPs**.  
- **Data visualization** is performed to provide insights into security threats:  
  - **Top 10 IPs with the Highest Detected Samples**  
  - **Malicious IP Distribution by Country**  
- These insights help drive **security measures** and improve **threat intelligence**.  

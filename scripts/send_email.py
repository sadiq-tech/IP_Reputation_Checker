import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from setup_mongodb import collection


# Fetch data from MongoDB and convert to DataFrame (Excluding "Detected URLs" & "Undetected URLs")
data = list(collection.find({}, {"_id": 0, "Detected URLs": 0, "Undetected URLs": 0}))
df_results = pd.DataFrame(data)

# Convert dataFrame to HTML table
html_table = df_results.to_html(index=False, border=1)


"""---------------- Sending Email ----------------- """
# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "email_password"
RECEIVER_EMAILS = ["xyz@gmail.com"]
CC_EMAILS = ["pqr@gmail.com"]

# Creating email message
msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = ", ".join(RECEIVER_EMAILS)

# Adding CC (only if there are email IDs present in CC)
if CC_EMAILS:
    msg["Cc"] = ", ".join(CC_EMAILS)

msg["Subject"] = "IP Reputation Report | Optiv Solutions"

# Adding data of above (line no: 16) converted to HTML table
html_body = f"""
<html>
    <body>
        <p>Hi Manager,</p>

        <p>I have successfully completed the <b>IP Reputation Check </b> project as per the given requirements. The project covers:</p>

        <ul>
            <li>The <b>AbuseIPDB API</b> fetched 10,000 IP addresses.</li>
            <li>To optimize computation and save time, <b>only the first 100 IPs</b> are selected for enrichment and reputation analysis.</li>
            <li>Performing <b>IP reputation checks</b> using <b>VirusTotal</b> and storing key attributes in <b>MongoDB</b>.</li>
            <li>Sending an <b>automated email report</b> with the <b>AbuseIPDB results attached</b> and <b>VirusTotal results displayed in a tabular format</b>.</li>
        </ul>

        <p>Additionally, I went beyond the core requirements and incorporated:</p>

        <ul>
            <li><b>IP Enrichment</b> – Enriching the AbuseIPDB (100 IPs) output with additional data fields, for further analysis.</li>
            <li><b>Data Visualization</b> – Creating insightful <b>bar charts & heatmaps</b> for better threat analysis.</li>
            <li>The <b>automated email report</b> includes a <b>tabular summary</b> of the reputation analysis for these <b>100 IPs</b>.</li>
        </ul>

        <h3>VirusTotal Results</h3>
        <p>Below is the <b>tabular format</b> of the VirusTotal reputation check:</p>

        {html_table}

        <h3>Attachments:</h3>
        <ul>
            <li>📄 <b>Response (raw) data from AbuseIPDB</b> – <i>AbuseIPDB_Report_Raw.xlsx</i></li>
            <li>📄 <b>Enriched Data</b> – <i>AbuseIPDB_Enriched_Report.xlsx</i></li>
            <li>🖼️ <b>Screenshot of collection ‘AbuseVT’ in MongoDB</b> – <i>MongoDB_AbuseVT.png</i></li>
            <li>📊 <b>Visualization of VirusTotal response</b> – <i>Visuals_VT_Data.pdf</i></li>
        </ul>

        <p>The project deliverables, including <b>code, reports, and visualizations</b>, can be found in my GitHub repository:</p>
        <p>🔗 <a href="[GitHub Repository Link]"><b>GitHub Repository Link</b></a></p>

        <p>Please review the project, and let me know if any modifications are needed.</p>

        <p>Looking forward to your feedback.</p>
        
        <br>
        <p>Thanks & Regards,<br>Your_Name.</p>
</html>
"""
msg.attach(MIMEText(html_body, "html"))

# Attaching files
files_to_attach = ["AbuseIPDB_Report_Raw.xlsx", "AbuseIPDB_Enriched_Report.xlsx", "MongoDB_AbuseVT.png", "Visuals_VT_Data.pdf"]

for file_path in files_to_attach:
    if os.path.exists(file_path):  # Check if file exists
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
        msg.attach(part)
    else:
        print(f"Warning: {file_path} not found. Skipping attachment.")

# Combining To & CC recipient IDs
ALL_RECIPIENTS = RECEIVER_EMAILS + CC_EMAILS if CC_EMAILS else RECEIVER_EMAILS

# Send email
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, ALL_RECIPIENTS, msg.as_string())
    server.quit()
    print("Email sent successfully with attachments !")
except Exception as e:
    print(f"Error: {e}")

import subprocess

print("Starting IP Reputation Checker...")

# Running the scripts (respective files)
subprocess.run(["python", "fetch_abuseipdb.py"])
subprocess.run(["python","enrich.py"])
subprocess.run(["python", "setup_mongodb.py"])
subprocess.run(["python", "check_virustotal.py"])
subprocess.run(["python", "send_email.py"])

print("Process completed !")

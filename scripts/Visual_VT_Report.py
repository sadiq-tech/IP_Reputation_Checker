import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "VirusTotal_Output.xlsx"                # Response of virusTotal
df = pd.read_excel(file_path, engine="openpyxl")    # Reading the above file

# Taking top 10 IPs and sorting detected amples
top_ips = df.sort_values(by="Detected Samples", ascending=False).head(10)

# Grouping data by country and summing up the detected samples
country_counts = df.groupby("Country")["Detected Samples"].sum().reset_index()
top_countries = country_counts.sort_values(by="Detected Samples", ascending=False).head(10)

# Creating a single figure with two subplots (charts / graphs)
fig, axes = plt.subplots(2, 1, figsize=(12, 12))  # (rows, columns)

# Plotting the bar chart for --> Top 10 IPs with the Highest Detected Samples
axes[0].barh(top_ips["IP Address"], top_ips["Detected Samples"], color="lightblue")
axes[0].set_xlabel("Detected Samples")
axes[0].set_ylabel("IP Address", rotation=0, labelpad=50)
axes[0].set_title("Top 10 IPs with the Highest Detected Samples")
axes[0].invert_yaxis()  # Invert y-axis to show the highest on top
axes[0].grid(axis="x", linestyle="--", alpha=0.7)
#axes[0].set_yticklabels(top_ips["IP Address"], rotation=0)


# Creating the heatmap for -->  Malicious IP Distribution by Country
sns.heatmap(top_countries.set_index("Country"), annot=True, fmt=".0f", cmap="Reds", linewidths=0.5, ax=axes[1])
axes[1].set_title("Malicious IP Distribution by Country")
axes[1].set_ylabel("Country", rotation=0, labelpad=30)
axes[1].set_yticklabels(axes[1].get_yticklabels(), rotation=0)


plt.tight_layout()  # Layout adjustments for better view.

# Adjusting the paddings
plt.subplots_adjust(top=0.905)
plt.subplots_adjust(bottom=0.1)
plt.subplots_adjust(hspace=0.427)
plt.subplots_adjust(wspace=0.206)
plt.subplots_adjust(left=0.288)
plt.subplots_adjust(right=0.735)

# Saving the generated / created charts as PDF file.
plt.savefig('Visuals_VT_Data.pdf', format="pdf", pad_inches="0.1")

import pandas as pd
import matplotlib.pyplot as plt


# STEP 1: Load CSV files

files = [
    "api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv",
    "api_data_aadhar_enrolment/api_data_aadhar_enrolment_500000_1000000.csv",
    "api_data_aadhar_enrolment/api_data_aadhar_enrolment_1000000_1006029.csv"
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

print("Total Records:", len(df))
print("Unique Raw States:", df["state"].nunique())



# STEP 2: Clean State Names


df["state_clean"] = df["state"].str.lower().str.strip()

fix_map = {
    "orissa": "odisha",
    "pondicherry": "puducherry",
    "westbengal": "west bengal",
    "west bengal": "west bengal",
    "jammu & kashmir": "jammu and kashmir",
    "andaman & nicobar islands": "andaman and nicobar islands",
    "dadra & nagar haveli": "dadra and nagar haveli and daman and diu",
    "daman and diu": "dadra and nagar haveli and daman and diu",
    "daman & diu": "dadra and nagar haveli and daman and diu",
    "dadra and nagar haveli": "dadra and nagar haveli and daman and diu",
    "100000": None
}

df["state_clean"] = df["state_clean"].replace(fix_map)
df = df[df["state_clean"].notna()]

print("Final Clean States & UTs:", df["state_clean"].nunique())



# STEP 3: Calculate Total Enrolment


df["total_enrolment"] = (
    df["age_0_5"] +
    df["age_5_17"] +
    df["age_18_greater"]
)



# STEP 4: State-wise Summary

state_summary = (
    df.groupby("state_clean")["total_enrolment"]
    .sum()
    .reset_index()
    .sort_values(by="total_enrolment", ascending=False)
    .reset_index(drop=True)
)

state_summary["Overall_Rank"] = range(1, len(state_summary) + 1)



# STEP 5: Top 10 States

top10 = state_summary.head(10).copy()
top10["Top10_Rank"] = range(1, 11)

print("\n🏆 Top 10 States (Aadhaar Enrolment):")
print(top10[["Top10_Rank", "state_clean", "total_enrolment"]].to_string(index=False))



# STEP 6: Bottom 10 States

bottom10 = state_summary.tail(10).copy().reset_index(drop=True)
bottom10["Bottom10_Rank"] = range(1, 11)

print("\n🔻 Bottom 10 States (Aadhaar Enrolment):")
print(bottom10[["Bottom10_Rank", "state_clean", "total_enrolment"]].to_string(index=False))



# STEP 7: Top 10 Bar Chart


colors_top = ["#ce4040", "#6643e4", "#7bdf72"]

plt.figure(figsize=(10, 5))
bars = plt.bar(
    top10["state_clean"],
    top10["total_enrolment"],
    color=colors_top * 4
)

plt.xticks(rotation=45, ha="right")
plt.title("Top 10 States by Aadhaar Enrolment")
plt.xlabel("State")
plt.ylabel("Total New Aadhaar Enrolments")
plt.ticklabel_format(style="plain", axis="y")

for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        h,
        f"{int(h):,}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()
plt.show()



# STEP 8: Bottom 10 Bar Chart


colors_bottom = ["#2c2c9c", "#000000", "#7be26a"]

plt.figure(figsize=(12, 5))
bars = plt.bar(
    bottom10["state_clean"],
    bottom10["total_enrolment"],
    color=colors_bottom * 4
)

plt.xticks(rotation=45, ha="right")
plt.title("Bottom 10 States by Aadhaar Enrolment")
plt.xlabel("State")
plt.ylabel("Total New Aadhaar Enrolments")
plt.ticklabel_format(style="plain", axis="y")

for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        h,
        f"{int(h):,}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()
plt.show()



# STEP 9: Demographic Pulse Pie Chart


age_0_5_total = df["age_0_5"].sum()
age_5_17_total = df["age_5_17"].sum()
age_18_plus_total = df["age_18_greater"].sum()

labels = ["0–5 Years", "5–17 Years", "18+ Years"]
sizes = [age_0_5_total, age_5_17_total, age_18_plus_total]
colors_pie = ["#3b7dd8", "#e44bd8", "#7be26a"]

plt.figure(figsize=(7, 7))
plt.pie(
    sizes,
    labels=labels,
    colors=colors_pie,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Demographic Pulse of Aadhaar Enrolment")
plt.axis("equal")
plt.show()

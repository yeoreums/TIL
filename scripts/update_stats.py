import os
from datetime import date
import subprocess

folders = [
    "airflow",
    "data-engineering",
    "dbt",
    "dev-ops-and-system",
    "git-and-github",
    "linux",
    "python",
    "statistics"
]

files = []

# Collect all TIL markdown files
for folder in folders:
    for file in os.listdir(folder):
        if file.endswith(".md"):
            files.append(os.path.join(folder, file))

count = len(files)

# Get last commit timestamp for a file
def get_last_commit_time(filepath):
    try:
        result = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%ct", "--", filepath],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        return int(result) if result else 0
    except Exception:
        return 0


# Find most recently committed TIL file
latest_file = max(files, key=get_last_commit_time, default="")

latest_name = os.path.basename(latest_file)
latest_name = latest_name.replace(".md", "").replace("-", " ").title()

today = date.today().isoformat()

# Update README
with open("README.md", "r") as f:
    lines = f.readlines()

new_lines = []

for line in lines:

    if line.startswith("📚 Total TIL entries"):
        line = f"📚 Total TIL entries: {count}\n"

    if line.startswith("📅 Last updated"):
        line = f"📅 Last updated: {today}\n"

    if line.startswith("→") and latest_file:
        line = f"→ [{latest_name}]({latest_file})\n"

    new_lines.append(line)

with open("README.md", "w") as f:
    f.writelines(new_lines)
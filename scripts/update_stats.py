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
count = 0

for folder in folders:
    for file in os.listdir(folder):
        if file.endswith(".md"):
            path = os.path.join(folder, file)
            files.append(path)
            count += 1

# find latest committed TIL file using git history
latest_file = subprocess.check_output(
    [
        "git",
        "log",
        "-1",
        "--name-only",
        "--pretty=format:",
        "--",
        "airflow/*.md",
        "data-engineering/*.md",
        "dbt/*.md",
        "dev-ops-and-system/*.md",
        "git-and-github/*.md",
        "linux/*.md",
        "python/*.md",
        "statistics/*.md",
    ]
).decode().strip().split("\n")[0]

latest_name = os.path.basename(latest_file)
latest_name = latest_name.replace(".md", "").replace("-", " ").title()

today = date.today().isoformat()

with open("README.md", "r") as f:
    lines = f.readlines()

new_lines = []

for line in lines:

    if line.startswith("📚 Total TIL entries"):
        line = f"📚 Total TIL entries: {count}\n"

    if line.startswith("📅 Last updated"):
        line = f"📅 Last updated: {today}\n"

    if line.startswith("→"):
        line = f"→ [{latest_name}]({latest_file})\n"

    new_lines.append(line)

with open("README.md", "w") as f:
    f.writelines(new_lines)
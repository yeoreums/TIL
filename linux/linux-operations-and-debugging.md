# Linux TIL – Practical Commands (Basics + Real Usage)

This document is a collection of **Linux commands I actually used** while working on:

* Cloud VMs (GCP / AWS)
* Docker & Airflow environments
* systemd-managed long-running services
* Debugging data pipeline issues (logs, processes, disk, permissions)

It includes **basic commands** as well as **practical ones** that repeatedly helped me identify and fix real problems.

---

## 1. Navigation & Filesystem Basics

### Check current location

pwd

Shows the current working directory.

### List files

ls
ls -la

* `-l`: long format (permissions, owner, size)
* `-a`: include hidden files (files starting with `.`)

### Move between directories

cd /path/to/dir
cd ..
cd ~

---

## 2. File & Directory Management

### Create directories

mkdir data
mkdir -p logs/airflow/worker

* `-p`: create nested directories at once

### Copy / move / delete files

cp file.txt backup.txt
mv old.py new.py
rm file.txt
rm -r tmp/

⚠️ `rm -r` deletes directories recursively. Be careful on servers.

---

## 3. Finding Files

### Find files by name

find . -name "*.log"
find / -name "dbt_project.yml" 2>/dev/null

* Useful when config files exist but their location is unknown
* `2>/dev/null` hides permission-denied errors

---

## 4. Text Search with grep (Very Important)

### What does grep do?

`grep` searches **text patterns inside files or command output**.

In practice, it helps answer questions like:

* Does this log contain an error?
* Is this process running?
* Where is this keyword mentioned?

### Basic usage

grep "ERROR" app.log

Searches for the word `ERROR` inside `app.log`.

### Case-insensitive search

grep -i "error" app.log

### Search recursively in a directory

grep -R "snowflake" .

### Combine with other commands (very common)

ps aux | grep python
journalctl -u upbit-consumer | grep failed

* `|` (pipe) sends output from one command to another

---

## 5. Process Management

### List running processes

ps aux
top
htop

* Used to check whether producer / consumer processes are alive

### Kill a process

kill PID
kill -9 PID

* `-9`: force kill (last resort)

---

## 6. Background Processes & systemd

### Run a script in background (manual)

nohup python consumer.py &

This works, but is fragile for long-running services.

### systemd service management (production-style)

systemctl status upbit-consumer
systemctl start upbit-consumer
systemctl stop upbit-consumer
systemctl restart upbit-consumer
systemctl enable upbit-consumer

Used to migrate a consumer from manual execution to a stable service.

---

## 7. Logs & Debugging

### View log files

tail -n 100 app.log
tail -f app.log

* `-f`: follow logs in real time

### systemd logs

journalctl -u upbit-consumer
journalctl -u upbit-consumer -n 200
journalctl -u upbit-consumer -f

Essential for diagnosing silent crashes.

---

## 8. Disk & Storage Checks

### Disk usage

df -h

Shows disk usage by filesystem.

### Directory size

du -sh *

Used when data files were not being written as expected.

---

## 9. Networking Basics

curl [https://api.upbit.com/v1/market/all](https://api.upbit.com/v1/market/all)
ping google.com
ss -tulnp

* Verify outbound network access
* Check open ports on a server

---

## 10. Permissions

ls -l
chmod +x script.sh
chown ubuntu:ubuntu file.txt

Used to fix execution and access errors on servers and containers.

---

## 11. Environment & History

### Environment variables

env
echo $PATH
export ENV=prod

### Command history

history
history | grep systemctl

Helpful for reconstructing what was done during debugging sessions.

---

## 12. Container & Runtime Inspection (Used with Docker / Airflow)

### Check running containers

docker ps
docker ps -a

Used to verify whether Airflow worker / scheduler containers were running.

### Inspect container logs

docker logs airflow-worker
docker logs -f airflow-worker

Very useful when application logs were not written to files.

### Execute inside a running container

docker exec -it airflow-worker bash

Used to:

* run dbt manually
* check Python environments
* inspect mounted volumes

### Execute inside a container as root (debugging only)

docker exec -it --user root airflow-worker bash
whoami
id

Used temporarily when:

* file permissions blocked access
* inspecting system-level paths
* checking installed packages inside the container

---

## 13. Python Runtime & Virtual Environments (Debug Context)

### Check Python binary location

which python
which python3

Used to confirm whether the system Python or virtualenv Python was active.

### Check installed packages

pip list
pip show dbt-core

Used when dependency conflicts caused runtime errors.

---

## 14. File Ownership & Permission Debugging (Real Issues)

### Identify ownership

ls -l
stat file.txt

Used when Airflow or systemd services could not access files.

### Fix ownership recursively

chown -R ubuntu:ubuntu /home/ubuntu/project

Used after copying files as root or via Docker volumes.

---

## 15. Networking & Connectivity Debugging (VM-level)

### Check outbound IP

curl ifconfig.me

Used to verify which public IP the VM was using.

### DNS resolution

nslookup api.upbit.com

Used when API requests failed unexpectedly.

---

## 16. Scheduling & Time (Often Overlooked)

### Check system time

date
timedatectl

Used to verify timezone mismatches between:

* VM
* Airflow
* Snowflake

---

## Closing Note

This is not a Linux command reference.

It is a **practical record of commands used while operating and debugging data pipelines**, including VMs, containers, services, and runtime environments.

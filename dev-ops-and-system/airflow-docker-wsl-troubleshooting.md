# 🐳 Airflow/Docker/WSL Troubleshooting: Core Commands and Fixes

This document records essential Linux/Docker commands and YAML fixes used to troubleshoot common issues (port conflicts, permission errors, and disk space problems) encountered during the Apache Airflow Docker setup on WSL2/Ubuntu.

## 1. Complete Environment Cleanup & Disk Space Recovery

Use these commands when ports are conflicting or when you need to free up hard drive space consumed by Docker artifacts.

| Goal | Command | Description |
| :--- | :--- | :--- |
| **Stop All Containers** | `docker stop $(docker ps -aq)` | Stops all currently running containers to avoid conflicts before cleanup. |
| **Full Airflow Cleanup** | `docker compose down -v` | Stops and removes all Airflow containers and **associated volumes** (which store persistent data like the Postgres DB). Use inside the project directory. |
| **Reclaim Disk Space** | `docker system prune -a --volumes` | Removes all stopped containers, networks, dangling images, and **all unused volumes**. This is the single best command for freeing up Docker-related disk space. (Requires `y` confirmation). |
| **Remove Airflow Images** | `docker rmi -f $(docker images -q apache/airflow)` | Forces deletion of all local images tagged with `apache/airflow` to ensure a fresh build. |

## 2. System and File Cleanup

| Goal | Command | Execution Context |
| :--- | :--- | :--- |
| **Force Delete Folder** | `sudo rm -rf [folder-name]` | Linux/WSL. Overrides `permission denied` errors and completely deletes the directory and its contents. |
| **WSL Instance Reset** | `wsl --shutdown` | **Windows PowerShell**. Shuts down all running WSL distributions, resolving daemon connection issues or port hangups. |
| **Change File Ownership** | `sudo chown -R $USER:$USER [folder-name]` | Linux/WSL. Resolves `permission denied` errors by granting ownership back to the current user. |

***

## 3. Configuration and Diagnostics Fixes

### A. YAML and Shell Escaping Fix

| Issue | Code Fix | Rationale |
| :--- | :--- | :--- |
| **Shell Expansion** | `volumes: - \${AIRFLOW_PROJ_DIR:-.}/data:/opt/airflow/data` | The `\` (backslash) **escapes** the `$` sign, preventing the host shell (Bash) from expanding the variable. This forces the Docker Compose parser to handle the default value (`:-.`) correctly, preventing a common YAML parsing error. |

### B. Port Conflict Resolution

| Action | Command / Modification | Notes |
| :--- | :--- | :--- |
| **Check Webserver Logs** | `docker compose logs webserver` | Crucial for confirming the exact error (`Bind failed: port is already allocated`). |
| **Find Port Occupier** | `sudo netstat -tulpn | grep 8080` | Finds the Process ID (PID) of any application listening on port `8080`. |
| **YAML Port Change** | `ports: - "8090:8080"` | Changes the host access port (in `webserver` section) to a less common port like `8090` to bypass conflicts. |

### C. Airflow Integration Setup

| Setting | Context | Value / Command |
| :--- | :--- | :--- |
| **Access Airflow UI** | After fixing conflicts | `http://localhost:8080` (or `8090`) |
| **Slack Webhook URL** | Airflow UI Variable | Key: `slack_url` (Set in Admin > Variables) |

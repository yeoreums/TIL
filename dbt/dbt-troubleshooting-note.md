# dbt Troubleshooting Notes (EC2 + Docker)

## Context

* dbt was initially installed and configured **inside a running Docker container** on an EC2 instance.
* The setup worked correctly at that time: dbt commands executed successfully and models ran as expected.
* Later, another team member performed Docker-related operations (e.g. `docker compose down`, rebuild, or re-init), which resulted in **container reset**.
* After that point, dbt-related files and configurations appeared to be missing or inconsistent.

---

## What Happened

### 1. Initial Setup (Worked)

* dbt was installed manually inside the container.
* Configuration files (e.g. `profiles.yml`, dbt project files) lived **inside the container filesystem**.
* No explicit Docker volume was used to persist dbt-related files.
* Result: everything worked, but state existed only inside the container.

### 2. Container Rebuild / Reset

* A teammate ran Docker commands that recreated containers (e.g. rebuild, re-init).
* Docker containers are **ephemeral by default**.
* When the container was recreated:

  * Installed packages inside the container were lost.
  * dbt configuration files inside the container filesystem were removed.

### 3. Symptoms Observed

* dbt commands no longer found expected config or environment.
* `profiles.yml` appeared missing or empty.
* dbt behavior differed from previous runs, even though code had not changed.
* Confusion arose because some team members expected container state to persist.

---

## Root Cause

**dbt state lived inside the container, not on the host.**

Key points:

* Docker containers do **not** persist filesystem changes unless volumes are explicitly configured.
* Manual setup inside a container is fragile if others can rebuild or reset containers.
* Rebuilding Docker effectively resets the container to the image state.

This was not caused by dbt itself, but by an implicit assumption that container state would persist.

---

## Why This Was Hard to Notice

* dbt worked fine initially, giving a false sense of stability.
* Docker rebuilds happened later, by someone else.
* No clear signal indicated that container state had been reset.
* Errors surfaced indirectly (missing configs, path issues), not as a single clear failure.

---

## Lessons Learned

1. **Never rely on container-internal state for important tooling**

   * Anything installed or configured inside a container can disappear.

2. **Volumes are required for persistence**

   * dbt projects, profiles, and configs should live on the host and be mounted into containers.

3. **Rebuild-safe setup matters in team environments**

   * If someone else can run Docker rebuilds, the setup must survive them.

4. **Working once does not mean safe**

   * Success without persistence is still a fragile setup.

---

## Recommended Stable Setup (Future)

* Keep dbt project and configuration **outside the container**.
* Mount them using Docker volumes.
* Example (conceptual):

  * Host: `/home/ec2-user/dbt`
  * Container: `/opt/dbt`
* Install dbt as part of the Docker image or via reproducible scripts.
* Assume containers can be destroyed and recreated at any time.

---

## Takeaway

The issue was not a dbt bug or misconfiguration, but a **Docker persistence misunderstanding**.

Once container resets are expected and planned for, the problem becomes straightforward to avoid.

# 🐙 GitHub Workflow Guide for Team Projects

A comprehensive guide for managing collaborative data engineering projects using GitHub Issues, Milestones, and Pull Requests.
> **Background:** Adapted from my previous team's workflow and refined as team leader for current bootcamp project.

---

## 📋 Table of Contents

- [Milestones](#milestones)
- [Work Types (Labels)](#work-types-labels)
- [Workflow Steps](#workflow-steps)
- [Branch Naming](#branch-naming)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)

---

## 🎯 Milestones

Define project phases to track progress:

| Milestone | Description |
|-----------|-------------|
| Milestone 1 | Pipeline architecture design (Airflow DAG, infrastructure setup) |
| Milestone 2 | Data collection and CSV storage (extract/transform per team) |
| Milestone 3 | Database loading automation (Airflow → Snowflake) |
| Milestone 4 | Data transformation for visualization |
| Milestone 5 | Final dashboard and presentation |

---

## 🏷️ Work Types (Labels)

Use these labels for both Issues and Commits:

| Label | Description |
|-------|-------------|
| **FEAT** | New feature implementation |
| **FIX** | Bug fixes |
| **DOCS** | Documentation updates |
| **REFACTOR** | Code refactoring (no feature change) |
| **PERFORMANCE** | Performance improvements |
| **CHORE** | Build/config/dependency updates |
| **INFRA** | Infrastructure changes (EC2, Airflow, CI/CD) |
| **STRUCTURE** | Folder/file structure reorganization |

---

## 🔄 Workflow Steps

### 1. Create an Issue

**Issue Title Format:** `[WORK_TYPE] Brief description`

**Example:** `[FEAT] Build NASDAQ data collection DAG`

**Issue Details:**
- **Title:** Follow the format above
- **Description:** Provide detailed context about the task
- **Assignee:** Assign yourself
- **Labels:** Select appropriate label(s)
- **Projects:** Link to project board (e.g., "Economic Indicators")
- **Milestone:** Assign relevant milestone

### 2. Move Issue on Project Board

- Check that the issue appears on the project board
- Move it to **"In Progress"** before starting work

### 3. Create a Branch

**Branch Naming Format:** `#issue-number-description`

**Example:** `#15-stock-data-scraper`

```bash
git checkout main
git pull origin main
git checkout -b #15-stock-data-scraper
```

### 4. Commit Your Work

**Commit Message Format:** `work-type: description #issue-number`

**Example:** `feat: build NASDAQ data collection pipeline #15`

**Guidelines:**
- Keep description concise (around 50 characters)
- Use lowercase for work type
- Always reference the issue number

```bash
git add .
git commit -m "feat: add yfinance data extraction for NASDAQ #15"
git push origin #15-stock-data-scraper
```

### 5. Create a Pull Request

Use this template for consistency:

```markdown
### Related Issue
#15

### Changes Made
- Implemented yfinance data collection for NASDAQ/S&P500
- Created Airflow DAG for scheduled extraction
- Configured Snowflake auto-loading pipeline

### Notes
- Followed previous project architecture
- Tested with sample date range
```

**PR Checklist:**
- Link the related issue
- Request review from at least one team member
- Ensure CI/CD checks pass (if configured)
- Use **"Squash and Merge"** when merging to keep history clean

---

## 🌿 Branch Naming

| Situation | Branch Name Example |
|-----------|---------------------|
| New feature | `#12-airflow-dag-setup` |
| Bug fix | `#18-fix-snowflake-connection` |
| Documentation | `#5-update-readme` |

---

## 💬 Commit Messages

Good commit messages help the team understand changes at a glance.

**Examples:**

```bash
feat: add S3 file upload task to DAG #23
fix: resolve Airflow scheduler timezone issue #19
docs: add setup instructions for EC2 environment #7
refactor: simplify data transformation logic #31
chore: update requirements.txt with latest packages #14
```

---

## 🔀 Pull Requests

### Before Creating a PR:

1. Rebase your branch with main to avoid conflicts:
   ```bash
   git checkout main
   git pull origin main
   git checkout #15-stock-data-scraper
   git rebase main
   ```

2. Push your changes:
   ```bash
   git push -f origin #15-stock-data-scraper
   ```

### PR Review Process:

1. At least **one team member** must review and approve
2. Address any requested changes
3. Once approved, use **"Squash and Merge"** for a clean history
4. Delete the branch after merging

---

## 🎯 Quick Reference

| Action | Command/Format |
|--------|---------------|
| Create branch | `git checkout -b #15-description` |
| Commit | `work-type: description #issue-number` |
| Issue title | `[WORK_TYPE] Description` |
| Before PR | `git rebase main` |
| Merge strategy | Squash and Merge |

---

**Tags:** `#git` `#github` `#workflow` `#team-collaboration` `#project-management` `#best-practices`

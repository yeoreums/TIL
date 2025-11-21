# 🔀 Git Strategy: Rebase vs Merge (Team Project)

## ✅ When to Use Rebase

Use this for your feature branches. Keeps the commit history clean and linear.

### Workflow

1. `git checkout feature/my-task`
2. `git fetch origin`
3. `git rebase origin/main`
4. Resolve conflicts (if any)
5. `git push -f origin feature/my-task`

### Good for:
- Making a clean PR history
- Ensuring your branch is updated with the latest main before PR
- Avoiding messy merge commits

### Avoid if:
- Your branch is already merged
- You don't understand the conflict fully (can cause issues with `-f`)

---

## 🔁 When to Use Merge

Use this for Pull Requests and team collaboration. Keeps history safe and avoids rewriting public history.

### Workflow

1. Make PR → "Merge"
2. One reviewer approves
3. Merge either:
   - **Squash & Merge** (clean + recommended)
   - Regular merge

### Good for:
- Safety
- Team projects
- Combining all feature branch commits into one clear commit (using Squash)

---

## 🎯 Recommended Strategy for Bootcamp Team Project (Best Practice)

### ⭐ 1. You always rebase your feature branch

Every member does:

```bash
git checkout main
git pull origin main
git checkout feature/your-task
git rebase main
```

Then create a PR.

### ⭐ 2. Team always uses "Squash & Merge" for PRs

This creates ONE clean commit per task. Your main branch stays readable, like:

```
feat: add S3 ingestion script
fix: airflow schedule bug
chore: add logging for ETL
```

### ⭐ 3. Never rebase main after pushing

Avoid rewriting shared history.

---

## 🛠 Simple Decision Table

| Situation | Recommended Method |
|-----------|-------------------|
| Want to get latest code before starting work | `rebase` (feature branch) |
| Team review complete, merging to main | `merge` (PR) |
| Want cleanest possible commit history | `rebase` + `squash & merge` |
| Conflicts are too complex | Regular `merge` |

---

**Tags:** `#git` `#rebase` `#merge` `#version-control` `#team-collaboration` `#best-practices`

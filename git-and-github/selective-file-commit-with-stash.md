# Git: Pushing Only a Single File Using `git stash`

A common scenario: you have multiple local changes, but you only need to push a specific file (like `requirements.txt`) to the remote branch **right now**.

## 🚀 The Situation

I needed to update **only** `requirements.txt` to the `dev` branch on GitHub, but I had other local changes that were not ready to be committed or pushed yet.

## 🛠️ Step-by-Step Solution

This process uses `git stash` to safely isolate the changes you *don't* want to push, commit the single file you *do* want, and then restore the rest of your work.

| Step | Command | Explanation |
| :--- | :--- | :--- |
| **1. Stash All Changes** | `git stash -u` | Safely stashes **all** current local changes, including **untracked** files (`-u`), preserving your entire workspace state. |
| **2. Restore Only the Target File** | `git checkout stash -- requirements.txt` | This is the key step! It retrieves **only** `requirements.txt` from the most recent stash entry and places it back in your working directory, leaving the rest of the stash untouched. |
| **3. Stage and Commit** | `git add requirements.txt`<br>`git commit -m "feat: Update requirements.txt"` | Commit the isolated change. (Using a conventional commit prefix like `feat:` is good practice!) |
| **4. Pull and Rebase** | `git pull origin dev --rebase` | Always pull the latest changes from the remote branch (`dev`) and perform a **rebase**. This cleanly places your new commit on top of the remote's history, preventing a merge commit. |
| **5. Push the Commit** | `git push origin dev` | Push your single-file commit to the remote branch. |
| **6. Restore Other Changes** | `git stash pop` | Restores the rest of your stashed changes. The `requirements.txt` file is ignored during restoration since it has already been committed and is now identical to the remote version. |

## 💡 Key Takeaways

* The combination of `git stash -u` and `git checkout stash -- <file>` is a powerful pattern for **selective commits**.
* **`git checkout stash -- <filename>`** is a fundamental command for recovering individual files from a stash without restoring the whole thing.
* Always use **`git pull --rebase`** (instead of just `git pull`) before pushing if the remote branch has new commits. It keeps your branch history clean and linear.

## 📘 Common Git Commands Used

| Command | Purpose |
| :--- | :--- |
| `git stash -u` | Stash local changes, **including untracked files**. |
| `git checkout stash -- <file>` | **Restore a specific file** from the latest stash entry. |
| `git stash pop` | Restore the latest stash and delete it from the stash list. |
| `git pull <remote> <branch> --rebase` | Pull latest from remote, placing your local commits on top. |

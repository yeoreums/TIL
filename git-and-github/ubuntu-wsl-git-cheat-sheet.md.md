# 🐧 Ubuntu WSL Essential Commands Cheat Sheet

Essential commands for navigating files, system administration, package installation, and performing Git operations in the Ubuntu (Linux) environment on Windows Subsystem for Linux.

## 1. File and Directory Navigation

| Command | Purpose | Example |
|---------|---------|---------|
| `pwd` | Prints the full path of the current working directory | `pwd` |
| `ls` | Lists files and folders in the current directory | `ls` |
| `ls -al` | Lists files with detailed information (permissions, owner), including hidden files | `ls -al` |
| `cd [dir]` | Changes the current directory to the specified directory | `cd Documents` |
| `cd ..` | Moves up to the parent directory | `cd ..` |
| `cd ~` | Moves to the user's home directory | `cd ~` |
| `clear` | Clears all content from the terminal screen | `clear` |
| `history` | Prints a list of previously entered commands | `history` |

## 2. File and Directory Management

| Command | Purpose | Example |
|---------|---------|---------|
| `mkdir [name]` | Creates a new directory (folder) | `mkdir my_project` |
| `touch [file]` | Creates a new empty file or updates the timestamp | `touch main.py` |
| `cat [file]` | Prints the contents of a file to the terminal | `cat README.md` |
| `nano [file]` | Edits a file using the nano text editor | `nano config.yaml` |
| `vim [file]` | Edits a file using the vim text editor | `vim script.sh` |
| `cp [src] [dest]` | Copies a file or folder (use `-r` for folders) | `cp file.txt backup/` |
| `mv [src] [dest]` | Moves a file/folder or renames it | `mv old_name.txt new_name.txt` |
| `rm [file]` | Deletes a file (⚠️ irreversible) | `rm temp.log` |
| `rm -rf [dir]` | Forcefully deletes a directory and contents (⚠️ use with extreme caution) | `rm -rf project_trash` |
| `find [path] -name [pattern]` | Searches for files matching a pattern | `find . -name "*.py"` |
| `grep [pattern] [file]` | Searches for text pattern within files | `grep "TODO" *.js` |

## 3. Package Management (apt)

Must be executed with `sudo` for administrative privileges.

| Command | Purpose | Example |
|---------|---------|---------|
| `sudo apt update` | Updates the package list (run this first!) | `sudo apt update` |
| `sudo apt upgrade` | Upgrades all installed packages to latest versions | `sudo apt upgrade` |
| `sudo apt install [pkg]` | Installs a specific package | `sudo apt install python3-pip` |
| `sudo apt remove [pkg]` | Removes a specific package | `sudo apt remove vim` |
| `sudo apt autoremove` | Removes unused dependencies | `sudo apt autoremove` |
| `apt search [keyword]` | Searches for packages by keyword | `apt search nodejs` |

## 4. Git Version Control

| Command | Purpose | Example |
|---------|---------|---------|
| `git init` | Initializes a new Git repository | `git init` |
| `git clone [url]` | Clones a remote repository | `git clone https://github.com/user/repo.git` |
| `git status` | Shows the status of modified files | `git status` |
| `git add .` | Stages all changes in current directory | `git add .` |
| `git add [file]` | Stages a specific file | `git add README.md` |
| `git commit -m "[msg]"` | Commits staged changes with a message | `git commit -m "feat: add login feature"` |
| `git push` | Pushes commits to remote repository | `git push origin main` |
| `git pull` | Pulls and merges changes from remote | `git pull origin main` |
| `git branch` | Lists all branches | `git branch` |
| `git branch [name]` | Creates a new branch | `git branch feature-x` |
| `git checkout [branch]` | Switches to a different branch | `git checkout develop` |
| `git merge [branch]` | Merges specified branch into current branch | `git merge feature-x` |
| `git log` | Shows commit history | `git log --oneline` |
| `git diff` | Shows changes between commits or working tree | `git diff` |
| `git reset [file]` | Unstages a file | `git reset main.py` |
| `git stash` | Temporarily saves uncommitted changes | `git stash` |
| `git stash pop` | Restores stashed changes | `git stash pop` |

## 5. VS Code and WSL Integration

| Command | Purpose | Note |
|---------|---------|------|
| `code .` | Opens current folder in VS Code with WSL remote connection | Most frequently used |
| `code [file]` | Opens a specific file in VS Code | `code main.py` |
| `explorer.exe .` | Opens current WSL folder in Windows File Explorer | Useful for GUI access |
| `wsl --shutdown` | Shuts down all WSL instances | Run from Windows PowerShell/CMD |
| `wsl --list` | Lists all installed WSL distributions | Run from Windows PowerShell/CMD |

## 6. Python Virtual Environment Management

| Command | Purpose | Example |
|---------|---------|---------|
| `python3 -m venv .venv` | Creates a virtual environment named `.venv` | `python3 -m venv .venv` |
| `source .venv/bin/activate` | Activates the virtual environment | `source .venv/bin/activate` |
| `deactivate` | Deactivates the active virtual environment | `deactivate` |
| `pip install [pkg]` | Installs a package in the virtual environment | `pip install pandas` |
| `pip install --upgrade pip` | Updates pip to the latest version | `pip install --upgrade pip` |
| `pip freeze > requirements.txt` | Saves installed packages to a file | `pip freeze > requirements.txt` |
| `pip install -r requirements.txt` | Installs packages from requirements file | `pip install -r requirements.txt` |
| `pip list` | Lists all installed packages | `pip list` |
| `pip uninstall [pkg]` | Uninstalls a package | `pip uninstall numpy` |

## 7. System Information & Process Management

| Command | Purpose | Example |
|---------|---------|---------|
| `uname -a` | Displays system information | `uname -a` |
| `df -h` | Shows disk space usage | `df -h` |
| `du -sh [dir]` | Shows directory size | `du -sh my_project/` |
| `top` | Shows running processes (press `q` to quit) | `top` |
| `htop` | Interactive process viewer (install first) | `htop` |
| `ps aux` | Lists all running processes | `ps aux` |
| `kill [PID]` | Terminates a process by ID | `kill 1234` |
| `killall [name]` | Terminates all processes by name | `killall python3` |
| `chmod +x [file]` | Makes a file executable | `chmod +x script.sh` |
| `chmod 755 [file]` | Sets file permissions (rwxr-xr-x) | `chmod 755 deploy.sh` |

## 8. Network & Connectivity

| Command | Purpose | Example |
|---------|---------|---------|
| `curl [url]` | Transfers data from/to a server | `curl https://api.github.com` |
| `wget [url]` | Downloads files from the web | `wget https://example.com/file.zip` |
| `ping [host]` | Tests network connectivity | `ping google.com` |
| `ifconfig` | Displays network interface information | `ifconfig` |
| `ssh [user]@[host]` | Connects to remote server via SSH | `ssh user@192.168.1.100` |

## 9. Text Processing & Utilities

| Command | Purpose | Example |
|---------|---------|---------|
| `echo [text]` | Prints text to terminal | `echo "Hello World"` |
| `head [file]` | Shows first 10 lines of a file | `head log.txt` |
| `tail [file]` | Shows last 10 lines of a file | `tail -f app.log` |
| `wc [file]` | Counts lines, words, characters | `wc -l file.txt` |
| `sort [file]` | Sorts lines in a file | `sort names.txt` |
| `uniq [file]` | Removes duplicate lines | `sort data.txt | uniq` |

## 10. Compression & Archives

| Command | Purpose | Example |
|---------|---------|---------|
| `tar -czf [name].tar.gz [dir]` | Creates a compressed archive | `tar -czf backup.tar.gz project/` |
| `tar -xzf [file].tar.gz` | Extracts a compressed archive | `tar -xzf backup.tar.gz` |
| `zip -r [name].zip [dir]` | Creates a zip archive | `zip -r project.zip project/` |
| `unzip [file].zip` | Extracts a zip archive | `unzip project.zip` |

## Quick Tips

- Use `Tab` key for auto-completion of commands and file names
- Use `Ctrl + C` to cancel a running command
- Use `Ctrl + R` to search through command history
- Use `!!` to repeat the last command
- Use `sudo !!` to repeat the last command with sudo privileges
- Add `&` at the end of a command to run it in the background: `python3 app.py &`
- Chain commands with `&&` (runs second only if first succeeds): `git add . && git commit -m "update"`
- Use `|` to pipe output from one command to another: `ls -al | grep ".py"`

## Resources

- [Official WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Git Documentation](https://git-scm.com/doc)
- [Ubuntu Command Line Guide](https://ubuntu.com/tutorials/command-line-for-beginners)

---

**Note:** Always use `sudo` carefully and understand what a command does before executing it, especially with `rm -rf`.

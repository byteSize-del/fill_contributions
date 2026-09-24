
# =========================
# CONFIGURATION
import subprocess
from pathlib import Path
import random
from datetime import date, timedelta
# =========================

START_DATE = "2026-01-01"
END_DATE = "2026-09-25"

# 1 = one contribution-producing commit per day.
# Increase this if you want more activity on some days.
COMMITS_PER_DAY = 1

# Set this to your GitHub-associated commit email if needed.
# Leave as None to use your existing Git configuration.
GIT_EMAIL = None

# File that will be changed for every commit.
ACTIVITY_FILE = Path(".github_activity.txt")

# =========================
# HELPERS
# =========================

def run(*args):
    """Run a git command and stop if it fails."""
    subprocess.run(args, check=True)


def git_output(*args):
    return subprocess.check_output(args, text=True).strip()


def make_commit(commit_date: date, number: int):
    """Create one commit with the requested author/committer date."""
    text = (
        f"GitHub activity: {commit_date.isoformat()} "
        f"entry {number}\n"
        f"Random value: {random.randint(100000, 999999)}\n"
    )

    ACTIVITY_FILE.write_text(text, encoding="utf-8")

    timestamp = commit_date.strftime("%Y-%m-%d") + " 12:00:00"

    env = {
        "GIT_AUTHOR_DATE": timestamp,
        "GIT_COMMITTER_DATE": timestamp,
    }

    # Keep the current environment and override only the dates.
    import os
    commit_env = os.environ.copy()
    commit_env.update(env)

    subprocess.run(
        ["git", "add", str(ACTIVITY_FILE)],
        check=True,
        env=commit_env,
    )

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            f"chore: daily activity {commit_date.isoformat()} #{number}",
        ],
        check=True,
        env=commit_env,
    )


def main():
    if not Path(".git").exists():
        raise SystemExit(
            "ERROR: Run this script from inside a Git repository."
        )

    if GIT_EMAIL:
        run("git", "config", "user.email", GIT_EMAIL)

    start = date.fromisoformat(START_DATE)
    end = date.fromisoformat(END_DATE)

    if end < start:
        raise SystemExit("ERROR: END_DATE must be on or after START_DATE.")

    print(f"Creating commits from {start} to {end}...")
    print(f"Commits per day: {COMMITS_PER_DAY}")
    print()

    current = start
    total = 0

    while current <= end:
        for number in range(1, COMMITS_PER_DAY + 1):
            make_commit(current, number)
            total += 1

        current += timedelta(days=1)

    print()
    print(f"Done. Created {total} commits.")
    print()
    print("Next steps:")
    print("  git status")
    print("  git log --oneline -10")
    print("  git push origin main")


if __name__ == "__main__":
    main()

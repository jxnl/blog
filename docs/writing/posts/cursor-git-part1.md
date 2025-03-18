---
description: Learn how to use Git to save your work and avoid the anxiety of powerful agents like Cursor.
date: 2025-03-18
author:
  - jxnl
comments: true
tags:
  - git
  - cursor
  - ai
---

# Version Control for the Vibe Coder: How to Save Your Work (Part 1)

Imagine this: you open Cursor, ask it to build a feature in YOLO-mode, and let it rip. You flip back to Slack, reply to a few messages, check your emails, and return...

It's still running.

What the hell is going on? `.sh` files appear, there's a fresh Makefile, and a mysterious `.gitignore`. Anxiety creeps in. Should you interrupt it? Could you accidentally trash something critical?

Relax—you're not alone. This anxiety is common, especially among developers newer to powerful agents like Cursor’s. Fortunately, Git is here to save the day.

<!-- more -->

### Git—your safety net in coding

Git is a distributed version control system designed to help you manage your code efficiently. Think of Git as the ultimate "save button" for your code, but smarter:

- **Branches**: These let you create isolated environments to experiment safely without affecting your main codebase.
- **Commits**: Each commit is a saved snapshot of your work—like checkpoints in a game.
- **Commit messages**: Short, clear descriptions that explain exactly what's been changed.

Here's how you start working on something new:

```bash
git checkout -b feature/login-page
```

Output:

```
Switched to a new branch 'feature/login-page'
```

Make incremental commits as you progress:

```bash
git add .
git commit -m "Add initial login page layout"
```

Output:

```
[feature/login-page a1b2c3d] Add login page components
 3 files changed, 45 insertions(+)
```

### Git vs. GH-GitHub CLI

- **Git** handles all your local version control tasks (branches, commits, merges, and history).
- **GH (GitHub CLI)** is a complementary tool that simplifies interactions directly with GitHub itself—creating pull requests, managing issues, and handling code reviews.

To set up GH:

```bash
brew install gh
gh auth login
```

Then create a pull request:

```bash
gh pr create --title "Add login feature" --body "Generated automatically by Cursor."
```

Output:

```
Creating pull request...
https://github.com/yourrepo/pull/123
```

### Why Git Matters Even More with Cursor

Cursor's AI agents can run long and make extensive code changes. While this might feel chaotic, using Git makes it powerful:

- **Semantic boundaries:** Commits mark logical checkpoints, not just arbitrary saves.
- **Structured experiments:** Cursor agents generate structured commits that are easier to review and manage.
- **Reversible changes:** Quickly revert any unwanted changes without losing valuable work.

Instead of managing Git manually, instruct Cursor directly:

Example CursorAgent prompt:

> "Cursor, when creating the authentication system, start a new branch called `feature/auth-system`, make incremental commits with descriptive messages, and log every step in a `TODO.md`."

### Automate Best Practices with `.cursor/rules`

You don’t have to type these instructions repeatedly. Instead, you can create a CursorRule—simple markdown files (`.mdc`) stored in `.cursor/rules`—to automate consistent workflows:

**Example CursorRule (`.cursor/rules/git.mdc`):**

```markdown
- For new features, automatically create a Git branch named after the feature (e.g., `feature/<feature-name>`).
- Commit incrementally, with clear, semantic commit messages describing the changes.
- Record progress and next steps clearly in a `TODO.md`.
- When you're done, push your branch to GitHub and create a pull request using `gh pr create --title "<pr-title>" --body "<pr-body>"`.
- Include that this PR was generated automatically by Cursor via `This PR was generated automatically by [Cursor](https://www.cursor.com/)`.
```

Cursor automatically reads and applies these rules when you're working, creating consistent workflows effortlessly.

### What's Next? (Foreshadowing Part 2)

In [Part 2](./cursor-git-part2.md), we’ll dive deeper into advanced techniques, like using stacked PRs, analyzing your project's history with `git log`, and quickly debugging with `git bisect`. These methods combine Git and Cursor into a powerful, anxiety-free coding workflow.


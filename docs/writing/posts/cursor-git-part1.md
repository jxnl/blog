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

# Version Control for the Vibe Coder (Part 1)

Imagine this: you open Cursor, ask it to build a feature in YOLO-mode, and let it rip. You flip back to Slack, reply to a few messages, check your emails, and return...

It's still running.

What the hell is going on? `.sh` files appear, there's a fresh Makefile, and a mysterious `.gitignore`. Anxiety creeps in. Should you interrupt it? Could you accidentally trash something critical?

Relax—you're not alone. This anxiety is common, especially among developers newer to powerful agents like Cursor's. Fortunately, Git is here to save the day.

<!-- more -->

!!! note "Do these vibe coders use git?"

Recently I asked twitter [do these vibe coders use git?](https://x.com/jxnlco/status/1901702040587501873). The top responses were 'no' and 'not really'. I think this is a shame because git is a powerful tool that can help you manage your codebase more effectively.

## 1. Git Fundamentals

### Git vs. GitHub: Understanding the Difference

Before diving deeper, let's clear up a common confusion: Git and GitHub are not the same thing.

- **Git** is a local version control system that runs on your computer

  - Works completely offline
  - Manages your code history
  - Handles branching and merging
  - Free and open-source
  - Can be used without any external services

- **GitHub** is a web platform that hosts Git repositories
  - Provides a place to store your Git repos online
  - Enables collaboration with others
  - Adds features like Issues, Pull Requests, and Actions
  - One of many Git hosting services (others include GitLab, Bitbucket)

Most developers interact with both because:

1. You clone (download) projects from GitHub using Git
2. You make changes locally using Git commands
3. You push those changes back to GitHub for sharing

Here's what this looks like in practice:

```bash
# Clone a project from GitHub
git clone https://github.com/username/project.git

# Make changes locally with Git
git checkout -b feature/new-idea
git add .
git commit -m "feat: add new feature"

# Share changes back to GitHub
git push origin feature/new-idea
```

### Understanding Git's Core Concepts

Let's break down the essential Git concepts you need to know:

1. **Repository (Repo)**

   - A container for your project that tracks all changes
   - Created with `git init` or `git clone`
   - Contains all project history and metadata

2. **Working Directory**

   - Your actual project files on disk
   - Where you make changes before staging them
   - Use `git status` to see what's changed

3. **Staging Area (Index)**

   - A preparation area for your next commit
   - Add files with `git add <file>` or `git add .`
   - Review staged changes with `git diff --staged`

4. **Commits**

   - Permanent snapshots of your staged changes
   - Each has a unique identifier (hash)
   - Include author, date, and message
   - Best practices:

     ```bash
     # Commit with a detailed message
     git commit -m "feat: add user authentication flow

     - Add login form component
     - Implement JWT token handling
     - Set up protected routes"
     ```

### Safety First: Git as Your Safety Net

When working with Git, here are some essential safety practices:

1. **Create Save Points**

   ```bash
   # Before making major changes
   git checkout -b backup/before-changes
   git add .
   git commit -m "chore: backup before changes"
   ```

2. **What to Commit (and What Not to)**

   - **Do Commit:**
     - Source code files
     - Configuration files
     - Documentation
     - Tests
   - **Don't Commit:**
     - API keys or secrets
     - Large binary files
     - Build artifacts
     - Dependencies

3. **Managing `.gitignore**
   ```bash
   # Common patterns for .gitignore
   node_modules/
   __pycache__/
   .env
   *.log
   dist/
   build/
   ```

## 2. Cursor + Git Integration

### Why Git Matters Even More with Cursor

Cursor's AI agents can run long and make extensive code changes. While this might feel chaotic, using Git makes it powerful:

- **Semantic boundaries:** Commits mark logical checkpoints, not just arbitrary saves.
- **Structured experiments:** Cursor agents generate structured commits that are easier to review and manage.
- **Reversible changes:** Quickly revert any unwanted changes without losing valuable work.

### Prompting Cursor to Use Git Effectively

When working with Cursor, you can guide its Git usage through clear prompts. Here are some effective prompting patterns:

1. **Starting New Features**

   ```
   Prompt: "Create a new feature branch called 'feature/user-auth' and implement user authentication. Make atomic commits for each logical change, and include appropriate tests. Use conventional commit messages."
   ```

2. **Incremental Development**

   ```
   Prompt: "Implement the login form component in small, testable steps. After each step:
   1. Stage relevant files
   2. Create a commit with a descriptive message
   3. Show me the git status
   4. Wait for my review before proceeding"
   ```

3. **Code Review Preparation**
   ```
   Prompt: "Review the changes you've made, create a commit with a clear message following conventional commits, and prepare a pull request using `gh pr create --title "<pr-title>" --body "<pr-body>"`" and make sure to include that this PR was generated automatically by Cursor.
   ```

### Handling Cursor's Generated Changes

When Cursor starts generating multiple files:

1. **Interrupt Safely**

   ```
   Prompt: "Please pause and show me the current changes before proceeding further. Let's commit what we have so far."
   ```

2. **Review Changes**

   ```bash
   # See what Cursor has created/modified
   git status
   git diff --staged  # For already staged changes
   ```

3. **Selective Commits**

   ```bash
   # Choose what to keep
   git add -p  # Interactive staging
   git commit -m "feat: add initial structure from cursor"
   ```

4. **Recovery Options**
   ```bash
   # If things go wrong
   git checkout -b recovery/cursor-changes  # Save problematic state
   git checkout main                        # Return to safe state
   git cherry-pick                         # Select good changes
   ```

### Red Flags and Warning Signs

Watch out for these signs that Cursor might be doing too much:

1. **File Volume**

   - Creating more than 5-10 files at once
   - Modifying files across many different directories
   - Generating large amounts of boilerplate

2. **Change Patterns**
   - Modifying core configuration files
   - Creating new package management files
   - Adding unfamiliar dependencies

When you see these signs:

```
Prompt: "Please pause and explain the changes you're planning to make. Let's break this down into smaller, manageable steps that we can review and commit separately."
```

## 3. Advanced Topics

### Advanced Git Commands for Cursor Workflows

Here are some Git commands you'll want Cursor to use:

```bash
# View branch history with graph
git log --oneline --graph --all

# Create and switch to a feature branch
git checkout -b feature/new-component

# Stage specific changes interactively
git add -p

# Temporarily save changes without committing
git stash save "work in progress on login form"

# Apply saved changes later
git stash pop
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

### Teaching Cursor Git Best Practices

Create a `.cursor/rules/git-workflow.mdc` file to guide Cursor's Git usage:

```markdown
# Git Workflow Rules

1. Branch Management:

   - Create feature branches from main/master
   - Use conventional branch naming: feature/, bugfix/, hotfix/
   - Delete branches after merging

2. Commit Guidelines:

   - Write conventional commit messages (feat:, fix:, docs:, etc.)
   - Make atomic commits (one logical change per commit)
   - Include tests with feature commits

3. Code Review Preparation:

   - Squash related commits if requested
   - Write detailed PR descriptions
   - Link related issues/tickets

4. Safety Measures:
   - Stash changes before switching branches
   - Create backup branches for experimental changes
   - Never force push to main/master
```

### Automate Best Practices with `.cursor/rules`

You don't have to type these instructions repeatedly. Instead, you can create a Cursor Rule, a simple markdown files (`.mdc`) stored in `.cursor/rules`—to automate consistent workflows:

**Example CursorRule (`.cursor/rules/git.mdc`):**

```markdown
- For new features, automatically create a Git branch named after the feature (e.g., `feature/<feature-name>`).
- Commit incrementally, with clear, semantic commit messages describing the changes.
- Record progress and next steps clearly in a `TODO.md`.
- When you're done, push your branch to GitHub and create a pull request using `gh pr create --title "<pr-title>" --body "<pr-body>"`.
- Include that this PR was generated automatically by `This PR was generated automatically by [Cursor](https://www.cursor.com/)`.
```

Cursor automatically reads and applies these rules when you're working, creating consistent workflows effortlessly.

### What's Next? (Foreshadowing Part 2)

In [Part 2](./cursor-git-part2.md), we'll dive deeper into advanced techniques, like using stacked PRs, analyzing your project's history with `git log`, and quickly debugging with `git bisect`. These methods combine Git and Cursor into a powerful, anxiety-free coding workflow.

Remember: Git is your safety net, but it works best when you use it proactively. Don't wait until after Cursor has made extensive changes to start thinking about version control.

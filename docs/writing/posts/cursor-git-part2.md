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

# Version Control for the Vibe Coder (Part 2)

In [Part 1](./cursor-git-part1.md), you learned the basics of safely using Git with Cursor agents. Now, let's level up your workflow by diving into advanced Git practices and explicitly instructing Cursor to handle these for you.

<!-- more -->

## Stacked Pull Requests: Building Features Layer by Layer

Stacked pull requests are a powerful workflow for building complex features incrementally. Instead of one massive PR, you create a series of smaller, dependent PRs that build upon each other. Here's how to master this approach:

### Understanding Stacked PRs

Think of stacked PRs like building blocks:

1. Base PR: Core functionality or infrastructure changes
2. Middle PRs: Feature implementations that depend on the base
3. Top PR: Final touches, UI polish, or integration work

### Step-by-Step Workflow

Let's build a complete authentication system using stacked PRs:

```bash
# 1. Create the base branch for core auth infrastructure
git checkout -b feature/auth-base main
# Add basic auth models and middleware
git add .
git commit -m "feat(auth): core authentication infrastructure"
git push -u origin feature/auth-base

# 2. Create the first stack for user management
git checkout -b feature/auth-users feature/auth-base
# Add user registration and management
git add .
git commit -m "feat(auth): user registration and management"
git push -u origin feature/auth-users

# 3. Add authentication UI components
git checkout -b feature/auth-ui feature/auth-users
# Add login/signup forms
git add .
git commit -m "feat(auth): login and signup UI components"
git push -u origin feature/auth-ui

# 4. Final integration and polish
git checkout -b feature/auth-integration feature/auth-ui
# Connect UI with backend, add error handling
git add .
git commit -m "feat(auth): integrate UI with backend"
git push -u origin feature/auth-integration
```

### Managing Dependencies with GitHub CLI

Create PRs in order, clearly showing dependencies:

```bash
# Create base PR
gh pr create \
  --base main \
  --head feature/auth-base \
  --title "feat(auth): Core Authentication Infrastructure" \
  --body "Base PR for authentication system. No dependencies."

# Create user management PR
gh pr create \
  --base feature/auth-base \
  --head feature/auth-users \
  --title "feat(auth): User Management" \
  --body "Depends on #123 (Core Authentication Infrastructure)"

# Create UI PR
gh pr create \
  --base feature/auth-users \
  --head feature/auth-ui \
  --title "feat(auth): Authentication UI" \
  --body "Depends on #124 (User Management)"

# Create integration PR
gh pr create \
  --base feature/auth-ui \
  --head feature/auth-integration \
  --title "feat(auth): Final Integration" \
  --body "Depends on #125 (Authentication UI)"
```

### Best Practices for Stacked PRs

1. **Keep Each Layer Focused**

   - Each PR should have a single responsibility
   - Make changes easy to review and understand
   - Include relevant tests for each layer

2. **Clear Documentation**

   - Maintain a `STACK.md` file describing the PR stack:

   ```markdown
   # Authentication Feature Stack

   1. Core Infrastructure (#123)
      - Basic auth middleware
      - Token management
   2. User Management (#124)
      - Registration flow
      - User CRUD operations
   3. UI Components (#125)
      - Login form
      - Registration form
   4. Integration (#126)
      - Connect UI to backend
      - Error handling
   ```

3. **Handle Updates Efficiently**
   When you need to update a lower layer:

   ```bash
   # Update base layer
   git checkout feature/auth-base
   # Make changes
   git commit -m "fix(auth): improve token validation"
   git push

   # Rebase each dependent branch
   git checkout feature/auth-users
   git rebase feature/auth-base
   git push --force-with-lease

   # Continue for each stack
   git checkout feature/auth-ui
   git rebase feature/auth-users
   git push --force-with-lease
   ```

## Using GitHub's Auto-Merge

Enable auto-merge to automatically merge PRs once dependencies are resolved:

```bash
gh pr merge feature/auth-base --auto --squash
gh pr merge feature/auth-users --auto --squash
gh pr merge feature/auth-ui --auto --squash
gh pr merge feature/auth-integration --auto --squash
```

### Troubleshooting Stacked PRs

1. **Handling Conflicts**

   ```bash
   # If a lower stack changes
   git checkout feature/auth-users
   git rebase feature/auth-base
   # Fix conflicts
   git add .
   git rebase --continue
   git push --force-with-lease
   ```

2. **Dropping a Middle Stack**
   If you need to remove a middle PR:
   ```bash
   # Rebase onto grandparent
   git checkout feature/auth-ui
   git rebase --onto feature/auth-base feature/auth-users
   git push --force-with-lease
   ```

This structured approach to feature development keeps your changes organized, reviewable, and maintainable.

## Using `git log`: Seeing Your Project's Evolution

Instruct Cursor to clearly mark incremental progress so you can use `git log` to quickly see changes:

```bash
git log --oneline --graph --decorate
```

Sample Output:

```
* 4f5e6d7 (feature/ui-auth) Add authentication UI components
* 2a3b4c5 (feature/base-auth) Set up backend authentication
* 1a2b3c4 Initial commit for auth setup
```

### Precise Differences with `git diff`

Easily see exactly what changed between branches or commits:

```bash
git diff feature/base-auth..feature/auth-ui
```

Output:

```diff
+ import LoginComponent from './LoginComponent';
+ export default function AuthPage() {
+   return <LoginComponent />;
```

Instructing Cursor explicitly helps keep these diffs clean and meaningful.

## Mastering `git bisect`: Your Time Machine Debugger

When a bug appears in your codebase and you're not sure which commit introduced it, `git bisect` becomes your best friend. It performs a binary search through your commit history to find the exact commit that introduced the problem. Here's how to use it effectively:

### Basic Workflow

1. Start the bisect process:

```bash
git bisect start
git bisect bad  # Mark current commit as having the bug
git bisect good v1.0  # Mark a known good commit/tag
```

2. Git will automatically checkout a commit halfway between good and bad. Test your code and tell Git the result:

```bash
# If the bug exists in this commit
git bisect bad

# If the bug doesn't exist in this commit
git bisect good
```

3. Repeat until Git identifies the problematic commit.

### Real-World Example

Let's say your tests are failing and you need to find why. Here's a practical workflow:

```bash
# Start bisecting
git bisect start

# Current state is broken
git bisect bad HEAD

# Last known good state (e.g., 2 weeks ago)
git bisect good HEAD~100

# Git checks out a commit - run your tests
npm test

# Mark the result
git bisect good  # or bad based on test results

# ... repeat until found ...

# Git will eventually show something like:
# b1234567 is the first bad commit
# Author: Developer Name
# Date: Thu Mar 14 15:31:22 2024
#
#     feat: add new authentication flow
```

### Automating the Process

For even more efficiency, you can automate the bisect process with a test script:

```bash
# Create a test script (test.sh)
#!/bin/bash
npm test
exit $?

# Run automated bisect
git bisect start
git bisect bad HEAD
git bisect good HEAD~100
git bisect run ./test.sh
```

### Best Practices

1. **Choose Good Boundaries**: Pick a recent "bad" commit and an older "good" commit that you're confident about.
2. **Use Meaningful Tests**: Ensure your test reliably reproduces the issue.
3. **Keep Notes**: Document what you find - the problematic commit might reveal patterns.
4. **Clean Up**: Always run `git bisect reset` when done to return to your original branch.

### Advanced Usage

You can get even more sophisticated with bisect:

```bash
# View the remaining commits to test
git bisect visualize

# Save bisect log for later analysis
git bisect log > bisect_log.txt

# Replay a previous bisect session
git bisect replay bisect_log.txt

# Skip a commit that can't be tested
git bisect skip
```

### When to Use Bisect

`git bisect` is particularly valuable when:

- A bug appears but you're not sure when it was introduced
- Tests suddenly fail after many commits
- Performance degradation occurs somewhere in history
- Behavior changes unexpectedly between releases

Remember to reset when you're done:

```bash
git bisect reset  # Returns to your original branch
```

This systematic approach turns what could be hours of manual debugging into a structured, efficient process.

### Explicitly Automate Workflows with `.cursor/rules`

Add rules to `.cursor/rules` to instruct Cursor clearly and repeatedly:

**Example CursorRule (`.cursor/rules/git.mdc`):**

```markdown
---
description: Git management by Cursor
---

- When creating new features, automatically branch (`feature/<feature-name>`).
- Commit incrementally with descriptive semantic messages.
- Document progress, branches, and commit structures clearly in a `TODO.md` file.
- Use GH to open and manage pull requests, specifying dependencies in stacked PRs.
```

### Leveraging GH-GitHub CLI for PR Management

Instruct Cursor explicitly to use GH to handle GitHub tasks directly from your terminal, keeping your workflow smooth:

- Create pull requests:

```bash
gh pr create --title "Cursor-generated auth feature" --body "Structured and documented by Cursor."
```

- View and manage PR comments:

```bash
gh pr view --comments
```

Remember to explicitly authenticate with GH once:

```bash
brew install gh
gh auth login
```

### Making the Most of CursorRules

Instruct Cursor through `.cursor/rules` to consistently automate advanced Git workflows:

```markdown
---
description: Structured Git workflow automation
globs: ["**/*"]
---

- Automatically create branches for new tasks.
- Commit frequently with semantic messages.
- Document each step clearly in `TODO.md`.
- Use GH CLI for seamless GitHub integration (creating PRs, managing comments).
```

### The Secret to Git Success: Keep It Simple, Let Cursor Handle the Complex

Here's the thing about all these advanced Git techniques - you don't need to master them yourself. The real key to success with Git is much simpler:

1. **Make Small, Frequent Commits**

   - Save your work often
   - Each commit should do one thing
   - Write clear commit messages
   - Don't worry about being perfect

2. **Let Cursor Handle the Rest**
   Instead of memorizing complex commands, just tell Cursor what you want:

   > "Create a stack of PRs for this feature using gh pr create"
   > "Find which commit broke the tests using git bisect"
   > "Rebase these changes onto main using git rebase"

3. **Focus on Your Code**
   - You don't need to be a Git expert
   - Cursor knows all the commands we covered
   - Your job is to prompt well and make sure you or cursor are committing often
   - Let Cursor handle the complex workflows knowing that you can always revert to the last commit if something goes wrong and that your job is to orchestrate and be aware of the overall plan

Remember: The most important Git skill is making regular, small commits. Everything else - bisecting, stacked PRs, complex rebases - these are just tools that Cursor can handle for you. Start with good commit habits, and let Cursor be your Git expert.

### Mastering Your Workflow

The power of Git with Cursor isn't just knowing the commands—it's about explicitly telling Cursor to manage these tasks. By clearly instructing your agents or using structured CursorRules, you turn chaotic coding into organized productivity.

Now, go code confidently—let Cursor handle the Git.

# AGENTS.md

Repo facts I discovered:

- Content lives in `docs/`.
- Blog posts live in `docs/writing/posts/`.
- New posts need frontmatter: `authors`, `categories`, `comments`, `date`, `description`, `draft`, `slug`, `tags`.
- Use `<!-- more -->` for the excerpt break.
- When editing dictated draft content, preserve my voice as much as possible. Only make light punctuation and grammar fixes unless I explicitly ask for a rewrite.
- New external links must go through `scripts/shortlinks.py` with `uv run python ... --blog-tag <slug>`.
- Local build/preview: `uv run mkdocs serve` and `uv run mkdocs build`.

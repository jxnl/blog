# AGENTS.md

## Commands

- `uv sync` - Install dependencies (use uv, not pip)
- `mkdocs serve` - Development server with live reload
- `mkdocs build` or `./build_mkdocs.sh` - Build static site
- `pre-commit run --all-files` - Run quality checks
- `python check_links.py` - Validate all markdown links
- `python generate_sitemap.py` - Generate SEO sitemap
- `uv run python scripts/shortlinks.py "URL" --blog-tag "slug"` - Create Dub shortlinks

## Architecture

MkDocs Material blog with Python utilities. Content in `docs/writing/posts/`. Config: `mkdocs.yml`, deps: `pyproject.toml`. Pre-commit hooks validate formatting, links, and <!-- more --> tags.

## Code Style

- Blog posts require YAML frontmatter (authors, categories, date, description, draft, slug, tags)
- All posts must have `<!-- more -->` tag after excerpt
- Use kebab-case filenames
- Add external links via shortlinks CLI with --blog-tag parameter
- Cross-link related posts naturally using sitemap.yaml for reference
- Images in `docs/writing/posts/img/`

## Writing Guidelines

- Direct, actionable titles ("Four Levels Every RAG System Should Implement")
- Core insights upfront, avoid dramatic subheadings
- Include consulting attribution and series positioning
- Use descriptive link text, weave research naturally
- Maintain 9th-grade reading level, concise professional tone

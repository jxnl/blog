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

## Finding Blog Posts

Blog posts are located in `docs/writing/posts/`. To find a specific post:

1. **By filename**: Posts use kebab-case filenames (e.g., `rag-only-6-evals.md` for "There Are Only 6 RAG Evals")
2. **By slug**: Each post has a `slug` field in frontmatter that matches the URL path
3. **By title search**: Use semantic search or grep to find posts by title keywords
4. **By category**: Check `docs/writing/index.md` which organizes posts by topic
5. **By sitemap**: `sitemap.yaml` contains metadata for all posts including titles, slugs, and summaries

Common post patterns:

- RAG posts: `rag-*.md` (e.g., `rag-only-6-evals.md`, `rag-levels-of-rag.md`)
- Context Engineering: `context-engineering-*.md` (e.g., `context-engineering-tool-response.md`)
- Consulting: `consulting-*.md` (e.g., `consulting-everything-i-know.md`)
- Personal: `advice.md`, `hands-part-1.md`, `learning.md`

When linking to posts, use relative paths like `./writing/posts/filename.md` or `../posts/filename.md` depending on context.

## Writing Guidelines

- Direct, actionable titles ("Four Levels Every RAG System Should Implement")
- Core insights upfront, avoid dramatic subheadings
- Include consulting attribution and series positioning
- Use descriptive link text, weave research naturally
- Maintain 9th-grade reading level, concise professional tone

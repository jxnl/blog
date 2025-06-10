# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is Jason Liu's personal blog and consulting website built with MkDocs Material. The site features AI/ML technical content, consulting services, RAG education courses, and personal writing.

## Build Commands

```bash
# Install dependencies (using uv as preferred)
uv pip install -r requirements-doc.txt

# Development server with live reload
mkdocs serve

# Build static site
mkdocs build
# or
./build_mkdocs.sh

# Utility scripts
python check_links.py          # Verify all links in markdown files
python generate_sitemap.py     # Generate SEO sitemap with AI summaries
python generate_desc.py        # Add AI-generated descriptions to posts
```

## Architecture

The site uses MkDocs with Material theme for static site generation:

- **Content**: All markdown files in `docs/` directory
- **Blog posts**: Located in `docs/writing/posts/`
- **Configuration**: `mkdocs.yml` defines site structure, theme, and plugins
- **Automation**: Python scripts for SEO optimization and link checking
- **Styling**: Custom CSS in `docs/stylesheets/`, JS in `docs/javascripts/`

Key architectural decisions:

- Static site generation for performance and hosting simplicity
- Material Design for modern, responsive UI
- Blog plugin for chronological content organization
- AI-powered tools for SEO metadata generation
- YouTube color scheme for consistent branding

## Adding Content

When adding new blog posts:

1. Create markdown file in `docs/writing/posts/`
2. Include frontmatter with date, authors, description, categories, and draft status
3. Run `python generate_desc.py` to generate AI descriptions if needed
4. Links should be verified with `python check_links.py`

## Important Notes

- The site is live at https://jxnl.co/
- Git repository: https://github.com/jxnl/blog/
- Uses YouTube color scheme (dark theme)
- Google Analytics enabled (G-686PKP2V2V)
- RSS feed available for blog posts
- MathJax enabled for mathematical notation

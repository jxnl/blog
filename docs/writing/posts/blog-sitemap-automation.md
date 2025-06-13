---
authors:
  - jxnl
categories:
  - Writing and Communication
  - Software Engineering
comments: true
date: 2025-01-06
description: How I automated my blog's sitemap generation with AI, saving hours and improving SEO with every commit
draft: false
slug: blog-sitemap-automation
tags:
  - SEO
  - Automation
  - AI
  - Blog Infrastructure
  - Python
---

# How I Accidentally Built the World's Most Over-Engineered Blog Sitemap

Here's a confession: I spent more time automating my blog's sitemap generation than I've spent writing some of my actual blog posts. But hear me out – it's actually been worth it.

<!-- more -->

## The Problem: Sitemaps Are Boring But Important

If you run a blog, you know sitemaps are crucial for SEO. They tell search engines what content you have and help them understand your site structure. But maintaining them? Pure tedium.

Every time I wrote a new post or updated existing content, I'd need to:

- Update the sitemap manually
- Write a summary for SEO
- Make sure I didn't break anything
- Remember to actually do it (spoiler: I usually forgot)

After forgetting to update my sitemap for the 47th time, I decided to solve this problem once and for all. This is the same philosophy I apply to [my consulting work](./consulting-everything-i-know.md) – automate the boring stuff so you can focus on what matters.

## The Solution: Make AI Do the Boring Stuff

I built a system that automatically generates and updates my sitemap every time I commit changes to my blog. Here's the beautiful part: it only regenerates summaries for files that actually changed.

### How It Works

1. **Pre-commit Hook**: Every time I commit, a Python script runs automatically
2. **Content Hashing**: It generates MD5 hashes of each markdown file to detect what changed
3. **Smart Caching**: Only files with changed content get new summaries
4. **AI Summary Generation**: GPT-4 generates SEO-optimized summaries for changed files
5. **Automatic Commit**: The updated sitemap gets included in my commit

Here's what this looks like in practice:

```bash
$ git commit -m "Add internal links for SEO"
prettier (markdown)......................................................Passed
Update sitemap...........................................................Running
Generated new summary for: writing/posts/consulting-start.md
Generated new summary for: writing/posts/rag-improving-rag.md
Processing files... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Sitemap generated successfully!
📊 Summary: 89 cached, 7 newly generated
💾 Saved to sitemap.yaml
```

## The Implementation

The magic happens in `generate_sitemap.py`. Here's the core logic:

```python
def should_regenerate_summary(file_path, file_hash, sitemap_data):
    """Check if we should regenerate the summary for a file"""
    relative_path = os.path.relpath(file_path, root_dir)

    # If file not in sitemap, generate summary
    if relative_path not in sitemap_data:
        return True

    # If hash changed, regenerate
    existing_hash = sitemap_data[relative_path].get('hash')
    if existing_hash != file_hash:
        return True

    # If no summary exists, generate
    if not sitemap_data[relative_path].get('summary'):
        return True

    return False
```

The AI prompt for generating summaries is carefully crafted to produce SEO-friendly content:

```python
prompt = f"""Generate a comprehensive summary for SEO optimization.
Include:
- Main topics and themes
- Key insights and takeaways
- Target audience
- Important keywords

Content: {content[:4000]}"""
```

## The Results

Since implementing this system (part of my broader [content creation strategy](./writing-style-guide.md)):

- **Zero manual sitemap updates**: It just happens automatically
- **Better SEO**: AI-generated summaries are consistently high quality
- **Cost efficient**: Only regenerates what changed (typically 5-10 files per commit)
- **Always up-to-date**: Impossible to forget since it's automatic

In my last commit adding internal links across posts, it processed 96 files in seconds, regenerating summaries for only the 7 that changed. The other 89 used cached summaries.

## The Over-Engineering Part

Yes, I could have just used a static sitemap generator. Yes, I could have written summaries manually. But where's the fun in that?

This system:

- Uses GPT-4 to write better summaries than I would
- Saves me 10-15 minutes per blog post
- Never forgets to update
- Makes me feel like a automation wizard

## Setup for Your Own Blog

Want to implement something similar? Here's the configuration (and if you need help setting this up, check out my [consulting services](./services.md)):

1. Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: update-sitemap
      name: Update sitemap
      entry: python generate_sitemap.py
      language: python
      files: \.md$
      pass_filenames: false
      additional_dependencies: [openai, pyyaml, python-frontmatter]
```

2. Create `generate_sitemap.py` with the logic above
3. Set your OpenAI API key: `export OPENAI_API_KEY=your-key`
4. Commit and watch the magic happen

## Was It Worth It?

Absolutely. I've saved hours of manual work, my SEO has improved, and I have one less thing to think about when publishing content.

Plus, there's something deeply satisfying about watching your blog maintain itself. It's like having a very specialized, very nerdy robot assistant. This automation mindset is similar to building [data flywheels](./data-flywheel.md) – set it up once, benefit forever.

## The Real Lesson

The best automation is the kind you set up once and forget about. Every time I commit a blog post and see that sitemap update automatically, I feel a small surge of joy.

Is it over-engineered? Definitely.
Is it unnecessary? Probably.
Do I love it? Absolutely.

Sometimes the best solutions are the ones that make you smile every time they run. It's the same principle I discuss in [systematically improving RAG](./rag-improving-rag.md) – continuous, automated improvement beats sporadic manual effort every time.

---

_P.S. This blog post's summary was, of course, generated automatically by the very system it describes. Meta enough for you?_

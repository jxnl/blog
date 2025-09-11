---
authors:
  - jxnl
categories:
  - Writing and Communication
  - Software Engineering
comments: true
date: 2025-01-06
description: How I used AI agents to analyze 100+ blog posts and add 50+ strategic cross-links in just 30 minutes
draft: false
slug: ai-agents-cross-linking
tags:
  - SEO
  - AI
  - Content Strategy
  - Cross-linking
  - GPT-4
---

# I Used AI Agents to Add 50+ Cross-Links to My Blog (And You Can Too)

I just had an AI agent read through 100+ of my blog posts and tell me exactly where to add internal links. In 30 minutes, it found connections I'd missed for years. Here's how I did it.

<!-- more -->

## The Problem: Manual Cross-Linking Doesn't Scale

I have 100+ blog posts. Each one could potentially link to 5-10 others. That's 500-1000 potential cross-links.

Doing this manually means:

- Reading every post (again)
- Remembering what each one covers
- Finding natural places to add links
- Not making it feel forced

Or... I could have an AI agent do it in 30 minutes.

## The Solution: AI Agent as Content Strategist

Here's my exact process:

### Step 1: Generate AI Summaries

I have a Python script that runs GPT-4 on every blog post to create summaries. But the summaries aren't just for SEO – they're a map of my content.

### Step 2: Feed Everything to an AI Agent

I gave Claude this prompt:

```
Here are summaries of all my blog posts.
Analyze them and tell me:
1. Which posts reference similar concepts
2. Where I mention a topic briefly that I cover in detail elsewhere
3. Natural places to add cross-links that would help readers
```

### Step 3: Get Specific Recommendations

The AI agent returned specific, actionable suggestions:

- "In consulting-start.md line 57, you mention pricing – link to consulting-pricing.md"
- "Your RAG posts form a learning path – connect them sequentially"
- "You reference hand injuries in 3 posts without linking to the full story"

Here's actual output from the AI agent:

```
File: consulting-start.md
Line ~89: "I learned this the hard way when I undercharged"
Suggestion: Link to money-negative-margin.md (discusses pricing mistakes)

File: rag-improving-rag.md
Line ~180: "I also wrote a 6 week email course on RAG"
Suggestion: Link to rag-course-breakdown.md (detailed course description)

File: ai-engineering-communication.md
Line ~110: "centered around RAG"
Suggestion: Link to rag-what-is-rag.md (explains RAG fundamentals)
```

50+ suggestions like this. All specific. All actionable.

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

The beauty is in the two-step process:

**Step 1: Summarize (Automated)**

```python
# This runs on every commit via pre-commit hook
for post in blog_posts:
    if content_changed(post):
        summary = gpt4_summarize(post)
        save_to_sitemap(summary)
```

**Step 2: Find Links (AI Agent)**

```python
# This is where the magic happens
all_summaries = load_sitemap()
links = ai_agent_find_connections(all_summaries)
for link in links:
    print(f"{link.file}:{link.line} -> {link.target}")
```

## The Results: 30 Minutes = 50+ Quality Cross-Links

In one session, the AI agent found:

- **15 links** between consulting posts (creating a complete guide)
- **12 links** in the RAG series (forming a learning path)
- **8 links** from personal stories to relevant technical content
- **20+ links** where I mentioned concepts briefly that I explain in detail elsewhere

Each suggestion included:

- Exact file and line number
- The text that should be linked
- Which post to link to
- Why the link adds value

## Why AI Agents Are Perfect for This

AI agents excel at this because they can:

- **Hold 100+ posts in context** simultaneously
- **Understand semantic relationships** between different topics
- **Find non-obvious connections** (like my hand injury story relating to why I started consulting)
- **Give specific line-by-line suggestions** instead of vague advice
- **Work at superhuman speed** (analyzing 100 posts in minutes)

## The Implementation: Two Scripts, Endless Value

**Script 1: generate_sitemap.py** (runs automatically)

- Generates AI summaries for changed blog posts
- Maintains a cache to avoid regenerating everything
- Runs on pre-commit hook
- Costs: ~$0.01 per post

**Script 2: AI Agent Analysis** (run manually)

- Feed all summaries to Claude/GPT-4
- Ask for specific cross-linking opportunities
- Get line-by-line suggestions
- Implement the links

Total time: 30 minutes. Total cost: ~$2.

## This Changes Everything

Think about what this means:

- **Every blogger** can have perfect internal linking
- **Every content site** can maximize reader engagement
- **Every knowledge base** can be fully interconnected

And it takes 30 minutes.

This is what I mean when I talk about [AI agents changing how we work](./ai-truths.md). Not replacing us – augmenting us to do things we could never do manually.

## Your Turn: Try This Now

1. Export your blog posts (or any content)
2. Feed them to Claude or GPT-4
3. Ask: "Find opportunities for cross-links between these posts"
4. Watch it find connections you missed

Or if you want to go full automation like me:

1. Set up automated summaries with GPT-4
2. Use those summaries for AI agent analysis
3. Never miss a cross-linking opportunity again

The future isn't AI writing our content. It's AI making our existing content work harder.

---

_P.S. An AI agent helped me write this post by analyzing my commit history and identifying what made this approach unique. It suggested I focus on the agent aspect rather than the automation. Meta? Absolutely._

---

**Want help building systems like this?** I know AI automation can feel overwhelming—I try to share what works from my consulting, but sometimes it helps to have someone walk through it with you:

[Free 6-Week RAG Email Course](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }
[Maven RAG Playbook — 20% off with code EBOOK](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK){ .md-button .md-button--secondary }

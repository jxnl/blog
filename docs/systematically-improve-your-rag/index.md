---
title: Workshops
description: Hands-on workshops for building self-improving RAG systems
---

# Workshops

These workshops walk you through building RAG systems that actually get better over time. If you're tired of deploying a RAG system only to watch it stagnate while users complain, this is for you.

!!! success "🎓 Get the Complete Course - 20% Off"
    This content is from the [Systematically Improving RAG Applications](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK) course on Maven.
    
    **Readers can enroll for 20% off with code: `EBOOK`**
    
    Join 500+ engineers who've transformed their RAG systems from demos to production-ready applications.
    
    [Enroll in the RAG Playbook Course - 20% Off](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK){ .md-button .md-button--primary }

## What's Covered

### [Introduction: Beyond Implementation to Improvement](chapter0.md)

Why most RAG systems fail after deployment and how to build ones that improve instead. Covers thinking about RAG as a recommendation engine, setting up feedback loops, and moving from random tweaks to data-driven improvements.

### [Chapter 1: Getting Started with Synthetic Data](chapter1.md)

How to evaluate your RAG system before you have real users. Learn to avoid common mistakes (vague metrics, generic solutions), generate synthetic evaluation data, and set up continuous evaluation pipelines. Real examples of improving recall from 50% to 90%.

### [Chapter 2: From Evaluation to Better Models](chapter2.md)

Turn your evaluation data into actual improvements. Covers when generic embeddings fail, how to create training data from evaluations, fine-tuning strategies, and cost-effective alternatives like re-rankers.

### Chapter 3: Getting Users to Actually Give Feedback

#### [Chapter 3.1: Feedback Collection That Works](chapter3-1.md)

How to get feedback rates above 30% (most systems get <1%). Includes specific copy that works, UI patterns, mining implicit signals, and Slack integration examples.

#### [Chapter 3.2: Making RAG Feel Fast](chapter3-2.md)

Streaming techniques that make your system feel faster and increase feedback by 30-40%. Covers Server-Sent Events, skeleton screens, and platform-specific tricks for Slack and web.

#### [Chapter 3.3: Small Changes, Big Impact](chapter3-3.md)

Practical improvements that users love: interactive citations, chain of thought (8-15% accuracy boost), validation patterns (80% error reduction), and knowing when to say no.

### Chapter 4: Learning from User Behavior

#### [Chapter 4.1: Finding Patterns in User Data](chapter4-1.md)

How to turn vague feedback into actionable improvements. Learn the difference between topics (what users ask about) and capabilities (what they want done), plus practical clustering techniques.

#### [Chapter 4.2: Deciding What to Build Next](chapter4-2.md)

Practical prioritization using 2x2 frameworks, failure analysis, and user behavior. Real examples of how query analysis changes what you build.

### Chapter 5: Specialized Retrieval That Actually Works

#### [Chapter 5.1: When One Size Doesn't Fit All](chapter5-1.md)

Why generic RAG hits limits and how specialized retrievers solve it. Covers metadata extraction vs. synthetic text strategies and how to measure two-level systems.

#### [Chapter 5.2: Search Beyond Text](chapter5-2.md)

Practical implementations for documents, images, tables, and SQL. Real performance numbers: 40% better image retrieval, 85% table accuracy. Includes RAPTOR and other advanced techniques.

### Chapter 6: Making It All Work Together

#### [Chapter 6.1: Query Routing Basics](chapter6-1.md)

How to build systems where specialized components work together. Covers team structure, the API mindset, and the math behind routing performance.

#### [Chapter 6.2: Building the Router](chapter6-2.md)

Practical implementation of routing layers. Includes Pydantic interfaces, structured outputs, dynamic examples, and when to use multi-agent vs. single-agent designs.

#### [Chapter 6.3: Measuring and Improving Routers](chapter6-3.md)

How to know if your router works and make it better. Covers metrics, dual-mode UIs, diagnostic frameworks, and setting up improvement loops.

## How These Workshops Work

Each chapter includes practical exercises you can apply to your own RAG system. They build on each other, so start from the beginning unless you know what you're doing.

The progression:

1. **Getting Started** (Intro & Ch 1): Think like a product, set up evaluation
2. **Making It Better** (Ch 2): Turn evaluation into improvements
3. **User Experience** (Ch 3): Get feedback, feel fast, don't break
4. **Learn from Users** (Ch 4): Find patterns, pick what to build
5. **Go Deep** (Ch 5): Build specialized tools that excel
6. **Tie It Together** (Ch 6): Make everything work as one system

## Prerequisites

You should know what RAG is and have at least played with it. If you're totally new, start with the [Introduction](chapter0.md).

## What You'll Have When Done

A RAG system that:

- Gets better from user feedback
- Routes queries to the right specialized tools
- Feels fast and responsive
- Makes improvement decisions based on data
- Doesn't break in weird ways
- Works for teams, not just demos


## Stay Updated

Get access to our free 6-day email course on RAG improvement

[Subscribe for updates](https://himprovingrag.com){ .md-button }

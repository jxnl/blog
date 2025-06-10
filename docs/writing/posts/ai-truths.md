---
description: A collection of hard truths from the AI trenches.
slug: ai-from-the-trenches
authors:
  - jxnl
categories:
  - AI
comments: true
date: 2025-03-05
---

# Hard Truths From the AI Trenches

I never planned to become a consultant. But somewhere between building machine learning systems and growing my Twitter following, companies started sliding into my DMs with the same message: "Help, our AI isn't working."

So I started charging to join their stand-ups. Sometimes I didn't even code. I just asked uncomfortable questions.

Here's what I've learned watching companies burn millions on AI.

<!-- more -->

## Your AI problems aren't AI problems

The head of AI at a major company once showed me their evaluation framework. They had 23 evals. One of them tested if their AI could "talk like a pirate."

I shit you not.

Meanwhile, 75% of their users were just trying to make their AI read Excel spreadsheets. But they had three engineers focused on a fancy document integration that less than 10% of users touched.

This is the pattern everywhere I go. Companies obsess over sophisticated AI capabilities while ignoring what users actually do with their product.

The truth? Your AI problem is almost always a data problem. Or a process problem. Or a people problem. But rarely is it actually an AI problem.

## Stop waiting for the model to save you

"When GPT-5 comes out, all our problems will be solved."

I've heard this exact sentiment in different words from CTOs who should know better. It's magical thinking, and it's everywhere.

Here's a hard truth: capabilities are monotonically increasing. Each new model will be better than the last. But if your recall sucks now, ChatGPT 47.0 isn't going to save you.

Fix your retrieval. Fix your data pipeline. Fix your evaluation process. These are things you control today.

When I tell clients this, they often look disappointed. They wanted me to tweak some prompt magic or recommend a fancy new model. Instead, I'm telling them to do the unsexy work of:

- Building better test sets
- Implementing proper feedback loops
- Actually looking at their data

One client went from 27% recall to 85% in four hours once they stopped praying to the model gods and started making targeted improvements to their data preprocessing. It wasn't glamorous, but it worked.

## Measure what matters (and it's not what you think)

Most AI teams are measuring the wrong things. They obsess over model perplexity or ROUGE scores while their business burns.

At a sales tech company, engineers spent weeks trying to perfect their call transcript summarization accuracy. Meanwhile, sales managers didn't care about perfect summaries — they wanted to know which prospects had buying objections.

Classification first, extraction second. Always.

When we shifted from "how accurately can we summarize this call?" to "can we identify sales objections with 95% recall?", suddenly the business value was obvious. The sales team could follow up on objections, coach their reps better, and close more deals.

The best metric isn't technical. It's: "Does this solve a real problem someone will pay for?"

## Experimentation speed is your only moat

Ask most AI teams how long it takes to run an experiment, and you'll get embarrassed silence. Four days? A week? "Well, we have to coordinate with three teams and..."

The companies winning with AI can run 10 experiments before lunch.

One client went from spending weeks fine-tuning prompts to implementing a system where they could:

1. Sample real-time traffic
2. Test multiple approaches
3. Compare metrics
4. Deploy winners

All in the same day.

Your ability to learn fast is everything. Build for learning velocity above all else.

As I tell my clients: how do you get better at jiu-jitsu? Mat time. More experiments, more data, more learning.

## Testimonials > Metrics

Nobody cares that your RAG system has 78.9% recall. They care that FancyCorp saved $2M using your product.

I was advising a construction tech company where we dramatically improved their document retrieval. But the testimonial that closed their next funding round wasn't "They improved our retrieval precision by 40%."

It was: "Their system automatically identifies contractors who haven't signed liability waivers 4 days before they're scheduled on site. This prevented $80,000 in construction delays last month alone."

When marketing your AI, translate your metrics into outcomes people actually care about.

## Find the hidden value patterns

The highest-leverage consulting I do isn't technical at all. It's identifying where the actual value is.

At a document management company, we discovered that 60% of questions weren't about document content at all. Users were asking: "Who last modified this document?" They needed contact information to verify decisions.

So we modified every text chunk to include metadata about creation date, modification date, and owner contact info. Suddenly, the most valuable feature wasn't fancy RAG—it was helping people find who to call.

At another client, we found that what users really wanted wasn't answering questions about blueprints. They wanted to count rooms. We could have spent months improving general QA, or we could build a specialized counter. We built the counter.

Your users are telling you what they value. But you have to listen.

## Network effects are everything (and AI doesn't have them yet)

Here's the biggest challenge facing AI companies: getting more customers doesn't make your product better. It just creates more opportunities to disappoint people.

Netflix gets better when more people use it. Spotify gets better. Doordash gets better.

But most AI apps? Adding users just adds load without improving quality.

What if having 1,000 users made your recall go up by 20%? You'd have a flywheel. Right now, most companies are just pushing a boulder.

This is why few AI companies have achieved escape velocity. The ones that do figure out how to create virtuous loops where more usage makes their systems smarter in ways users can feel.

## The 'Oh shit' moment

You know you've found product-market fit when user growth starts hurting. One client went viral with their AI assistant, hitting 400,000 MRR almost overnight.

The next week? 340,000. Week after? 280,000.

Why? Their product wasn't ready for scale. They blew their first impression with thousands of users who will never come back.

AI products often focus so much on capabilities that they forget fundamentals like stability, speed, and reliability. The most elegant RAG system means nothing if it takes 10 seconds to respond or breaks under load.

## Most consultants solve the wrong problem (including me sometimes)

I've fired clients when I realized I couldn't help them. Not because their AI challenges were too hard, but because their organizational challenges were too deep.

When a client books meetings with me at 5am while I'm about to board a flight, that's not an AI problem. When a team is rebuilding the same database integration for the third time, that's not an AI problem.

Sometimes the highest-value thing I can do is tell clients: "Your issue isn't that your AI is bad. It's that your company's processes are broken."

And sometimes the best consulting is just giving smart people permission to trust their instincts. Like when an engineer tells me: "The only way forward is to try random permutations of these parameters to see what works," and I say, "Yes, that's called hyperparameter optimization, and it's exactly what you should be doing."

## Lessons learned

The pattern I see across every client is this: companies spend too much time on capabilities and not enough on connections. They build amazing AI features without connecting them to business outcomes.

The best AI isn't the most impressive in a demo. It's the one that solves a real problem customers will pay for.

When a client asks how they're doing, I don't start with technical metrics. I ask: "Are pilots converting to paid? Are usage numbers climbing? Are customers telling their friends?"

Those are the only metrics that matter.

Remember:

- Start with the business outcome, work backwards
- Measure what matters (hint: it's rarely model performance)
- Optimize for learning velocity
- Connect your AI directly to problems people will pay to solve

And if all else fails, remember what I tell prospective clients: "If we meet at a party six months from now, I don't want you to say 'Jason helped us improve our AI answers.' I want you to say 'Jason helped us close our Series A.'"

That's the difference between solving AI problems and solving business problems.

---

If you found this useful, follow me on Twitter [@jxnlco](https://twitter.com/jxnlco) for more AI insights. And if you're struggling with your AI strategy, DM me. I might be able to help.

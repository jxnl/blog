# Chapter 0 Slides

## jxnl.co

@jxnlco

<!-- Welcome everyone to Systematically Improving RAG Applications. I'm Jason Liu, and I'm excited to be here with all of you today. This is session zero, where we're going to set the foundation for everything we'll cover over the next six weeks. Today's focus is on the critical mindset shift from implementation to improvement - thinking about RAG as a product, not just a technical project. -->

## Systematically Improving RAG Applications

**Session 0:** Beyond Implementation to Improvement: A Product Mindset for RAG

Jason Liu

---

## Welcome to the Course

**Instructor:** Jason Liu - AI/ML Consultant & Educator

**Mission:** Dismantle guesswork in AI development and replace it with structured, measurable, and repeatable processes.

**Your Commitment:**
- Stick with the material
- Have conversations with teammates  
- Make time to look at your data
- Instrument your systems
- Ask yourself: "What work am I trying to do?"

<!-- My mission is to dismantle guesswork in AI development and replace it with structured, measurable, and repeatable processes. This course is designed to give you systems thinking about RAG that will serve you well regardless of what new technologies emerge. I need you to make some commitments though - stick with the material even when it gets challenging, have conversations with your teammates about what you're learning, make time to actually look at your data, instrument your systems properly, and constantly ask yourself "what work am I trying to do?" This last question is critical - it forces you to think about user needs rather than just technical capabilities. -->

---

## Who Am I?

**Background:** Computer Vision, Computational Mathematics, Mathematical Physics (University of Waterloo)

**Facebook:** Content Policy, Moderation, Public Risk & Safety
- Built dashboards and RAG applications to identify harmful content
- Computational social sciences applications

**Stitch Fix:** Computer Vision, Multimodal Retrieval  
- Variational autoencoders and GANs for GenAI
- **$50M revenue impact** from recommendation systems
- $400K annual data curation budget
- Hundreds of millions of recommendations/week

<!-- Let me tell you a bit about my background so you understand where I'm coming from. I studied computer vision, computational mathematics, and mathematical physics at University of Waterloo. At Facebook, I worked on content policy and moderation - building dashboards and RAG applications to identify harmful content at scale. This is where I first learned about the challenges of production AI systems. At Stitch Fix, I worked on computer vision and multimodal retrieval systems. We were using variational autoencoders and GANs for generative AI before it was cool. The key point here is scale and impact - our recommendation systems had a $50M revenue impact, we had a $400K annual data curation budget, and we served hundreds of millions of recommendations per week. This taught me that successful AI systems are about systematic processes, not just clever algorithms. -->

---

## Current Focus

**Why Consulting vs Building?**
- Hand injury in 2021-2022 limited typing
- Highest leverage: advising startups and education
- Helping others build while hands recover

**Client Experience:**
- HubSpot, Zapier, Limitless, and many others
- Personal assistants, construction AI, research tools
- Query understanding, prompt optimization, embedding search
- Fine-tuning, MLOps, and observability

<!-- You might wonder why I'm consulting rather than building my own company. I had a hand injury in 2021-2022 that severely limited my typing ability. During recovery, I realized that my highest leverage was in advising startups and education rather than hands-on coding. I've worked with companies like HubSpot, Zapier, Limitless, and many others across diverse domains - personal assistants, construction AI, research tools. The common thread is always query understanding, prompt optimization, embedding search, fine-tuning, MLOps, and observability. What I've learned is that the same systematic principles apply regardless of domain or technology stack. -->

---

## Who Are You?

**Cohort Composition:**
- **30%** Founders and CTOs
- **20%** Senior Engineers  
- **50%** Software Engineers, Data Scientists, PMs, Solution Engineers, Consultants

**Companies Represented:**
- OpenAI, Amazon, Microsoft, Google
- Anthropic, NVIDIA, and many others

**Excited to hear about your challenges and experiences!**

<!-- Now let me tell you about who you are, because this cohort is incredible. About 30% of you are founders and CTOs, 20% are senior engineers, and 50% are software engineers, data scientists, product managers, solution engineers, and consultants. You're coming from companies like OpenAI, Amazon, Microsoft, Google, Anthropic, NVIDIA, and many others. This diversity is exactly what makes this course valuable - you're bringing different perspectives and challenges. I'm genuinely excited to hear about what you're working on and what problems you're trying to solve. Your real-world experiences will make this course better for everyone. -->

---

## Course Structure: 6-Week Journey

### Week 1: Synthetic Data Generation
- Create precision/recall evaluations
- Start with text chunks → synthetic questions
- Build baseline evaluation suite

### Week 2: Fine-Tuning and Few-Shot Examples
- Convert evals to few-shot examples
- Fine-tune models for better performance
- Evaluate rerankers and methodologies

### Week 3: Deploy and Collect Feedback
- Deploy system to real users
- Collect ratings and feedback
- Improve evals with real user data

<!-- Here's our journey over the next six weeks. Week 1 is all about synthetic data generation - we'll create precision and recall evaluations by starting with your existing text chunks and generating synthetic questions. This builds your baseline evaluation suite. Week 2 focuses on fine-tuning - we'll convert those evaluations into few-shot examples and fine-tune models for better performance, evaluating rerankers and methodologies. Week 3 is about deployment and feedback collection - getting your system in front of real users, collecting ratings and feedback, and using that real user data to improve your evaluations. This is where synthetic data meets reality. -->

---

## Course Structure (continued)

### Week 4: Topic Modeling and Segmentation  
- Use clustering to identify valuable topics
- Decide what to double down on vs abandon
- Focus resources on economically valuable work

### Week 5: Multimodal RAG Improvements
- Incorporate images, tables, code search
- Contextual retrieval and summarization
- Target specific query segments

### Week 6: Function Calling and Query Understanding
- Combine all systems with intelligent routing
- Query → Path selection → Multimodal RAG → Final answer
- Complete end-to-end orchestration

<!-- Week 4 is about topic modeling and segmentation - we'll use clustering to identify the most valuable topics in your data and help you decide what to double down on versus what to abandon. This is where resource allocation becomes strategic. Week 5 covers multimodal RAG improvements - incorporating images, tables, code search, contextual retrieval and summarization, all targeted at specific query segments you've identified. Finally, Week 6 ties everything together with function calling and query understanding - combining all your systems with intelligent routing so queries flow to the right retrieval path and get multimodal treatment before final answer generation. -->

---

## Learning Format

**Asynchronous Lectures (Fridays)**
- Watch videos on your schedule
- Take notes and prepare questions

**Office Hours (Tuesdays & Thursdays)**  
- Multiple time zones supported
- Active learning and discussion
- Question-driven sessions

**Guest Lectures (Wednesdays)**
- Industry experts and practitioners
- Q&A with speakers
- Real-world case studies

**Slack Community**
- Ongoing discussions
- Peer support and collaboration

<!-- Here's how the learning format works. Asynchronous lectures drop on Fridays - watch them on your schedule, take notes, prepare questions. Office hours happen Tuesdays and Thursdays with multiple time zones supported. These aren't passive lectures - they're active learning sessions driven by your questions. Guest lectures on Wednesdays bring in industry experts and practitioners for Q&A and real-world case studies. And we have a Slack community for ongoing discussions and peer support. The key is active participation - this isn't a course you can just watch passively. -->

---

## The Critical Mindset Shift

### ❌ Implementation Mindset
- "We need to implement RAG"
- Obsessing over embedding dimensions  
- Success = works in demo
- Big upfront architecture decisions
- Focus on picking "best" model

### ✅ Product Mindset  
- "We need to help users find answers faster"
- Tracking answer relevance and task completion
- Success = users keep coming back
- Architecture that can evolve
- Focus on learning from user behavior

**Launching your RAG system is just the beginning!**

<!-- This is the critical mindset shift I need you to make. Most teams have an implementation mindset - "we need to implement RAG," obsessing over embedding dimensions, considering success as "works in demo," making big upfront architecture decisions, focusing on picking the "best" model. But what you need is a product mindset - "we need to help users find answers faster," tracking answer relevance and task completion, success means users keep coming back, architecture that can evolve, focus on learning from user behavior. Launching your RAG system is just the beginning, not the end. The real work starts after launch. -->

---

## Why Most RAG Implementations Fail

**The Problem:** Treating RAG as a technical project, not a product

**What Happens:**
1. Focus on technical components (embeddings, vector DB, LLM)
2. Consider it "complete" when deployed
3. Works for demos, struggles with real complexity
4. Users lose trust as limitations surface
5. No clear metrics or improvement process
6. Resort to ad-hoc tweaking based on anecdotes

**The Solution:** Product mindset with continuous improvement

<!-- Let me explain why most RAG implementations fail. The core problem is treating RAG as a technical project rather than a product. Here's what typically happens: teams focus on technical components like embeddings, vector databases, and LLMs. They consider the project "complete" when it's deployed. It works great for demos but struggles with real-world complexity. Users start losing trust as limitations surface. There are no clear metrics or improvement processes, so teams resort to ad-hoc tweaking based on anecdotes. The solution is adopting a product mindset with continuous improvement. RAG is never "done" - it's always evolving. -->

---

## The Key Insight: RAG as Recommendation Engine

**Stop thinking:** Retrieval → Augmentation → Generation

**Start thinking:** Recommendation Engine + Language Model

```
User Query → Query Understanding → Multiple Retrieval Paths
                                    ↓
                        [Document] [Image] [Table] [Code]
                                    ↓
                          Filtering & Ranking
                                    ↓
                            Context Assembly
                                    ↓
                              Generation
                                    ↓
                             User Response
                                    ↓
                             Feedback Loop
```

<!-- This is the key insight that will change how you think about RAG. Stop thinking of it as simple "Retrieval, Augmentation, Generation." Start thinking of it as a recommendation engine plus a language model. Look at this flow: user query goes through query understanding, which triggers multiple retrieval paths - documents, images, tables, code. Then filtering and ranking, context assembly, generation, user response, and critically - a feedback loop. This is exactly how recommendation systems work at companies like Netflix or Amazon. RAG is fundamentally a recommendation problem where you're recommending the most relevant information to include in the generation context. -->

---

## What This Means

### 1. Generation Quality = Retrieval Quality
- World's best prompt + garbage context = garbage answers
- Focus on getting the right information to the LLM

### 2. Different Questions Need Different Strategies
- Amazon doesn't recommend books like electronics
- Your RAG shouldn't use same approach for every query

### 3. Feedback Drives Improvement  
- User interactions reveal what works
- Continuous learning from real usage patterns

<!-- Understanding RAG as a recommendation engine has three critical implications. First, generation quality equals retrieval quality. You can have the world's best prompt, but if you feed garbage context to your LLM, you'll get garbage answers. Focus on getting the right information to the LLM, not just better prompts. Second, different questions need different strategies. Amazon doesn't recommend books the same way it recommends electronics. Your RAG shouldn't use the same approach for every query type. Third, feedback drives improvement. User interactions reveal what actually works. You need continuous learning from real usage patterns, not just theoretical performance metrics. -->

---

## What Does Success Look Like?

### Feeling of Success
- **Less anxiety** when hearing "just make the AI better"
- **Less overwhelmed** when told to "look at your data"  
- **Confidence** in making data-driven decisions

### Tangible Outcomes
- Identify high-impact tasks systematically
- Prioritize and make informed trade-offs
- Choose metrics that correlate with business outcomes
- Drive user satisfaction, retention, and usage

<!-- What does success look like? There's both a feeling component and tangible outcomes. For the feeling of success, you'll have less anxiety when someone says "just make the AI better" because you'll have systematic approaches. You'll feel less overwhelmed when told to "look at your data" because you'll know what to look for and how to act on what you find. You'll have confidence in making data-driven decisions because you'll have the right metrics and processes. For tangible outcomes, you'll be able to identify high-impact tasks systematically, prioritize and make informed trade-offs, choose metrics that actually correlate with business outcomes, and ultimately drive user satisfaction, retention, and usage. -->

---

## The System Approach

**What is a System?**
- Structured approach to solving problems
- Framework for evaluating technologies  
- Decision-making process for prioritization
- Methodology for diagnosing performance
- Standard metrics and benchmarks

**Why Systems Matter:**
- Frees mental energy for innovation
- Replaces guesswork with testing
- Enables quantitative vs "feels better" assessments
- Secures resources through data-driven arguments

<!-- Let me explain what I mean by a system approach. A system is a structured approach to solving problems, a framework for evaluating technologies, a decision-making process for prioritization, a methodology for diagnosing performance, and a set of standard metrics and benchmarks. Why do systems matter? They free up mental energy for actual innovation instead of constantly deciding how to approach problems. They replace guesswork with systematic testing. They enable quantitative assessments instead of subjective "feels better" evaluations. And crucially, they help you secure resources through data-driven arguments rather than hopes and intuition. -->

---

## RAG vs Recommendation Systems

**The Reality:** RAG is a 4-step recommendation system

1. **Multiple Retrieval Indices** (multimodal: images, tables, text)
2. **Filtering** (top-k selection)  
3. **Scoring/Ranking** (rerankers, relevance)
4. **Context Assembly** (prepare for generation)

**The Problem:** Engineers focus on generation without knowing if right information is retrieved

**The Solution:** Improve search to improve retrieval to improve generation

<!-- The reality is that RAG is fundamentally a 4-step recommendation system. First, you have multiple retrieval indices that are multimodal - images, tables, text. Second, filtering with top-k selection. Third, scoring and ranking with rerankers and relevance models. Fourth, context assembly to prepare information for generation. The problem I see everywhere is that engineers focus intensely on generation - tweaking prompts, trying different models - without knowing if the right information is even being retrieved. The solution is to improve search first, which improves retrieval, which then improves generation. Fix the foundation before worrying about the roof. -->

---

## Experimentation Over Implementation

**Instead of:** "Make the AI better"

**Ask:**
- Why am I looking at this data?
- What's the goal and hypothesis?
- What signals am I looking for?
- Is the juice worth the squeeze?
- How can I use this to improve?

**Success Formula:** Flywheel in place + Consistent effort = Continuous improvement

Like building muscle: track calories and workouts, don't just weigh yourself daily

<!-- This is about shifting from implementation thinking to experimentation thinking. Instead of vague directions like "make the AI better," ask specific questions: Why am I looking at this data? What's the goal and hypothesis? What signals am I looking for? Is the juice worth the squeeze? How can I use this to improve? The success formula is simple: get your flywheel in place plus consistent effort equals continuous improvement. It's like building muscle - you track calories and workouts, you don't just weigh yourself daily and hope for the best. You measure the inputs that drive the outputs you want. -->

---

## Course Commitments

### My Commitment to You
- Be online and answer questions
- Provide extensive office hours support
- Share real-world experience and case studies
- Connect you with industry experts

### Your Commitment
- Engage with the material actively
- Look at your own data and systems
- Participate in discussions and office hours
- Apply learnings to your real projects

**Together, we'll transform your RAG from demo to production-ready product**

<!-- Let's talk about our mutual commitments. My commitment to you is to be online and answer your questions, provide extensive office hours support, share real-world experience and case studies from my consulting work, and connect you with industry experts who can provide additional perspectives. Your commitment is to engage with the material actively - don't just watch passively. Look at your own data and systems - this course only works if you apply it to real problems. Participate in discussions and office hours - your questions make everyone's learning better. Apply learnings to your real projects - this isn't theoretical. Together, we'll transform your RAG from a demo that impresses stakeholders to a production-ready product that users actually rely on. -->

---

## Key Takeaway

> **Successful RAG systems aren't projects that ship once—they're products that improve continuously.**

The difference between success and failure isn't the embedding model or vector database you choose.

It's whether you treat RAG as:
- **❌ Static implementation** that slowly decays
- **✅ Living product** that learns from every interaction

**Let's build systems that get better every week! 🚀**

<!-- Here's the key takeaway I want you to remember: Successful RAG systems aren't projects that ship once - they're products that improve continuously. The difference between success and failure isn't the embedding model or vector database you choose. The technology matters far less than your approach. It's whether you treat RAG as a static implementation that slowly decays over time, or as a living product that learns from every interaction and gets better continuously. Let's build systems that get better every week, not systems that peak on launch day and decline from there. -->

---

## Next Week

**Week 1: Kickstart the Data Flywheel**

- Synthetic data generation strategies
- Building precision/recall evaluations
- Creating your evaluation foundation
- "Fake it till you make it" with synthetic data

**Come prepared to look at your data!**

<!-- Next week we're going to kickstart the data flywheel. We'll cover synthetic data generation strategies, building precision and recall evaluations, creating your evaluation foundation, and the philosophy of "fake it till you make it" with synthetic data. This might seem counterintuitive, but synthetic data is often the fastest way to bootstrap your evaluation systems before you have enough real user data. Come prepared to look at your actual data - bring your real text chunks, your real queries, your real problems. The course works best when you're applying it to something concrete. -->
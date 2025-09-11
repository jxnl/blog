---
title: Converting Evaluations into Training Data
description: Learn how to use your evaluation data to create few-shot examples and training datasets for fine-tuning
authors:
  - Jason Liu
date: 2025-03-14
tags:
  - few-shot
  - fine-tuning
  - training-data
  - evaluation
---

# Converting Evaluations into Training Data for Fine-Tuning

## Learning Objectives

By the end of this chapter, you will be able to:

1. **Understand why off-the-shelf embeddings fail for specialized applications** - Recognize the limitations of generic models and the hidden assumptions that prevent them from handling domain-specific similarity requirements
2. **Master the fundamentals of similarity and objective functions** - Define what "similarity" means in your specific context and design training objectives that capture these relationships  
3. **Build custom embeddings using synthetic data and evaluation frameworks** - Transform your Chapter 1 evaluation examples into training data for fine-tuning embedding models
4. **Apply contrastive learning techniques for retrieval systems** - Implement triplet structures with hard negatives to improve domain-specific retrieval accuracy by 6-10%
5. **Design and implement fine-tuning workflows** - Execute complete embedding and re-ranker training processes that cost hundreds of dollars rather than thousands
6. **Create continuous data collection systems** - Start logging relevancy signals now to build the training datasets that will power future improvements

These objectives build directly on the evaluation foundation from Chapter 1 and prepare you for the feedback collection mechanisms in Chapter 3.

### Key Insight

**If you're not fine-tuning, you're Blockbuster, not Netflix.** The goal isn't to fine-tune language models (which are expensive and complex), but to fine-tune embedding models that move toward your specific data distributions and improve retrieval, not generation.

!!! info "Learn the Complete RAG Playbook"
    All of this content comes from my [Systematically Improving RAG Applications](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK) course. Readers get **20% off** with code EBOOK. Join 500+ engineers who've transformed their RAG systems from demos to production-ready applications.

!!! success "Fine-Tuning Cost Reality Check"
**Real Numbers from Production:**
    - **Just 6,000 examples = 6-10% improvement** (Sentence Transformers team validated)
    - **Cost: Hundreds of dollars in API calls** (vs tens of thousands for data labeling previously)
    - **Time: 40 minutes training on your laptop** 
    - **Systems at 70% can reach 85-90%** - remember that 50% to 90% recall jump from Chapter 1? That's exactly this kind of improvement
    - **Companies see 14% accuracy boost over baseline** just from fine-tuning cross-encoders
    - **12% increase in exact match** by training better passage encoders
    - **20% improvement in response accuracy** with rerankers
    - **30% reduction in irrelevant documents** with proper fine-tuning

    **Language Model Fine-Tuning:**
    - Cost: $100-1000s depending on model size
    - Time: Hours to days
    - Infrastructure: Multiple GPUs or specialized services
    - Complexity: Requires ML expertise

    This dramatic difference explains why embedding fine-tuning should be your first focus.

## Introduction

Remember in Chapter 1 where we talked about that $100M company with only 30 evaluation examples? Well, here's the good news: once you have those evaluation examples, you can multiply their value. The synthetic data and evaluation framework from Chapter 1 becomes your training data in this chapter.

**Building on Chapter 1's Foundation:**
Your evaluation examples (synthetic questions + ground truth) now become few-shot examples and training data. We're turning that evaluation flywheel into a fine-tuning flywheel.

Here's the thing: the data you collect for evaluation shouldn't just sit there. Every question, every relevance judgment, every piece of feedback—it can all be used to improve your system. That's what we'll cover here.

**Key Philosophy:** "This is the "wax on, wax off" moment: 20 examples become evals (Chapter 1), 30 examples become few-shot prompts, 1,000 examples let you start fine-tuning. Remember that $100M company with 30 evals? Once you have that data, this is how you turn it into actual improvements. It's never done, just gets better."

The process is straightforward: you start with evaluation examples, turn them into few-shot prompts, then eventually use them to fine-tune your embedding models and re-rankers. Each step builds on the last.

## Why Generic Embeddings Fall Short

Let me start with something that trips up a lot of teams: generic embeddings from providers like OpenAI often don't work great for specialized applications. They're good models, don't get me wrong. But they're built to handle everything, which means they don't handle your specific thing particularly well.

### Limitation of Generic Models

Generic embedding models come with built-in assumptions about what "similarity" means. You don't know:

- What data they were trained on
- How they defined "success" during training
- How they weighted different types of similarity
- What trade-offs they made to work for everyone

### The Elusive Nature of "Similarity"

Embedding models seem simple enough: they turn text into numbers, and similar text should end up with similar numbers. Measure the distance between vectors and you know how similar things are.

**Domain-Specific Similarity Example:** In e-commerce, what makes two products "similar"? Are they substitutes (different brands of red shirts) or complements (a shirt and matching pants)? Depends on what you're trying to do.

Take music recommendations. Songs might be similar because they're the same genre, or because they show up in the same playlists, or because the same people like them. If you're adding songs to a playlist, you want one kind of similarity. If you're building Spotify's Discovery Weekly, you want something else entirely.

Take dating apps - should "I love coffee" and "I hate coffee" be similar? Linguistically opposite, but both care enough about coffee to mention it. Generic embeddings see them as opposites. But for matching people? Maybe that matters more than word similarity. This is exactly the kind of nuance you miss without domain-specific fine-tuning.

Here's the thing: **What actually matters for a dating app is whether two people will like each other**, not whether their profiles use similar words. Generic embeddings trained on web text have no idea about this.

The problem is that "similarity" means different things in different contexts. There's no universal right answer—it depends on what you're trying to do.

### The Hidden Assumptions in Provider Models

When you use OpenAI or Cohere's embeddings, you're stuck with their definition of similarity. It might not match what you need.

**Legal Document Search Example:** One memorable case involved a legal document search application. The generic embeddings performed reasonably well for finding factual information but struggled with procedural questions. The embeddings didn't adequately capture the relationships between legal procedures and their applications—a specific type of similarity vital to legal professionals but not emphasized in general-purpose training data.

Provider embeddings aren't bad—they're great for general use. But your application probably isn't general. Fine-tuning with your own data fixes this mismatch.

## From Evaluation to Few-Shot Examples

Before jumping into fine-tuning, there's something simpler you can try: few-shot examples. Let's talk about turning your evaluation data into prompts that actually work.

### The Power of Examples in Context

Few-shot learning is pretty straightforward: instead of retraining the model, you just show it some examples in the prompt. No special infrastructure needed.

### How Few-Shot Learning Works

When you provide a language model with examples of how to respond to similar queries, you activate its ability to recognize patterns and apply them to new inputs. It's like showing a human a few examples of a task before asking them to perform it themselves—no specialized training required, just clear demonstrations.

This works especially well for RAG because different types of questions need different approaches. Show the model a few examples and it figures out what kind of question it's dealing with.

### Selecting the Right Examples

Don't just grab random examples from your evaluation set. I've watched teams do this and make their model worse. You need to pick the right examples.

**Characteristics of Good Examples:**

- Match the queries your users actually ask
- Show clear reasoning steps
- Cover different types of questions
- Aren't too weird or specific

Remember the synthetic data generation techniques we explored in Chapter 1? You can use those same methods to generate examples specifically for few-shot learning. The key difference is that for few-shot examples, you need not just questions and answers, but also the reasoning process that connects them.

### Building Your Few-Shot Library

Build yourself a library of few-shot examples. Here's how I do it:

1. Filter your evaluation data for the best examples
2. Group them by type (factual questions, how-to guides, comparisons)
3. Pick representative examples from each group
4. Format them consistently
5. Test them with your actual pipeline
6. Keep the ones that work, toss the ones that don't

### Structured Few-Shot Prompt Example

```
You are an assistant specialized in answering questions about [domain].

Here are some examples of how to answer questions:

Question: [Example Question 1]
Thinking: [First, I'll identify the key entities in the question. Then I'll look for information about their relationship...]
Answer: [Example Answer 1]

Question: [Example Question 2]
Thinking: [This appears to be a comparison question. I should look for information about both entities and highlight similarities and differences...]
Answer: [Example Answer 2]

Now please answer the following question:
Question: [Actual User Query]
```

Having an organized library means you can track what works, swap out examples that get stale, and keep improving based on what your users actually do.

## Practical Implementation: Building the Data Flywheel for Fine-Tuning

Few-shot examples are great, but fine-tuning your embeddings is where you see real improvements. The trick is getting enough good data to make it worth doing.

### Starting the Flywheel

Building a RAG system is iterative. You start with a few examples for evaluation. Those become few-shot prompts. Eventually you have enough for fine-tuning. Each stage builds on the last.

**Data Collection Milestones:**
- With 20 examples, you can build basic evaluation benchmarks
- With 30 examples, you can create effective few-shot prompts
- With 1000+ examples, you can fine-tune your retrieval models

What's nice is you're not throwing away data—you're using it differently as you get more of it.

### Start Collecting Now

You need to start collecting the right data now, even if you're not ready to fine-tune yet. The sooner you start logging relevant user interactions, the sooner you'll reach the critical mass needed for fine-tuning.

### What Data Should You Log?

For RAG, here's what you should be logging:

1. What users actually ask
2. Which chunks got used in responses
3. Which responses users liked (or didn't)
4. Which queries needed follow-ups

This tells you what's actually relevant to what—which is exactly what you need for fine-tuning.

### Domain-Specific Relevance Signals

For other applications, the relevance signals will differ:

- In e-commerce: track which items are purchased together, viewed in sequence, or added to the same lists
- For music recommendations: log which songs appear in the same playlists or are hearted by the same users
- For dating apps: record which profiles match and go on to have meaningful conversations

The key is defining what "relevance" means in your specific context and systematically collecting data that captures this relationship.

### Start Logging Yesterday!

I've seen numerous companies hire machine learning engineers to fine-tune embedding models, only to realize they hadn't started logging relevance data. These teams then have to wait 3-6 months to collect enough data before they can begin the work they intended to do immediately.

**The most important action you can take today is to start logging relevance data**, even if you're not ready to hire ML specialists or begin fine-tuning. Save the top 20-40 chunks for each query and use an LLM to mark relevance if human annotation isn't feasible. This data will be invaluable when you're ready to improve your models.

I watched a team build a great RAG app for internal docs. Six months later they wanted to fine-tune embeddings but had zero data because they never set up logging. Had to start from scratch with synthetic data. Don't do this.

!!! success "Small Datasets Can Make Big Differences"
The team at Sentence Transformers has demonstrated that even with just 6,000 examples, you can achieve 6-10% better performance. With 40 minutes of fine-tuning on a laptop, you can create significant lifetime value for your application. This makes fine-tuning embedding models accessible even to teams without massive datasets or specialized infrastructure.

## Understanding Contrastive Learning for Embeddings

Let's talk about how fine-tuning actually works. Most approaches use something called contrastive learning.

### Learning Through Contrasts

Contrastive learning is simple: you teach the model what's similar by showing it what's different. It's all about relationships, not absolute values.

### Triplet Structure

The most common implementation uses a structure called a triplet, which consists of:

1. An **anchor** (usually the query)
2. A **positive example** (a document that's relevant to the query)
3. A **negative example** (a document that's not relevant to the query)

The goal of training is straightforward: adjust the embedding model so that the distance between the anchor and positive example decreases, while the distance between the anchor and negative example increases. In other words, pull similar things closer together and push dissimilar things further apart.

```mermaid
graph LR
    A[Anchor: Query] --- P[Positive: Relevant Document]
    A --- N[Negative: Irrelevant Document]
    P -.- |"Pull Closer"| A
    N -.- |"Push Away"| A
````

This works great for embeddings because you're directly optimizing the distance relationships that matter for retrieval.

### Creating Effective Triplets for RAG

For RAG applications, there are several natural ways to create triplet datasets:

- **Anchor**: The user's query
- **Positive**: Document chunks that were cited in the final response or received positive feedback
- **Negative**: Document chunks that were retrieved but not cited, or received negative feedback

### Healthcare RAG Triplet Example

Imagine a healthcare RAG application where a user asks:

```
What are the side effects of medication X?
```

Our retrieval system might return several documents, including:

```
Document A: "Medication X may cause drowsiness, nausea, and in rare cases, allergic reactions."

Document B: "Medication X is used to treat high blood pressure and should be taken with food."
```

If Document A is cited in the response while Document B isn't, we can create a triplet:

```json
{
  "anchor": "What are the side effects of medication X?",
  "positive": "Medication X may cause drowsiness, nausea, and in rare cases, allergic reactions.",
  "negative": "Medication X is used to treat high blood pressure and should be taken with food."
}
```

Through many such examples, the model learns that queries about side effects should be closer to texts describing adverse reactions than to texts describing indications or administration instructions.

### The Challenge of Hard Negatives and How UX Can Help

Notice something subtle in that example? The negative document is still about the same medication—just not about side effects. That's a "hard negative": similar in some ways, different in the ways that matter.

### Hard Negative Mining Strategies

**Effective Approaches:**

1. **Semantic Similarity with Different Intent:**
   - "Software engineer" vs "Software engineering recruiter"
   - Both about software roles, but serving different user needs

2. **User Deletion Signals:**
   - Track which documents users actively remove from results
   - These are perfect hard negatives - retrieved but explicitly rejected

3. **Category Boundaries:**
   - Items from adjacent but different categories
   - Example: "Red running shoes" vs "Red dress shoes"

4. **Temporal Relevance:**
   - Outdated versions of correct information
   - Example: "2023 tax rates" when user needs "2024 tax rates"

> **Agentic Retrieval Perspective**
> 
> Colin Flaherty's work on agentic coding systems reveals a surprising insight: "We found that for SweeBench tasks, embedding-based retrieval was not the bottleneck - grep and find were sufficient." The agent's persistence effectively compensated for less sophisticated tools. This suggests that while fine-tuning embeddings is valuable, the agent layer can sometimes overcome retrieval limitations through persistence. [Learn more about agentic approaches →](../talks/colin-rag-agents.md)

### Value of Hard Negatives

Hard negatives are way more valuable than easy ones. If your negative example was about car maintenance instead of medications, the model learns nothing—it already knows car maintenance isn't relevant to medication side effects.

The real challenge is teaching the model to distinguish between different aspects of the same topic. That's where you get actual improvements.

That's why hard negative mining matters—finding examples that are tricky but teachable.

### Designing UX for Better Training Data

If you're serious about improving your embeddings, consider explicitly designing your UX to capture these signals:

1. **Document-level feedback mechanisms**: Add simple thumbs up/down options next to each retrieved document, not just for the final answer

2. **Click tracking**: Record which documents users click on and which they ignore—those ignored despite ranking highly are excellent hard negative candidates

3. **Dwell time analysis**: If a user quickly returns from a document without spending time reading it, that's a strong signal it wasn't relevant

4. **Explicit comparison interfaces**: For critical applications, consider interfaces that ask users to compare documents and select the most relevant one

5. **Query reformulation tracking**: When a user modifies their query slightly and gets better results, you can pair the original query with documents from the improved results to create training pairs

One team I worked with added a "more like this" button next to helpful documents. Users loved it, and it gave us perfect training data about what users actually consider similar—which often wasn't what we expected from just reading the text.

## The Power of Re-Rankers in RAG Systems

Embeddings do the heavy lifting in retrieval, but re-rankers add polish. The difference: embeddings process queries and documents separately, while re-rankers look at them together and can make smarter decisions.

### Bi-Encoders vs. Cross-Encoders: Understanding the Trade-offs

Here's the trade-off: embeddings are fast, re-rankers are accurate.

### Model Comparison

**Bi-encoders (embedding models):**
- Encode query and document independently
- Allow pre-computation of document embeddings
- Enable fast vector similarity operations
- Work well for first-pass retrieval of candidates
- Examples include OpenAI's text-embedding models, SBERT, MPNet

**Cross-encoders (re-rankers):**
- Process query and document together as a pair
- Cannot pre-compute relevance scores
- Provide more accurate relevance judgments
- Work best for re-ranking a smaller set of candidates
- Examples include Cohere Rerank, monoT5

Use them together: embeddings grab candidates quickly, re-ranker sorts them properly.

**Re-Ranker Success Story:** One team I worked with was debating whether to invest in fine-tuning their embeddings or implementing a re-ranker. When they tested both approaches, they found that fine-tuning embeddings improved recall from 65% to 78%, while adding a re-ranker (even without fine-tuning) improved it to 82%. Combining both approaches pushed performance to 91%—a transformative improvement from where they started.

### Creating Training Data for Re-Rankers

Re-rankers work better with graded relevance scores instead of just yes/no labels. Try this:

1. Score query-document pairs on a scale (like 0-5)
2. Include the full range of scores
3. Train the model to predict these scores

### Graded Relevance Example

```json
{
  "query": "How do I reset my password?",
  "documents": [
    {"text": "Step-by-step password reset guide", "score": 5},
    {"text": "General account management information", "score": 3},
    {"text": "Creating a strong password", "score": 2},
    {"text": "About our company", "score": 0}
  ]
}
```

This helps the re-ranker understand degrees of relevance, not just binary yes/no. Users notice the difference.

## Practical Fine-Tuning Workflow

Here's a workflow that actually works, based on what I've seen teams do successfully.

### When to Fine-Tune Embeddings

Fine-tune your embedding models when:

1. **You have 6,000+ query-document pairs** with relevance labels
2. **Domain-specific terminology** isn't well-represented in generic models
3. **Your definition of similarity** differs from general language understanding
4. **Cost at scale** justifies maintaining your own infrastructure

!!! tip "Production Insight"
From office hours: "With just 6,000 examples from your domain, you can train embedding models and cross-encoders that outperform general-purpose models on your specific tasks. This typically costs around $1.50 and takes about 40 minutes on a laptop."

### The Fine-Tuning Process

#### Step 1: Data Preparation

Transform your evaluation data into training format:

- **Positive pairs**: Query-document combinations that should rank highly
- **Hard negatives**: Similar but incorrect documents for each query
- **Validation set**: Hold out 20% for testing improvements

!!! warning "Critical Success Factor"
The quality of your hard negatives determines the quality of your fine-tuned model. Documents that are topically similar but serve different intents make the best hard negatives.

#### Step 2: Model Selection

Choose your base model wisely:

- **For English-only**: Modern BERT models with 8,000 token context (vs original 512)
- **For multilingual**: Cohere's multilingual models or mE5
- **For specialized domains**: Start with models pre-trained on similar content

#### Step 3: Training Infrastructure

You don't need massive infrastructure:

- **Local training**: Consumer GPU with 8GB+ VRAM
- **Cloud notebooks**: Colab Pro or similar services
- **Training time**: 30-60 minutes for most datasets
- **Cost**: Under $5 for most use cases

### Measuring Success

Track these metrics before and after fine-tuning:

1. **Recall@K** at different values (5, 10, 20)
2. **Mean Reciprocal Rank (MRR)**
3. **Business metrics** tied to retrieval quality
4. **Latency impact** if self-hosting

!!! example "Real-World Results"
A healthcare company fine-tuned embeddings on medical abbreviations where generic models confused similar acronyms. Results: - Recall@10 improved from 72% to 89% - Reduced confusion between similar medical terms - Cost: $1.50 in compute, 45 minutes of training - ROI: Prevented multiple medical documentation errors

### Common Pitfalls to Avoid

1. **Training on too little data**: Wait until you have at least 6,000 examples
2. **Ignoring hard negatives**: Easy negatives don't improve the model
3. **Not validating on real queries**: Synthetic data alone isn't sufficient
4. **Over-optimizing on metrics**: Ensure improvements translate to user experience

### Resources for Implementation

For detailed implementation guides:

- [Sentence Transformers Training Documentation](https://www.sbert.net/docs/training/overview.html)
- [Cohere's Fine-tuning Guide](https://docs.cohere.com/docs/fine-tuning)
- [OpenAI's Fine-tuning Best Practices](https://platform.openai.com/docs/guides/fine-tuning)

!!! quote "Key Takeaway"
"It's probably a bad idea to train your own language model, but it's a very good idea to train your own embedding model. The infrastructure requirements are minimal, the process is well-understood, and the improvements are substantial for domain-specific applications."

## Testing Different Approaches Systematically

Now that you have evaluation data from Chapter 1, you can start testing different approaches. You need to be systematic about this.

!!! tip "Good Experimentation Practices"
For each experiment:

1. Have a clear hypothesis ("Re-ranker will improve recall@10 by 15%")
2. Define success before you start
3. Change one thing at a time
4. Measure using your established metrics
5. Document what worked AND what didn't

Experiments worth trying:

1. Different embedding models (OpenAI vs Cohere vs open-source)
2. Chunk sizes and overlaps
3. Lexical vs semantic vs hybrid retrieval
4. Adding a re-ranker
5. Different few-shot examples

!!! example "Debate Resolved Through Data"
One team I worked with spent weeks debating which embedding model to use, with different team members advocating for their preferred option. Instead of continuing the debate, they implemented a simple experiment: they indexed their documents with three different embedding models and measured recall on their evaluation set. The results settled the debate in hours, not weeks, and the team moved forward with data-backed confidence.

Keep running experiments, measuring results, and iterating. That's how you get better.

## Building a Roadmap for Continuous Improvement

Once you've run some experiments, you can plan what to do next. It's not just about adding features—it's about having a process.

!!! tip "Prioritization Framework"
When deciding what to work on:

- **Impact**: What will move the needle most?
- **Effort**: How much work is it?
- **Dependencies**: What needs to be done first?
- **Risk**: What could break?

I like using a simple impact/effort grid. High impact, low effort goes first—those quick wins build momentum while you're working on the harder stuff.

!!! example "Prioritization in Action"
In one project, we identified that implementing BM25 hybrid retrieval would be high-impact and medium-effort, while fine-tuning custom embeddings would be high-impact but high-effort. We prioritized the hybrid retrieval first, which gave us immediate gains while we collected data for the eventual embedding fine-tuning.

## Linear Adapters: A Cost-Effective Alternative

Before diving into full fine-tuning, consider linear adapters - a technique that can deliver significant improvements at a fraction of the cost.

!!! info "What Are Linear Adapters?"
Linear adapters add a small trainable layer on top of frozen embeddings: - Train only a linear transformation matrix - Keep the base embedding model unchanged - Combine benefits of domain specificity with pre-trained knowledge

    **Cost Comparison:**
    - Full fine-tuning: $50-100 for meaningful datasets
    - Linear adapters: ~$12 for the same improvement
    - Training time: Minutes vs hours

!!! example "When to Use Linear Adapters"
**Perfect for:** - Domain-specific terminology mapping - Multi-domain applications (train separate adapters) - Rapid experimentation - Limited computational resources

    **Implementation:**
    ```python
    # Simplified example
    base_embeddings = model.encode(texts)
    adapted_embeddings = linear_adapter(base_embeddings)
    ```

    You can train different adapters for different query types or domains, switching between them based on query classification.

## Additional Resources

!!! info "Tools and Libraries"

```
### Understanding Embedding Models

1. **Sentence Transformers Library** ([https://www.sbert.net/](https://www.sbert.net/)): This library provides easy-to-use implementations for state-of-the-art embedding models, supporting both pairwise datasets and triplets for fine-tuning. It's my recommended starting point for most teams due to its balance of performance and ease of use.

2. **Modern BERT** ([https://huggingface.co/sentence-transformers](https://huggingface.co/sentence-transformers)): These newer models offer 8,000 token sequence lengths and generally outperform classic BERT-based models. The BGE models in particular have shown excellent performance across many domains and are worth testing in your applications.

3. **Cohere Re-ranking Models** ([https://cohere.com/rerank](https://cohere.com/rerank)): Cohere offers state-of-the-art re-ranking capabilities with a fine-tuning API that makes it relatively easy to customize for your specific needs. In my experience, even their base re-ranker without fine-tuning often provides substantial improvements to retrieval quality.

4. **Specialized Domains**: For specific domains like code, science, or legal documents, look for models pre-trained on related corpora. For example, CodeBERT for programming or SciBERT for scientific literature can provide better starting points than general models.

5. **Comparison to Data Labeling**: Everything we're doing today with fine-tuning embedding models is what I used to pay data labeling teams hundreds of thousands of dollars to do annually. The ML playbook that was once only accessible to large companies with significant budgets is now available to teams of all sizes thanks to advances in transfer learning and fine-tuning techniques.
```

!!! info "Key Concepts"

```
#### Contrastive Learning In-Depth

Contrastive learning trains models to recognize similarities and differences between items by pushing and pulling examples in the embedding space:

- **Triplet Loss**: Optimizes the distance between anchor-positive pairs relative to anchor-negative pairs
- **InfoNCE Loss**: Contrasts a positive pair against multiple negative examples
- **Multiple Negatives Ranking Loss**: Handles batches of queries with multiple negatives per query

#### Scaling and Efficiency Considerations

For large datasets or production workloads:

- **Modal Labs for Parallel Processing**: Consider platforms like [Modal](https://modal.com) for massive parallelization. As mentioned in our sessions, you can embed all of Wikipedia in 15 minutes or train 200 different model variations across 50 GPUs simultaneously, dramatically reducing iteration time from hours to minutes
- Experiment with multi-GPU training for faster iterations
- Evaluate the trade-offs between API costs and self-hosting
- Test multiple model variations simultaneously to find optimal configurations

## This Week's Action Items

Based on the content covered, here are your specific tasks:

### Immediate Actions (Start This Week)

1. **Start Logging Relevancy Data NOW**
   - Don't wait for perfect infrastructure - start collecting query + retrieved chunks + user interactions immediately
   - Save top 20-40 chunks per query for future training data
   - Use LLM judges to mark relevance if human annotation isn't feasible
   - This data will be invaluable when you're ready to fine-tune (don't make the mistake of waiting 3-6 months)

2. **Define Your Domain-Specific Similarity**
   - Clearly define what "relevant" and "similar" mean for your specific application
   - Document edge cases where generic embeddings fail in your domain
   - Create examples of hard negatives (topically similar but contextually different)

3. **Build Few-Shot Examples**
   - Convert your best evaluation examples from Chapter 1 into few-shot prompts
   - Test different few-shot configurations and measure impact on retrieval quality
   - Create a library of examples organized by query type

### Technical Implementation

4. **Experiment with Re-Rankers First**
   - Try Cohere Rerank API (credits provided for course participants)
   - Measure the 10% recall improvement vs 300-500ms latency tradeoff
   - Compare results with and without re-ranking using your evaluation framework

5. **Test Domain-Specific Models**
   - Compare OpenAI embeddings against BGE, E5, or domain-specific models
   - Use your Chapter 1 evaluation framework to measure differences objectively
   - Try modern BERT models with 8,000 token context vs older 512 token models

6. **Prepare for Fine-Tuning**
   - Once you have 1,000+ examples, prepare triplet datasets (anchor, positive, negative)
   - Focus on hard negatives - documents that are topically similar but serve different intents
   - Create graded relevance scores (0-5) rather than binary yes/no labels

### Strategic Planning

7. **Build the Data Flywheel**
   - 20 examples → evaluations
   - 200 examples → few-shot prompts  
   - 2,000 examples → fine-tuning datasets
   - Plan your progression through these milestones

8. **Design UX for Better Training Data**
   - Add document-level feedback mechanisms (thumbs up/down per retrieved chunk)
   - Track click patterns and dwell time on retrieved documents
   - Consider explicit comparison interfaces for critical applications

## Reflection Questions

Take a minute to think about:

1. What specific definition of "similarity" is most important for your application's domain?
2. How would you create effective few-shot examples from your existing evaluation data?
3. What user interactions in your application could provide valuable training signals for fine-tuning?
4. If you had to prioritize one retrieval improvement for your system, would it be embeddings, re-ranking, or something else? Why?
5. What experiments could you run to test your hypotheses about improving retrieval quality?

## Conclusion and Next Steps

We covered a lot:

1. Turning evaluation examples into few-shot prompts
2. Why generic embeddings often aren't good enough
3. Building datasets for fine-tuning
4. How contrastive learning works
5. Running systematic experiments
6. Planning improvements

The main takeaway: don't waste your data. Every question, every bit of feedback, every evaluation—it can all make your system better if you capture and use it.

Fine-tuning embeddings really works, and unlike fine-tuning LLMs, it's actually doable. You can see real improvements with just 6,000 examples.

!!! tip "What's Coming Next"
    In [Chapter 3](chapter3-1.md), we'll dive into deployment strategies, user feedback collection methods, and how to use this feedback to further refine your RAG application. We'll explore practical techniques for gathering implicit and explicit feedback, designing effective user interfaces, and closing the loop between user interactions and system improvements.

!!! info "Related Concepts in Other Chapters" 
    - **Query Segmentation** ([Chapter 4](chapter4-2.md)): Learn how to identify which queries benefit most from fine-tuning 
    - **Specialized Models** ([Chapter 5](chapter5-1.md)): See how fine-tuned embeddings power specialized retrievers 
    - **Router Optimization** ([Chapter 6](chapter6-2.md)): Understand how fine-tuning improves query routing

## Summary

Start with evaluation, add few-shot examples, work up to fine-tuning. Each step makes the next one better.

Do these things now:

1. **Start logging data** - Even if you're not ready to use it
2. **Define what "similar" means for you** - It's different for every application
3. **Add feedback mechanisms** - You'll need the data later
4. **Build your few-shot library** - Start small, grow over time
5. **Try domain-specific models** - They might already solve your problem

If you do this right, every piece of data makes your system better. The improvements compound over time and affect everything—clustering, topic modeling, all of it.

---



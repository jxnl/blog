# Chapter 1 Slides

## jxnl.co

@jxnlco

<!-- Welcome to the first actual lecture for Systematically Improving RAG Applications. This week is all about giving you the tools to kickstart the data flywheel, and in particular thinking about evaluations, the mistakes people make, and then ultimately thinking about synthetic data as a way of addressing a lot of these concerns before you even have users. -->

## Systematically Improving RAG Applications

**Session 1:** Kickstart the Data Flywheel: Fake it Till You Make It

Jason Liu

<!-- Today we're covering the common pitfalls that most AI developers make and the vicious cycle I see in every consulting engagement that I go into. We'll talk about how we over emphasize lagging metrics and how many of us fall victim to absence blindness and intervention bias. -->

---

## Today's Goals

**Break the Vicious Cycle of RAG Development**

- Identify common pitfalls that sabotage RAG applications
- Understand the difference between lagging and leading metrics
- Combat absence blindness and intervention bias
- Build the foundation: synthetic data and evaluations
- Start the data flywheel before you have users

**Focus: Measurements before features**

<!-- This is the key mindset shift I want you to take away today. We need to fundamentally restructure how we think about stand-up meetings and team priorities. Instead of focusing on features, we need to focus on the velocity of learning through experiments. -->

---

## The Challenge: "We Need Complex Reasoning"

> "Often when I hear 'we need complex reasoning' it comes from lack of user empathy"

**Hot Take:** This usually means:
- Haven't looked at customer data in months
- Never asked for specific feedback  
- Building generic solutions for broad problems
- Focusing on features instead of outcomes

**Key Questions to Ask:**
- When was the last time we looked at data from customers?
- When was the last time we read that feedback?
- When was the last time we asked for that feedback?

**Solution:** Build high-specificity tooling that users actually care about

<!-- My first question is, how often do we hear things like "we need more complex reasoning"? My hot take here is that it's often going to be a case of a lack of user empathy. When you hear something like this, I would really challenge you to figure out when was the last time we looked at data from customers and figured out what they want, what they really cared about. This is a general result of a lack of specificity in the tools that we actually build for our customers. -->

---

## Common RAG Developer Pitfalls

### The Vicious Cycle

**Developers unknowingly sabotage their applications through:**

1. **Vague Metrics**
   - "Does it look better?"
   - "Doesn't feel right"
   - No clear success criteria
   - You're sabotaging not only your product but your team and yourself

2. **No Superpowers**
   - Generic solutions for broad problems
   - 30-40% churn rates
   - Too scared to fully launch
   - Focus on features rather than outcomes
   - Mandate too broad, overpromised

3. **Poor Feedback Loops**
   - LLM-based feedback only
   - No actionable insights
   - No roadmap for improvements
   - Feedback not actionable - doesn't identify what's next

<!-- This is how we enter the vicious cycle. These developers unknowingly sabotage their applications because they define very vague metrics. We think things like "does it look better" or "does it feel right?" And ultimately you're sabotaging not only your product but your team and yourself if you don't define these clear metrics. You would be surprised at how pervasive these problems are - there have been companies I've worked with with 100 million dollar valuations with less than 30 evals. -->

---

## The $100M Problem

> "Companies with $100M valuations operating with less than 30 evaluations"

**When something changes, you have no way to understand what moves the needle**

**Real Impact:** I've worked with companies with $100M+ valuations that have fewer than 30 evaluations total

**The Result:**
- Disappointed leadership
- Frustrated developers
- Products that nobody uses
- Endless feature churn

**The Solution:** Focus on metrics and experiments, not just features

<!-- When something changes, you have no way of understanding what is actually moving the needle. This leads to disappointed leadership and very sad developers. After looking at data, you're supposed to take action. But this won't be you. If you're in this class, I really challenge you to spend the next couple of weeks thinking about how we can fundamentally shift our mindsets into making our teams focus on metrics and running experiments rather than just features. -->

---

## Lagging vs Leading Metrics

### Lagging Metrics: Easy to Measure, Hard to Improve
- **What:** Past outcomes (weight, strength, churn, satisfaction)
- **Characteristics:** Unresponsive, measures outputs
- **Problem:** Shows results after it's too late to act

### Leading Metrics: Hard to Measure, Easy to Improve  
- **What:** Future predictors (calories, workouts, experiments)
- **Characteristics:** Actionable, measures inputs
- **Power:** Provides feedback on when and where to intervene

**Key Insight:** Control the inputs to influence the outputs

<!-- If you're a product scientist or data scientist, this might be very obvious to you, but for everyone else, let's define what these metrics really mean. This was really profound to me when I was working at Facebook. A lagging metric is difficult to improve, but very easy to measure. A good example might be being stronger or losing weight - we can always test how strong we are or weigh ourselves, but we can't do much about it at the time. Leading metrics are easy to change but much harder to measure - like counting calories and working out. -->

---

## The Only Leading Metric That Matters

**For RAG Development: Number of Experiments**

> "If you're feeling lost, plan to do a couple more experiments"

**Focus Areas:**
- How many experiments are we running?
- What infrastructure investments improve velocity?
- How can we brainstorm better experiment designs?

**Success Pattern:** Doing the obvious thing over and over again
- Like counting calories in vs calories out
- Boring but effective
- Way more boring than you think, but that's what success looks like

**In Practice:**
- Focus on how many experiments we're running
- What infrastructure investments improve velocity?
- How can we brainstorm better experiment designs?
- Build stronger intuition through continual experimentation

<!-- The simple example I want you to think about most in the upcoming weeks is just how many experiments are we running. A simple analogy is counting calories and burning calories and working out. On any given moment of any given day, you can count up how many calories you've eaten. If you want to gain weight, check if you've eaten enough. If you want to lose weight, check if you've eaten too much. If you want to control your weight, the only thing that matters is calories in and calories out. This is going to be way more boring than you think - doing the obvious thing over and over again - but that is often what success looks like. -->

---

## Absence Blindness: You Don't Fix What You Can't See

**Common Pattern:**
- Everyone talks about generation quality and latency
- Nobody checks if retrieval actually works
- Focus on visible problems, ignore hidden ones

**Hidden Issues We Miss:**
- Is retrieval finding relevant documents?
- Are text chunks properly extracted?
- Do embeddings match query semantics?
- Has data been extracted correctly?
- Are representations and text chunks working?

**Reality Check:** People always talk about generation and latency, but no one has ever really looked at whether the retrieval is good or bad

**Solution:** Measure retrieval before generation

<!-- You don't fix what you can't see. I see this every day with almost every client. People are always talking about generation and latency, and no one has ever really looked at whether the retrieval is good or bad, whether the representations and the text chunks are bad, or even if the data has been extracted correctly. Too many of us focus on what you can see - the generation and latency - and not the retrieval itself. This is why a lot of the focus of today's lecture is around thinking about precision and recall. -->

---

## Intervention Bias: Action Without Purpose

**The Pattern:**
- Switch between models randomly
- Add prompt tweaks everywhere
- Do things just to feel in control

**Why This Fails:**
- No specific hypothesis being tested
- No metrics to validate improvements
- "It depends on your data" - always
- Trying to feel in control vs. being in control

**The Reality:**
- Pay consultants just to hear what you hope to hear
- But the answer is always: "it depends on your data, your evaluations, and your benchmarks"

**Better Approach:** Specific interventions against specific metrics

<!-- Something else that we do too often is we just try to do things in order to feel control. We'll just switch between different models and add a couple of lines of prompts everywhere and we just want to see if anything gets better. A lot of people pay me just to tell them what they hope to hear, but that's usually not how things work. Things are very empirical. If you send me an email and pay me a couple dollars to ask whether this thing or that thing is going to work, the answer is always going to be: it depends on your data, your evaluations, and your benchmarks. It's one thing to do something because you want to feel like you're in control, versus taking specific interventions against specific metrics. -->

---

## The RAG Flywheel

**Core Principle:** Everything from search applies to RAG

### Step 1: Basic RAG Setup
Start with existing system

### Step 2: Synthetic Data Generation  
Create test questions for retrieval abilities

### Step 3: Fast Evaluations
Unit-test-like assessments (precision, recall)

### Step 4: Real-World Data
Collect actual user queries and feedback

**Goal:** Build intuition through continuous experimentation

<!-- The basic principle here is that everything that we've applied in search is incredibly relevant to how we want to do retrieval. Many of you already have a basic RAG setup, and the only thing to do next is to think about how we can bring in synthetic questions that test the system's ability to do retrieval. Then we can conduct very fast unit tests like evaluations that assess basic retrieval capabilities like precision and recall. -->

---

## Why Retrieval Evals Beat Generation Evals

### Generation Evals: Too Subjective
```
Q: "What is the powerhouse of the cell?"
A1: "Mitochondria [1]"
A2: "The powerhouse of the cell is the mitochondria, which..."
A3: "Mitochondria are organelles that..."
```
**Problem:** Which answer is "correct"? Too subjective.

<!-- For every company that I worked with that did not come from a machine learning background, they started focusing on things like subjective generation evals way too early. In the long term, language models are going to improve their ability to synthesize new data in context, but it's our responsibility to be improving things like our search and retrieval evals. If we focus on generation evals, things like factuality become very subjective and confusing. -->

### Retrieval Evals: Objective and Clear
```
Q: "What is the powerhouse of the cell?"
Expected pages: [6, 9, 13]
Retrieved pages: [6, 8, 9, 13, 15]
Recall: 3/3 = 100% ✓
Precision: 3/5 = 60%
```

<!-- If we start committing to improving precision and recall directly, now we can test things like whether lexical search, semantic search, or re-rankers can help us improve our retrieval. Instead of running tests that take minutes or hours to run, you can run tests that take seconds. They're also going to be much cheaper, and we're not going to run into issues where we wake up one Monday morning and realize an engineer has spent $1,000 on OpenAI credits to run your factuality evals. -->

---

## Retrieval Eval Benefits

**Speed & Cost**
- Seconds vs minutes/hours
- Cheap vs expensive (no LLM judge needed)
- Can run frequently vs infrequently

**Scalability**
- Hundreds/thousands of tests
- Clear pass/fail criteria
- No subjective interpretation

**Actionability**
- Test lexical vs semantic search
- Evaluate reranker impact
- Measure chunk extraction quality

<!-- As they get more expensive and take longer, we tend to run them more infrequently, and now we lose the ability to run more experiments in a shorter amount of time. As you scale to having hundreds or even thousands of tests, retrieval evals scale incredibly well, whereas generation evals and using LLM as a judge too early in the process can result in much more difficult test cycles. -->

---

## Precision and Recall Fundamentals

### Recall: Percentage of relevant documents found
```
10 correct documents exist
Retrieved 5, found 4 correct ones
Recall = 4/10 = 40%
```
**High recall:** System finds most relevant documents
**Critical when:** Facts scattered across many documents

### Precision: Percentage of retrieved documents that are relevant
```
Retrieved 10 documents
2 are actually relevant
Precision = 2/10 = 20%
```
**High precision:** System avoids irrelevant results
**Critical when:** Too much noise confuses the model

<!-- So recall is the percentage of relevant documents that are successfully retrieved. If there are 10 correct documents and we find the top five and four of them are in there, then recall is four out of 10. High recall means that the system is able to find most of the relevant documents. This is particularly important where facts are hard to find across many documents. Precision is the percentage of retrieved documents that are relevant to the query. High precision means that the system retrieves mostly relevant documents. This is important because dumber models might be more confused with irrelevant context. -->

---

## Case Study 1: Research Interview Reports

**Problem:** Consultants losing trust in AI-generated reports
- "I know 6 people liked the product, but only 3 quotes showed up"
- **Recall:** 3/6 = 50%

**The Problem in Detail:**
- Consultants do 15-30 research interviews with experts
- AI generates reports from interview data
- Customer: "I know 6 people liked the product, but only 3 quotes showed up"
- **Trust broken:** "I know there were 6. There's something wrong."

**Solution Process:**
1. Manual question-chunk dataset creation
2. Focused on preprocessing experiments (our hypothesis)
3. 3-4 experiments on preprocessing text chunks before ingestion
4. Improved recall from 50% to 90%
5. Rebuilt customer trust through data-driven examples

**Key Lesson:** Specific goals enable rapid experimentation and customer-driven test suites. Preprocessing aligned with anticipated customer queries.

<!-- I work with a company that does report generation for user interviews. These consultants do about 15 to 30 research interviews with experts. These consulting teams then request an AI generated report and what they found was that only a subset of the quotes were being found. The consultant says, "I know I asked 15 people and six of them said they really like the product. But when this report was generated, only three of them said so. I know there were six. There's something wrong." And now I don't trust the system. We had a three out of six recall. We manually built out a question chunk dataset and found that a lot of the work could be done in preprocessing. By doing three or four experiments on preprocessing text chunks before ingestion, we improved recall from 50% to 90%. -->

---

## Case Study 2: Construction Blueprint Search

**Problem:** Workers couldn't find relevant blueprints
- **Recall:** 27% for finding correct images
- Critical documents going unfound

**The Detailed Process:**
1. Built synthetic dataset of blueprint queries
2. **Hypothesis:** Better image summaries and captions needed
3. Used visual language models to create captions and descriptions
4. Applied chain of thought reasoning about blueprints
5. Generated hypothetical questions for each blueprint
6. Tested ability to recall correct document and answer questions

**Results:** 4 days, ~12 prompts, 3 models → 27% to 85% recall

**Bonus Discovery:** 20% of queries were about counting objects in blueprints
- Justified investment in bounding box models
- Applied technique to tables, documents, other artifacts

**Key Lesson:** Highly specific prompts for synthetic summary generation + domain expertise

<!-- Another example was around using AI for multimodal search and in particular searching blueprints at a construction company. Construction workers want to ask questions regarding blueprints. When we took some examples of questions, we found that we only had a 27% recall for even finding the correct image, the correct blueprint. We found that we might be able to do better if we had better image summaries. Our approach was using a visual language model to create captions and descriptions over these blueprints. In just four days of experimenting, maybe about 12 prompts and trying three models, we went from 27% recall to 85%. Once we looked at those queries, we found that 20% were around counting objects in blueprints, which justified investment in bounding box models. -->

---

## The Synthetic Data Strategy

**Before Users:** Create synthetic questions to test systems

**Benefits:**
- Test edge cases before they happen
- Build confidence in system capabilities
- Establish baseline performance metrics
- Enable rapid iteration cycles

**Simple Starting Process:**
1. Take a random text chunk
2. Ask LLM to generate a question this chunk answers
3. Verify that retrieval finds this chunk when searching the generated question
4. Now you have synthetic dataset testing chunk retrieval
5. Recall becomes a very binary metric

**Advanced Process (with user data):**
1. Use user queries as few-shot examples for generation
2. Generate chunks from queries and test retrievability
3. Use LLM as ranker to produce weak ranking labels
4. Review weak labels to get correct labels
5. Test precision and recall (correlated with real performance)

**Key Question:** Given what I know about user data, what questions could I NOT answer with current infrastructure?

<!-- Everyone talks about synthetic data, but it's not as simple as just asking an LLM for more data. The questions here revolve around how do you make an LLM create diverse and interesting datasets that reflect production traffic. If you have no query data, the simplest thing you can do is just take a random text chunk, ask a language model to generate a question that this text chunk answers, and just verify that when you do retrieval, that text chunk is recovered when you search the question that was generated. Here, recall is a very binary metric. -->

---

## Building Your First Evaluation Set

**Start Simple:**
```python
test_cases = [
    {
        "query": "How to contact Jason?", 
        "expected_chunks": ["contact_info_page_1", "about_page_3"]
    },
    {
        "query": "What is the powerhouse of the cell?",
        "expected_chunks": ["biology_chapter_6", "cell_structure_page_9"] 
    }
]

def evaluate_retrieval(query, expected_chunks):
    retrieved = retrieval_system.search(query, top_k=10)
    retrieved_ids = [chunk.id for chunk in retrieved]
    
    hits = len(set(expected_chunks) & set(retrieved_ids))
    recall = hits / len(expected_chunks)
    precision = hits / len(retrieved_ids)
    
    return recall, precision
```

## Example Prompt for Question Generation

**Domain-Specific Product Search Example:**
```
You are generating questions for product search.
Given this product description: [PRODUCT_DESCRIPTION]
Context: [OTHER_CONTEXT_ABOUT_TEXT_DATA]

Generate questions that would retrieve this product, such as:
- Comparison questions
- Pattern recognition questions  
- Feature-specific questions

Example questions: [FEW_SHOT_EXAMPLES]

Bake in domain knowledge about:
- Document types you're working with
- Common user query patterns
- Business-specific terminology
```

**Note:** In sessions 4-5, we'll use topic modeling and segmentation to understand core capabilities and question types.

<!-- We want to try to bake as much information as possible in the domain knowledge of these prompts. We want to change these prompts based on things like document types or other information. This prompt in particular is about trying to create questions that would retrieve certain products. We might want to give it a product description, some other context around the text data, and maybe some example questions. In sessions four and five, we're going to talk about using topic modeling and segmentation to really understand the core capabilities and the core questions people are asking. -->

---

## Common Pitfalls to Avoid

**1. Oversimplification**
- Don't aim for 100% recall - probably means test cases too simple
- Define dynamic datasets vs static datasets
- As scores improve, add more complex examples

**2. Neglecting Real Data**
- If you have real user data, don't neglect it
- Include it in your dataset for higher quality testing

**3. Production Misalignment** 
- Ensure search implementations match production exactly
- No misalignment in configuration or specifications
- Test what you actually ship

<!-- The first pitfall is oversimplification. You don't actually want 100% recall, because it probably means that your test cases are too simple. I want you to think about defining dynamic datasets versus static datasets. As your scores get higher, it means your models are getting better, so add more complex examples into your dataset. If you have real data, don't neglect it - make sure it's included. Also make sure that the search implementations you're using and testing are the same ones in production. Make sure there are no misalignments in how things are being configured. -->

---

## This Week's Homework

**Step 1: Audit Current State**
- How many evaluations do you currently have?
- What metrics are you tracking?
- Are they leading or lagging metrics?

**Step 2: Create Your First Eval Set**
- 10-20 query/expected-chunk pairs
- Focus on your most common use cases
- Test current retrieval performance

**Step 3: Run Your First Experiment**
- Change one thing (chunk size, embedding model, etc.)
- Measure before and after performance
- Document what you learned

**Experiment Ideas:**
- Try BM25 and full-text search (if using LanceDB/ChromaDB)
- Test different embedding models
- Experiment with chunking strategies
- Try different re-rankers (e.g., Cohere)
- Test different top-k values (10, 20, 30)
- Compare latency vs retrieval quality tradeoffs

**Important:** If experiments don't improve metrics, do nothing. Choose to do nothing rather than add tech debt.

<!-- Don't hesitate to ask me any questions during office hours or on Slack. This is what we're here to do. We can just deep dive into the problems of your application and what you're struggling with. I really want you to start thinking about creating evaluation datasets by leveraging synthetic data. If you're using something like LanceDB or ChromaDB, also check if something like BM25 and full text search can improve these systems. Review these generated questions with subject matter experts. Ask them, are these questions even relevant for the use cases? -->

---

## Next Week Preview: Fine-tuning

**Session 2 Focus:**
- When and how to fine-tune embedding models
- Building relevancy into your representations
- Moving beyond off-the-shelf solutions
- Creating custom models for your domain

**Goal:** Once you know what relevancy is, build it yourself

<!-- The focus for next week is thinking about taking this synthetic dataset, and exploring things like fine tuning, representations, and embeddings, and ultimately training re-ranker models to just give you that extra boost in precision and recall. -->

---

## Key Takeaways

### Mindset Shifts
1. **Experiments over features** - measure velocity of learning
2. **Leading over lagging metrics** - control inputs, not just outputs  
3. **Retrieval over generation** - fix what you can't see first
4. **Specific over generic** - build superpowers, not generic tools

### Action Items
1. **Count your experiments** - how many can you run this week?
2. **Build synthetic data** - before you have real users
3. **Focus on recall first** - can you find the right documents?
4. **Measure everything** - absence blindness kills RAG systems

<!-- These are the fundamental mindset shifts I want you to take away. We need to focus on experiments over features - measure the velocity of learning. Leading over lagging metrics - control inputs, not just outputs. Retrieval over generation - fix what you can't see first. Specific over generic - build superpowers, not generic tools. Count your experiments - how many can you run this week? Build synthetic data before you have real users. Focus on recall first - can you find the right documents? -->

---

## Remember: Fake It Till You Make It

**The Data Flywheel:**
- Synthetic data → Fast evaluations → Better intuition → More experiments → Better product

**Success Metrics:**
- Number of experiments run per week
- Precision and recall improvements  
- Customer trust and satisfaction growth

**Foundation First:** Build the evaluation infrastructure that will guide all future improvements

**Collection Strategy:**
- Start simple: Google Sheets for valuable labels
- Every demo, user interview, thumbs up/down = gold data
- Later: Use tools like Braintrust for programmatic collection
- Review generated questions with subject matter experts
- Ask: "Are these questions even relevant for our use cases?"

**Data Collection Mindset:** Log everything. Track questions. Create evals from every interaction.

<!-- The data flywheel is: synthetic data leads to fast evaluations, which leads to better intuition, which leads to more experiments, which leads to better product. Your success metrics should be: number of experiments run per week, precision and recall improvements, and customer trust and satisfaction growth. Build the evaluation infrastructure that will guide all future improvements. Start simple with Google Sheets for valuable labels. Every demo, user interview, thumbs up/down is gold data. Later use tools like Braintrust for programmatic collection. -->

---

## Thank You

**Questions for office hours:**
- How to generate synthetic data for your domain?
- What's a good starting number of evaluations?
- How to convince leadership to invest in metrics?

**Next week:** From measuring relevancy to building it

*maven.com/applied-llms/rag-playbook*

<!-- We're still learning who you are. As we learn everyone's technical levels, we'll be able to dig deeper in these office hours and calibrate to everyone's level. So make sure to ask questions on Slack. Remember, we're trying to establish baselines. With this, we'll be able to use the techniques we learn in sessions four, five, and six, and really start testing different interventions and seeing which ones make a real difference in our metrics. Most importantly, by using these benchmarks, we can also reject interventions - we don't have to add superstitious interventions that become tech debt too quickly. -->
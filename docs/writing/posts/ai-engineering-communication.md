---
title: "Effective Communication in AI Engineering: Moving Beyond Vague Updates"
description: "Learn how to enhance AI engineering processes through rigorous and insightful updates, focusing on hypotheses, interventions, results, and trade-offs."
categories:
  - "Applied AI"
  - "Software Engineering"
  - "Writing and Communication"
tags:
  - "AI Engineering"
  - "Communication"
  - "Project Management"
  - "Probabilistic Systems"
  - "Search Optimization"
date: 2024-10-15
comments: true
---

# The right way to do AI engineering updates

*Helping software engineers enhance their AI engineering processes through rigorous and insightful updates.*

---

After working with over a dozen startups trying to build out their AI engineering teams and helping them transition their software engineering practices to applied AI, I noticed a couple of shortcomings, there's a pressing need to adapt our communication methods to better reflect the complexities and uncertainties inherent in these systems.

In this post, we'll explore how adopting a more rigorous approach to updates—focusing on hypotheses, interventions, results, and trade-offs—can significantly improve project outcomes. We'll delve into real-world examples, highlighting successes, failures, and the invaluable lessons learned along the way. Whether you're a software engineer new to AI, a junior AI engineer, or a VP of engineering overseeing AI initiatives, this guide aims to enhance your understanding of effective communication in the realm of AI engineering.

---

## What is a bad update?

> Hey guys, I tried some of the suggestions we had last week, and the results look a lot better.

This is a bad update. It's vague. It's not helpful. It doesn't communicate what worked and what didn't.

It's a description of an activity, not a description of an experiment.

1. Adjectives mean you're hiding something. Quantify or don't even mention it.
2. Not having a clear hypothesis makes it impossible to interpret the results.
3. Subjective metrics are meaningless, when 1% could be massive or microscopic.

## What is a good update?

> I tried lexical search, semantic search, and hybrid indexing. We were able to get 85% recall at 5 and 93% recall at 10, which is about a 16% relative improvement from whats currenty deployed, Its only a few lines of code so it should be pretty cheap to roll out.

| Metric       | Baseline | Hybrid Search | Re-ranking |
|--------------|----------|---------------|------------|
| Recall @ 5   | 73%      | 85% (+16.4%)  | 88% (+20.5%) |
| Recall @ 10  | 80%      | 93% (+16.3%)  | 95% (+18.8%) |


This is a good update. It's clear what was done, the results are quantifiable, and the trade-offs are acknowledged. and came with a table to show the results, no adjectives needed.

> I tried adding a re-ranking layer. It improves results by like 3% but adds 70ms to 700ms latency to the application. Based on other things I've looked up, it might not be worth it. That said, if any of these re-ranking models were to get faster in the next couple of months, I'd definitely think we should revisit.

This is also great, even though results are lower, the trade-off is clearly understood and communicated. We even have a plan to revisit if certain conditions are met, like faster or smarter re-ranking models.


## The Challenge of Communicating

Imagine you're part of a team building an AI agent designed to provide accurate and relevant search results. Unlike traditional software systems, AI models don't always produce deterministic outcomes. They're probabilistic by nature, meaning their outputs can vary even when given the same input. This inherent uncertainty presents a unique challenge: How do we effectively communicate progress, setbacks, and insights in such an environment?

Traditional update formats—like stating what you did last week or identifying blockers—aren't sufficient. Instead, we need to shift our focus towards:

- **Hypotheses:** What do we believe will happen if we make a certain change?
- **Interventions:** What specific actions are we taking to test our hypotheses?
- **Results:** What are the quantitative outcomes of these interventions?
- **Trade-offs:** What are the benefits and costs associated with these outcomes?

---

## A New Approach, (old for many of us)

To illustrate the power of this approach, let's dive into a series of examples centered around **RAG**—a crucial aspect of building effective AI agents.

### **Scenario Setup**

Our team is enhancing a search engine's performance. We're experimenting with different search techniques:

- **Lexical Search (BM25):** A traditional term-frequency method.
- **Semantic Search:** Leveraging AI to understand the context and meaning behind queries.
- **Hybrid Indexing:** Combining both lexical and semantic searches.
- **Re-ranking Models:** Using advanced models like Cohere and RankFusion to reorder search results based on relevance.

Our primary metric for success is **Recall at 5 and at 10**—the percentage of relevant results found in the top 5 or 10 search results.

---

## **Example 1: A High-Impact Intervention**


> We implemented a hybrid search index combining BM25 and semantic search, along with a re-ranking model. Recall at 5 increased from 65% to 85%, and Recall at 10 improved from 78% to 93%. User engagement also increased by 15%. While there's a slight increase in system complexity and query processing time (~50ms), the substantial gains in performance justify these trade-offs.


| Metric       | Semantic Search | Hybrid Search | Hybrid + Re-ranking |
|--------------|-----------------|----------------|---------------------|
| Recall @ 5   | 65%             | 75% (+15.4%)   | 86% (+32.3%)        |
| Recall @ 10  | 72%             | 83% (+15.3%)   | 93% (+29.2%)        |
| Latency      | ~50ms           | ~55ms (+10%)   | ~200ms (+264%)      |

### **Hypothesis**

Integrating a **hybrid search index** combining BM25 and semantic search will significantly improve Recall at 5 and 10 since reranking after a hybrid search will provide better ranking

### **Intervention**

- **Action:** Developed and implemented a hybrid search algorithm that merges BM25's lexical matching with semantic embeddings.
- **Tools Used:** Employed Cohere's re-ranking model to refine the search results further.

### **Results**

- **Recall at 5:** Increased from **65% to 85%** (a 20% absolute improvement).
- **Recall at 10:** Improved from **72% to 93%** (a 21% absolute improvement).
- **User Engagement:** Time spent on the site increased by **15%**, indicating users found relevant information more quickly.

### **Trade-offs**

- **Complexity:** Moderate increase in system complexity due to the integration of multiple search techniques.
- **Computational Cost:** Slight increase in processing time per query (~50ms additional latency).

### **Conclusion**

The substantial improvement in recall metrics and positive user engagement justified the added complexity and computational costs. This intervention was definitely worth pursuing.

---

## **Example 2: When Small Gains Aren't Worth It**


> We experimented with a query expansion technique using a large language model to enhance search queries. While this approach showed promise in certain scenarios, the overall impact on recall metrics was mixed, and it introduced significant latency to our search system.

| Metric       | Baseline | Query Expansion |
|--------------|----------|-----------------|
| Recall @ 5   | 85%      | 87% (+2.4%)     |
| Recall @ 10  | 93%      | 94% (+1.1%)     |
| Latency      | ~200ms   | ~1800ms (+800%)  |



### **Hypothesis**

Implementing query expansion using a large language model will enhance search queries and improve recall metrics, particularly for complex or ambiguous queries.

### **Intervention**

- **Action:** Implemented query expansion using a large language model to enhance search queries.
- **Objective:** Improve recall metrics, particularly for complex or ambiguous queries.

### **Results**

- **Recall at 5:** Improved from **85% to 87%** (2% absolute improvement).
- **Recall at 10:** Improved from **93% to 94%** (1% absolute improvement).
- **Processing Time:** Increased latency from **~200ms to ~1800ms** (800% increase).
- **System Complexity:** Significant increase due to the integration of a large language model for query expansion.

### **Trade-offs**

- **Marginal Gains:** The slight improvement in recall did not justify the substantial increase in latency.
- **Performance Overhead:** The significant increase in latency could severely impact user satisfaction.
- **Maintenance Burden:** Higher complexity makes the system more difficult to maintain and scale.
- **Resource Consumption:** Integrating a large language model requires additional computational resources.

### **Conclusion**

Despite the modest improvements in recall metrics, the substantial increase in latency and system complexity made this intervention impractical. The potential negative impact on user experience due to increased response times outweighed the marginal gains in search accuracy. Therefore, we decided not to proceed with this intervention. 

If smaller models become faster and more accurate, this could be revisited.

---

## **Embracing Failure as a Learning Tool**

We should also embrace failure as a learning tool, its not a waste of time as it has helped you refine your approach, your knowledge, and your systems and where not to go.

I also like updates to include examples of before and after the interfectinos when possible to show the impact. As well as examples of failures and what was learned from them.

### Example

> We experimented with a query expansion technique using a large language model to enhance search queries. While this approach showed promise in certain scenarios, the overall impact on recall metrics was mixed, and it introduced significant latency to our search system. Here some examples of before and after the intervention.

```python
print(expand_v1("Best camera for low light photography this year ")
{
   "category": "Camera",
   "query": "low light photography",
   "results": [
      "Sony Alpha a7 III",
      "Fujifilm X-T4"
   ]
}
print(expand_v2("Best camera for low light photography")
{
   "query": "low light photography",
   "date_start": "2024-01-01",
   "date_end": "2024-12-31",
   "results": [
      "Sony Alpha a7 III",
      "Fujifilm X-T4"
   ]
}
```

We found that these expansion modes over dates did not work successfully because we're missing metadata around when cameras were released. Since we review things that occur later than their release, this lack of information has posed a challenge. For this to be a much more fruitful experiment, we would need to improve our coverage, as only 70% of our inventory has date or time metadata.

These examples and insights demonstrate the value of embracing failure as a learning tool in AI engineering. By documenting our failures, conducting regular reviews, and using setbacks as fuel for innovation, we can extract valuable lessons and improve our systems over time. To further illustrate how this approach can be implemented effectively, let's explore some practical strategies for incorporating failure analysis into your team's workflow

1. **Document Your Failures:**
   - Maintain a "Failure Log" to record each unsuccessful experiment or intervention.
   - Include the hypothesis, methodology, results, and most importantly, your analysis of why it didn't work.
   - This practice helps build a knowledge base for future reference and learning.

2. **Conduct Regular Failure Review Sessions:**
   - Schedule monthly "Failure Retrospectives" for your team to discuss recent setbacks.
   - Focus these sessions on extracting actionable insights and brainstorming ways to prevent similar issues in future projects.
   - Encourage open and honest discussions to foster a culture of continuous improvement.

3. **Use Failure as Innovation Fuel:**
   - Encourage your team to view failures as stepping stones to breakthrough innovations.
   - When an experiment fails, challenge your team to identify potential pivot points or new ideas that emerged from the failure.
   - For example, if an unsuccessful attempt at query expansion leads to insights about data preprocessing, explore how these insights can be applied to improve other areas of your system.

---

## **Effective Communication Strategies for Probabilistic Systems**

### **Tips for Engineers and Leaders**

1. **Emphasize Hypotheses:**
   - Clearly state what you expect to happen and why.
   - Example: "We hypothesize that integrating semantic search will improve recall metrics by better understanding query context."

2. **Detail Interventions:**
   - Explain the specific actions taken.
   - Example: "We implemented Cohere's re-ranking model to refine search results after the initial query processing."

3. **Present Quantitative Results:**
   - Use data to showcase outcomes.
   - Example: "Recall at 5 improved from 65% to 85%."

4. **Discuss Trade-offs:**
   - Acknowledge any downsides or costs.
   - Example: "While we saw performance gains, processing time increased by 50ms per query."

5. **Be Honest About Failures:**
   - Share what didn't work and potential reasons.
   - Example: "Our attempt at personalization didn't yield results due to insufficient user data."

6. **Recommend Next Steps:**
   - Provide guidance on future actions.
   - Example: "We recommend revisiting personalization once we have more user data."

7. **Visual Aids:**
   - Use before-and-after comparisons to illustrate points.
   - Include charts or tables where appropriate.

---

## **Conclusion**

Building and improving AI systems is an iterative journey filled with uncertainties and learning opportunities. By adopting a rigorous approach to updates—focusing on hypotheses, interventions, results, and trade-offs—we can enhance communication, make better-informed decisions, and ultimately build more effective AI agents.

For software engineers transitioning into AI roles, junior AI engineers honing their skills, and VPs overseeing these projects, embracing this communication style is key to navigating the complexities of probabilistic systems. It fosters transparency, encourages collaboration, and drives continuous improvement.

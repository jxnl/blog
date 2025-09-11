# Chapter 4 Slides

## jxnl.co

@jxnlco

<!-- Welcome to Session 4 of Systematically Improving RAG Applications. This is my favorite session because it's where we get into the real meat of systematic improvement. Today we're talking about splitting - when to double down on capabilities that are working versus when to fold and abandon segments that aren't worth the investment. This is post-production analysis at its finest. -->

## Systematically Improving RAG Applications

**Session 4:** Split: When to Double Down vs When to Fold

Jason Liu

---

## My Favorite Session! 🎯

**Today's Focus:** Data segmentation and strategic decision-making

**Key Questions:**
- How do we segment user data and queries?
- When should we double down on capabilities?
- When should we fold and abandon segments?
- How do we allocate resources effectively?

**This is the actual playbook for post-production analysis**

<!-- This really is my favorite session because it transforms vague product management into data-driven decision making. We're going to answer fundamental questions: How do we segment user data and queries systematically? When should we double down on capabilities that are working? When should we fold and abandon segments that aren't worth the investment? How do we allocate resources effectively based on data rather than intuition? This is the actual playbook I use with clients for post-production analysis. -->

---

## RAG Flywheel Recap

**Where we've been (Sessions 1-3):**

1. **Initial RAG System** - Basic implementation in place
2. **Synthetic Data Generation** - Create test questions for retrieval evaluation  
3. **Fast Evaluations** - Precision, recall, ranking improvements
4. **User Interaction Data** - Collect feedback through better UI
5. **Fine-Tuning** - Embedding models and rerankers
6. **Production Deployment** - Reasonable product ready to deploy

**Today:** What do we do post-production with lots of data?

<!-- Let's recap where we've been. In sessions 1-3, we built the foundation: initial RAG system, synthetic data generation for test questions, fast evaluations focused on precision and recall, user interaction data collection through better UI design, fine-tuning of embedding models and rerankers, and finally production deployment of a reasonable product. Now you have a system in production collecting data. Today's question is: what do we do post-production when we have lots of data flowing in? This is where the real systematic improvement begins. -->

---

## Post-Production Data Analysis

**The Challenge:** You have plenty of data coming in - now what?

**Our Approach:**
- **Segmentation and Analysis** - Figure out what's missing and where blind spots are
- **Identify Improvements** - Understand what segments need targeted work
- **Specialized Systems** - Build specific tools for high-value segments  
- **Function Calling Integration** - Combine tools into unified system
- **Query Routing** - Ensure right retriever for each job

**This is where the real value gets unlocked!**

<!-- The challenge every team faces post-production is: you have plenty of data coming in, but now what? How do you systematically analyze and act on it? Our approach has five components: First, segmentation and analysis to figure out what's missing and where your blind spots are. Second, identify specific improvements by understanding what segments need targeted work. Third, build specialized systems and specific tools for high-value segments. Fourth, function calling integration to combine tools into a unified system. Finally, query routing to ensure the right retriever handles each job. This is where the real value gets unlocked - not in the initial deployment, but in systematic post-production improvement. -->

---

## Why Segmentation Matters

### Marketing Example: The 80% Sales Boost

**Scenario:** Consumer product marketing campaign → 80% sales increase

**Without Segmentation:**
- "Sales went up 80%!" 🤷‍♂️
- No actionable insights
- Can't replicate success

**With Segmentation:**
- 60% of increase from **30-45 year old women in Midwest**
- **Actionable insight:** Target this demographic more
- **Strategy shift:** Midwest podcasts vs Super Bowl ads
- **Resource allocation:** Focus where results happen

<!-- Let me give you a concrete example of why segmentation matters. Imagine a consumer product marketing campaign that produces an 80% sales increase. Without segmentation, all you can say is "Sales went up 80%!" There are no actionable insights and you can't replicate the success. But with segmentation, you discover that 60% of the increase came from 30-45 year old women in the Midwest. Now you have actionable insights - target this demographic more. This leads to strategy shifts - invest in Midwest podcasts instead of expensive Super Bowl ads. Resource allocation becomes focused where actual results happen. This is the power of segmentation - turning aggregate success into targeted action. -->

---

## Stitch Fix Segmentation Example

**The Discovery:**
- 10% of customer base → 60% of sales volume
- 40% of customer base → 10% of sales volume

**Strategic Decisions:**
- **Double Down:** Invest more in high-performing Segment 1
- **Investigate:** Why is Segment 1 outperforming?
- **Fold:** Stop onboarding low-performing segments
- **Reallocate:** Resources to better performing segments

**Same thinking applies to your queries!**

<!-- Here's a real example from my time at Stitch Fix. We discovered that 10% of our customer base was driving 60% of our sales volume, while 40% of our customer base was only driving 10% of sales volume. This led to clear strategic decisions: Double down by investing more in the high-performing segment. Investigate why Segment 1 was outperforming - what made them different? Fold by stopping onboarding of the low-performing segments. Reallocate resources to the better performing segments. This same thinking applies exactly to your RAG queries. Some query types will drive disproportionate value, and you need to systematically identify and double down on those while folding on the rest. -->

---

## Applying Segmentation to RAG

**Query Performance Patterns:**
- **Amazing Performance** - Queries to highlight and showcase
- **Good Performance** - Queries to double down on and target
- **Poor Performance** - Queries needing targeted improvements
- **Lost Causes** - Queries to abandon (not worth the investment)

**Segmentation Dimensions:**
- Role or organization ID
- Customer cohort or lifecycle stage  
- Psychographics (attitudes, values, interests)
- Query embeddings and summaries
- Chat history patterns

<!-- Applying this to RAG, you'll find query performance patterns that map directly to business decisions. Amazing performance queries should be highlighted and showcased - these are your success stories. Good performance queries you should double down on and target for expansion. Poor performance queries need targeted improvements - these are investment opportunities. Lost causes should be abandoned because they're not worth the continued investment. You can segment along multiple dimensions: role or organization ID, customer cohort or lifecycle stage, psychographics like attitudes and interests, query embeddings and summaries, and chat history patterns. The key is finding the dimensions that actually correlate with performance differences. -->

---

## Query Tagging and Classification

**Example Query:** "What's the difference between 2022 vs 2023 budgets?"

**Automatic Tags:**
- `time_filter_required`
- `multiple_queries_needed` 
- `financial_domain`
- `comparative_analysis`

**Analysis Opportunities:**
- Group by time queries → frequency analysis
- Customer satisfaction by query type
- Performance differences across segments
- Resource allocation decisions

<!-- Query tagging and classification is where the magic happens. Take this example: "What's the difference between 2022 vs 2023 budgets?" You can automatically tag this with time_filter_required, multiple_queries_needed, financial_domain, and comparative_analysis. Now you have analysis opportunities: group all time-based queries and do frequency analysis, measure customer satisfaction by query type, identify performance differences across segments, and make data-driven resource allocation decisions. The tags become the dimensions for your segmentation analysis. -->

---

## The Segmentation Formula

### Expected Value Equation

```
Expected Value = Σ (Impact × Percentage of Queries × Probability of Success)
                 across all segments
```

**Where:**
- **Impact** = Economic value of solving this query type
- **Percentage of Queries** = How often this segment occurs  
- **Probability of Success** = How well your system handles it

**This is how you improve your application systematically!**

<!-- This formula is the mathematical foundation of systematic improvement. Expected value equals the sum across all segments of impact times percentage of queries times probability of success. Impact is the economic value of solving this query type - some queries matter more for business outcomes. Percentage of queries is how often this segment occurs in your traffic. Probability of success is how well your current system handles it. This formula tells you exactly where to focus your engineering effort for maximum business impact. This is how you improve your application systematically instead of randomly. -->

---

## Understanding the Levers

### Impact (Economic Value)
- **Revenue generation potential**
- **Cost savings from automation**
- **User satisfaction correlation**
- **Strategic business importance**

*Usually determined by user feedback and research*

### Percentage of Queries (Volume)
- **UX design decisions**  
- **User education and onboarding**
- **Feature discoverability**
- **Customer behavior patterns**

*You have some control here through product decisions*

<!-- Understanding the levers in this formula is crucial for strategic thinking. Impact or economic value includes revenue generation potential, cost savings from automation, user satisfaction correlation, and strategic business importance. This is usually determined by user feedback and research - you need to talk to customers to understand what really matters. Percentage of queries or volume is influenced by UX design decisions, user education and onboarding, feature discoverability, and customer behavior patterns. The key insight is you have some control here through product decisions - you can drive traffic toward high-value query types. -->

---

## Understanding the Levers (continued)

### Probability of Success (Performance)
- **Generation quality**
- **Citation accuracy**
- **Text chunk relevance**  
- **User upvote correlation**
- **Task completion rates**

*This is what you optimize through technical improvements*

**Key Insight:** Build specialized systems to maximize each segment's probability of success!

<!-- Probability of success or performance includes generation quality, citation accuracy, text chunk relevance, user upvote correlation, and task completion rates. This is what you optimize through technical improvements - better embeddings, improved reranking, fine-tuned models. The key insight is to build specialized systems to maximize each segment's probability of success. Don't try to optimize everything globally - build segment-specific solutions that excel at particular query types. This is where the real performance gains come from. -->

---

## Practical Implementation

### Step 1: Clustering and Classification
- **Clustering models** for initial query grouping
- **Few-shot classifiers** for conversation analysis
- **Batch processing** for historical data
- **Online classification** for real-time segmentation

### Step 2: Monitoring and Analysis
- Track segment performance over time
- Historical trend analysis
- Success rate by segment
- Resource allocation tracking

<!-- For practical implementation, start with clustering and classification. Use clustering models for initial query grouping to discover natural patterns in your data. Build few-shot classifiers for conversation analysis - these are surprisingly effective with good prompt engineering. Do batch processing for historical data to establish baselines. Implement online classification for real-time segmentation of incoming queries. Then focus on monitoring and analysis: track segment performance over time, do historical trend analysis, measure success rates by segment, and track resource allocation to ensure you're investing where you get returns. -->

---

## The Strategic Decision Framework

### For Each Segment, Ask:

**1. Double Down (High Value)**
- High impact × High volume × Improving success rate
- **Action:** Invest more resources, build specialized tools

**2. Investigate (High Potential)** 
- High impact × High volume × Low success rate
- **Action:** Research why it's failing, targeted improvements

**3. Optimize (Steady Performance)**
- Medium impact × Medium volume × Good success rate  
- **Action:** Incremental improvements, maintain quality

**4. Fold (Not Worth It)**
- Low impact × Low volume × Poor success rate
- **Action:** Stop investing, redirect users, abandon segment

---

## Real-World Segmentation Examples

### Query Type Segments
- **Simple Factual** ("What is X?") - High volume, high success
- **Complex Analysis** ("Compare X vs Y over time") - High value, needs work
- **Procedural** ("How do I do X?") - Medium value, good performance  
- **Ambiguous** ("Tell me about stuff") - Low value, poor performance

### Business Context Segments  
- **Sales Team** queries - High business impact
- **Support Team** queries - High volume, cost savings
- **Executive** queries - Low volume, strategic importance
- **General Employee** queries - High volume, mixed value

---

## Success Metrics by Segment

### Technical Metrics
- **Retrieval accuracy** (precision/recall by segment)
- **Response relevance** (human evaluation scores)
- **Citation quality** (verifiable sources percentage)
- **Latency** (response time by complexity)

### Business Metrics
- **Task completion rate** (user achieved their goal)
- **User satisfaction** (thumbs up/down by segment) 
- **Return usage** (came back to ask more questions)
- **Escalation rate** (had to ask human for help)

---

## Implementation Tools and Techniques

### Clustering Approaches
```python
# Semantic clustering of queries
embeddings = embed_queries(query_list)
clusters = KMeans(n_clusters=10).fit(embeddings)

# Topic modeling for themes
topics = LatentDirichletAllocation(n_topics=15).fit(query_texts)
```

### Classification Systems
```python
# Few-shot classification for segments
classifier = FewShotClassifier(
    examples={
        "financial": ["budget", "cost", "revenue queries..."],
        "technical": ["how to", "configure", "troubleshoot..."], 
        "comparative": ["vs", "difference", "compare..."]
    }
)
```

---

## Resource Allocation Strategy

### High-Impact, High-Volume Segments
- **Dedicated engineering team**
- **Specialized embedding models**  
- **Custom retrieval systems**
- **Advanced reranking**

### Medium-Impact Segments
- **Shared engineering resources**
- **Configuration-based improvements**
- **A/B testing optimization**

### Low-Impact Segments  
- **Automated improvements only**
- **User education to redirect**
- **Consider deprecation**

---

## Common Segmentation Mistakes

### ❌ Avoid These Pitfalls

**Over-Segmentation**
- Too many micro-segments
- Analysis paralysis
- Resource fragmentation

**Under-Segmentation**  
- "One size fits all" approach
- Missing optimization opportunities
- Poor resource allocation

**Static Segmentation**
- Set it and forget it
- Missing evolving patterns
- Outdated assumptions

---

## Case Study: Query Performance Matrix

| Segment | Volume | Success Rate | Impact | Action |
|---------|--------|-------------|---------|---------|
| Financial Reports | 25% | 45% | High | 🔧 **Investigate & Fix** |
| Simple Q&A | 40% | 85% | Medium | 📈 **Double Down** |
| Code Debugging | 15% | 60% | High | 🎯 **Targeted Improvement** |
| Random Chat | 20% | 30% | Low | 🗑️ **Fold/Redirect** |

**Insight:** Focus engineering on Financial Reports (high impact, fixable), maintain Simple Q&A (working well), and redirect Random Chat users.

<!-- This case study shows the framework in action. Financial Reports has 25% volume, 45% success rate, high impact - this is a clear "Investigate & Fix" case. High impact but fixable performance issues. Simple Q&A has 40% volume, 85% success rate, medium impact - "Double Down" because it's working well and has good volume. Code Debugging has 15% volume, 60% success rate, high impact - "Targeted Improvement" because the impact is high even though volume is lower. Random Chat has 20% volume, 30% success rate, low impact - "Fold/Redirect" because resources are better spent elsewhere. The insight: focus engineering on Financial Reports where you can get high impact wins, maintain Simple Q&A that's already working, and redirect Random Chat users to more valuable interactions. -->

---

## Building Your Segmentation System

### Phase 1: Discovery (Week 1-2)
1. **Collect query logs** for 2-4 weeks minimum
2. **Manual labeling** of 200-500 queries  
3. **Initial clustering** to identify patterns
4. **Stakeholder interviews** for impact assessment

### Phase 2: Classification (Week 3-4)
1. **Build classification system** (few-shot or fine-tuned)
2. **Validate accuracy** on held-out set
3. **Process historical data** for baseline metrics
4. **Create monitoring dashboard**

### Phase 3: Action (Week 5-8)
1. **Prioritize segments** using impact/volume/success matrix
2. **Allocate engineering resources** to high-priority segments  
3. **Implement targeted improvements**
4. **Measure improvement and iterate**

---

## Key Questions for Your Team

### Strategic Questions
1. What are our top 5 query segments by volume?
2. Which segments have highest business impact?
3. Where are our biggest success rate gaps?
4. What segments should we abandon?

### Tactical Questions  
1. How do we automatically classify incoming queries?
2. What specialized tools does each segment need?
3. How do we measure success for each segment?
4. How often should we re-evaluate segments?

---

## Success Indicators

### You're Doing Segmentation Right When:

- **Teams have data-driven debates** about resource allocation
- **"Make AI better"** becomes **"Improve financial query segment"**
- **Engineering roadmap** aligns with segment priorities  
- **Business metrics improve** for targeted segments
- **User satisfaction** increases in focus areas
- **Resource waste decreases** on low-value segments

### Red Flags:
- Still making improvements randomly
- Can't explain why you're working on X vs Y  
- No clear success metrics by segment
- Equal effort on all query types

---

## Next Week Preview

**Session 5: Map - Navigating Multimodal RAG**

**Now that you know WHICH segments to focus on...**
- How do we build specialized systems for high-value segments?
- Multimodal retrieval (documents, images, tables, code)
- Contextual retrieval and summarization techniques
- System improvements targeting specific segments

**Come prepared with your segment analysis!**

---

## Homework: Segment Your Data

### This Week's Assignment

1. **Collect Queries** - Gather 2-4 weeks of user queries
2. **Manual Analysis** - Label 100-200 queries by type/theme  
3. **Initial Clustering** - Use embeddings to find natural groupings
4. **Impact Assessment** - Interview stakeholders about query value
5. **Performance Baseline** - Measure current success rates by segment

### Deliverable
- **Segment prioritization matrix** with volume, impact, and success rates
- **Top 3 segments** for targeted improvement
- **Bottom 2 segments** for potential abandonment

**This analysis will guide the rest of the course!**

<!-- Your homework this week is to segment your own data. Collect 2-4 weeks of user queries - you need volume for meaningful analysis. Do manual analysis by labeling 100-200 queries by type and theme - this gives you ground truth. Use embeddings to find natural groupings through clustering. Interview stakeholders about query value - don't assume you know what matters. Measure current success rates by segment to establish baselines. Your deliverable is a segment prioritization matrix with volume, impact, and success rates, plus identification of your top 3 segments for targeted improvement and bottom 2 segments for potential abandonment. This analysis will literally guide the rest of the course - it determines what specialized systems you'll build in sessions 5 and 6. -->

---

## Key Takeaway

> **Stop trying to make "the AI" better. Start making specific segments better.**

The magic happens when you:
1. **Identify** what's actually valuable to your users
2. **Focus** engineering effort on high-impact segments  
3. **Abandon** segments that aren't worth the investment
4. **Measure** improvements segment by segment

**Segmentation turns RAG from art into science! 🎯**

<!-- This is the key takeaway from today's session: Stop trying to make "the AI" better. Start making specific segments better. The magic happens when you identify what's actually valuable to your users through data analysis, focus engineering effort on high-impact segments based on the expected value formula, abandon segments that aren't worth the investment - this takes courage but it's essential, and measure improvements segment by segment rather than looking at global metrics. Segmentation turns RAG from art into science. It transforms vague product management into data-driven decision making. This is how you systematically improve RAG applications. -->
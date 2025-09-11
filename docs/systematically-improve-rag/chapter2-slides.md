# Chapter 2 Slides

## jxnl.co

@jxnlco

## Systematically Improving RAG Applications

**Session 2:** If You're Not Fine-Tuning, You're Blockbuster, Not Netflix

Jason Liu

<!-- 
Emphasize the urgency here - this is about seizing a competitive advantage while it still exists. The "Blockbuster vs Netflix" analogy is crucial - companies that don't adapt to new ML capabilities will be left behind. What used to require hundreds of thousands of dollars and large teams can now be done by individuals with a few hundred dollars of API calls. This window of opportunity won't last forever.
-->

---

## Today's Goals

**From Measuring Relevancy to Building It**

- Understand why off-the-shelf embeddings fail
- Learn the fundamentals of similarity and objective functions
- Build custom embeddings with synthetic data
- Master fine-tuning techniques for retrieval systems
- Start logging relevancy data for continuous improvement

**Focus: Train models that understand YOUR definition of relevance**

<!-- 
Key message: We're not fine-tuning language models (those are expensive and hard). We're fine-tuning embedding models - much easier and cheaper. The goal is to improve retrieval, not generation. This is the fundamental shift companies need to make.
-->

---

## Course Overview Reminder

### Sessions 1-3: Foundation Building
- **Session 1:** Synthetic data and evaluations  
- **Session 2:** Fine-tuning embeddings and representations ← Today
- **Session 3:** User experience and data collection

### Sessions 4-6: Advanced Optimization
- **Session 4:** Query segmentation and topic modeling
- **Session 5:** Multiple indices and multimodal search
- **Session 6:** Query routing and system integration

**Core Pattern:** Synthetic data → Evaluations → Fine-tuning → Better products

<!-- 
This is the foundation for everything. Sessions 1-3 build the core flywheel that makes everything else possible. Without this foundation, all the advanced techniques in sessions 4-6 won't work effectively. This pattern will repeat at different scales throughout the course.
-->

---

## The Fundamental Problem with Off-the-Shelf Embeddings

**The Big Assumption:**
> "Query embedding should be similar to text chunk embedding"

**But similar according to whom?**

**Example: E-commerce "Red Shirt" Query**
- More red shirts? (color similarity)
- Different materials? (silk vs polyester)
- Same style, different colors? (crew neck vs v-neck)
- Complementary items? (pants, shoes, bags for complete outfit)

**All could be "correct" - depends on your business objective**

<!-- 
This is the core insight Jason has been thinking about for 4 years from his image-based recommendation systems work. The key point: similarity is not objective - it depends entirely on your business objective. OpenAI embeddings were trained on web-scale text similarity, but that may not match your specific use case. This is why off-the-shelf embeddings fail.
-->

---

## The Similarity Definition Problem

### RAG Use Case Assumption
```
distance(query_embedding, chunk_embedding) = relevance
```

### E-commerce Use Case Assumption  
```
distance(user_embedding, product_embedding) = purchase_probability
```

### But what about:
- **Product → Product:** Substitutes or complements?
- **Song → Song:** Same playlist, same artist, same BPM?
- **User → Song:** Will listen, will like, will save?

**Issue:** We're assuming what distance correlates with, without training for our specific objective

<!-- 
This is the fundamental problem. We're making assumptions about what cosine distance means without actually training for our specific objective. Third-party embedding models bake in assumptions about similarity that may not match your use case. You need to decide what the objective function really is.
-->

---

## Real-World Example: Dating App Similarity

**Scenario:** Two profiles with different coffee preferences

```
Profile 1: "I love coffee"
Profile 2: "I hate coffee"
```

**Should these be similar or different?**

1. **Different:** People with opposite preferences won't match
2. **Similar:** Both express strong food/drink preferences  
3. **Context-dependent:** Coffee lover + tea lover might work

**The Point:** Linguistic similarity ≠ Business objective similarity

<!-- 
This dating app example perfectly illustrates the problem. From a linguistic perspective, "I love coffee" and "I hate coffee" are opposites. But for a dating app, they might both indicate food/drink preferences, or coffee lovers might actually work well with tea lovers. The business objective determines what similarity means, not linguistic similarity.
-->

---

## Why Third-Party Embeddings Fail

**The Core Issue:**
- **Their training data:** Web-scale text similarity
- **Your business need:** Domain-specific relevance

**Examples of Misalignment:**
- Medical documents: "neither" vs "nor" confusion
- Legal text: Contract signed vs unsigned
- Technical docs: Version differences matter
- Customer queries: Intent vs literal meaning

**Solution:** Train embeddings on YOUR definition of similarity

<!-- 
Jason emphasizes this is about domain-specific relevance vs web-scale text similarity. Medical documents might confuse "neither" vs "nor", legal contracts care about signed vs unsigned, technical docs care about version differences. The solution is training embeddings that understand YOUR specific definition of similarity.
-->

---

## The Data Collection Imperative

> "Start logging relevancy data now, or wait 6 months for an ML engineer to do nothing"

**What to Log:**
- Query and retrieved chunks
- User interactions (clicks, saves, ignores)
- Explicit feedback (thumbs up/down)
- Citation patterns in generated responses
- **Critical:** Start logging TODAY, or wait 6 months for ML engineer to do nothing

**The Reality:** I've seen companies hire ML engineers only to realize they didn't start logging. Now they wait 3-6 months for data.

**Simple Approach:**
```python
# Save top 20-40 chunks per query
retrieved_chunks = search(query, top_k=40)
relevance_labels = llm_judge(query, retrieved_chunks)
# Later: Fine-tune to move relevant items from position 20 → 5
# Goal: More context efficient, better understanding of relevance
```

<!-- 
Jason's personal experience: he's seen companies hire ML engineers only to realize they didn't start logging data. Now they wait 3-6 months for data collection. This is a critical mistake. Start logging TODAY - query, retrieved chunks, user interactions, citations. The key insight: move relevant content from position 20 to position 5 for better context efficiency.
-->

---

## The Modern Fine-Tuning Opportunity

**Historical Context:**
- **Old way:** Hire labeling teams ($100k+), wait months for data
- **New way:** LLM-generated labels in hours ($100s)
- **Game changer:** What used to require large teams is now accessible to individuals

**Current State:**
- Most systems at 70% performance (not 99%!)
- 70% → 85% → 90% is achievable with modest effort
- Sentence Transformers: 6-10% improvement with 6,000 examples
- Fine-tune on laptop in 40 minutes
- **Reality:** Hard to go 99% → 99.9%, easy to go 70% → 85%

**The Opportunity:** What used to cost hundreds of thousands now costs hundreds
- Before: Pay data labeling teams hundreds of thousands per year
- Now: Couple hundred dollars of API calls
- **Seize this while it's still a competitive advantage**

<!-- 
This is Jason's core message about urgency. What used to be accessible only to large companies with massive budgets is now available to small teams and individuals. This is the Netflix vs Blockbuster moment - seize this opportunity while it's still a competitive advantage. Many systems are at 70% performance, not 99%. Going from 70% → 85% → 90% is achievable with modest effort. Sentence Transformers can give 6-10% improvement with just 6,000 examples, fine-tuned on a laptop in 40 minutes.
-->

---

## Fine-Tuning Fundamentals: Contrastive Learning

**The Triplet Approach:**
```
Anchor (Query): "How to set up authentication?"
Positive: Actual auth setup documentation
Negative: Unrelated deployment docs
```

**Training Objective:**
- **Pull together:** Anchor + Positive examples  
- **Push apart:** Anchor + Negative examples
- **Learn:** Custom objective that captures YOUR customer relevance

**Real Impact:** Move relevant content from position 20 → position 5
**Use Cases:** Tool selection, retrieval, any similarity-based system
**Reference:** Check out Ramp's engineering article on this approach

**Result:** Model learns your specific definition of relevance

<!-- 
The triplet approach is fundamental to contrastive learning. Pull together anchor + positive examples, push apart anchor + negative examples. This can be used for tool selection, retrieval, any similarity-based system. Reference Ramp's engineering article as a good case study of this approach in production.
-->

---

## Visual: Before and After Fine-Tuning

### Before Fine-Tuning
```
Query Vector: [0.1, 0.5, 0.3]
├── Irrelevant (close): [0.2, 0.4, 0.3] ← Problem!
├── Relevant (far): [0.8, 0.1, 0.9]   ← Problem!
```

### After Fine-Tuning  
```
Query Vector: [0.1, 0.5, 0.3]
├── Relevant (close): [0.1, 0.5, 0.4]    ← Fixed!
├── Irrelevant (far): [0.9, 0.1, 0.1]    ← Fixed!
```

**Impact:** Relevant content moves from position 20 → position 5

<!-- 
This visual shows the core problem and solution. Before fine-tuning: irrelevant content is close, relevant content is far. After fine-tuning: relevant content is close, irrelevant content is far. This directly improves context efficiency and reduces hallucinations.
-->

---

## Types of Training Data

### Pairs (Query → Relevant Document)
```python
pairs = [
    ("How to deploy?", "deployment_guide.md"),
    ("Authentication setup", "auth_config.md")
]
```

### Triplets (Query → Positive + Negative)
```python
triplets = [
    {
        "anchor": "How to deploy?",
        "positive": "deployment_guide.md", 
        "negative": "marketing_copy.md"
    }
]
```

**Negative Selection Strategies:**
- Documents retrieved but not cited
- Random sampling from corpus  
- Hard negatives (similar but wrong)

<!-- 
Negative selection is crucial. Documents retrieved but not cited make great negative examples. Hard negatives (similar but wrong) are particularly valuable for training robust models. The quality of negatives often determines training success.
-->

---

## Synthetic Data for Fine-Tuning

**Same Principle from Session 1, New Application:**

### Traditional Approach
```
Query: "What is authentication?"
Expected Chunk: auth_docs_page_5
```

### Fine-Tuning Approach  
```python
training_examples = [
    {
        "query": "How to configure OAuth?",
        "positive": embedding_model(oauth_documentation),
        "negative": embedding_model(database_setup_docs)
    }
]
```

**Scaling Pattern (The "Wax On, Wax Off" Pattern):**
- 20 examples → Evaluation dataset
- 200 examples → Few-shot prompts  
- 2,000 examples → Fine-tuning dataset

**Key Insight:** Same synthetic data, different applications at different scales
- It's never "done" - it's just "better"
- Continuous cycle of improvement
- Same data serves multiple purposes as you scale

<!-- 
This is the "Wax On, Wax Off" pattern Jason keeps referring to. The same synthetic data serves different purposes at different scales: 20 examples become evaluations, 200 examples become few-shot prompts, 2,000 examples become fine-tuning datasets. It's a continuous cycle - never "done", just "better". This pattern will repeat throughout the entire course.
-->

---

## Model Types and Selection

### Bi-Encoders (Fast Retrieval)
```python
# Encode once, search many times
query_embedding = model.encode(query)
doc_embeddings = model.encode(documents)  # Pre-computed
similarities = cosine_similarity(query_embedding, doc_embeddings)
```
**Examples:** Sentence-BERT, BGE, E5

### Cross-Encoders (Accurate Reranking)
```python
# Encode query+document pairs
for doc in top_k_candidates:
    score = model.encode(f"{query} [SEP] {doc}")
```
**Examples:** Cohere Rerank, MS Marco Cross-Encoders

**Best Practice:** Bi-encoder for retrieval + Cross-encoder for reranking

<!-- 
Understand the tradeoff: Bi-encoders are fast (encode once, search many times) but less accurate. Cross-encoders are more accurate but slower (encode query+document pairs). Best practice is using bi-encoders for initial retrieval, then cross-encoders for reranking the top candidates.
-->

---

## Practical Fine-Tuning Strategy

### Step 1: Start with Reranking
- **Why:** Don't need to re-embed existing data
- **How:** Retrieve top-40, rerank to top-10
- **Tool:** Cohere Rerank API with fine-tuning

### Step 2: If Needed, Fine-Tune Embeddings
- **When:** You have 1000+ training examples
- **Models:** BGE, E5, Sentence Transformers
- **Result:** Replace OpenAI embeddings entirely
- **Caution:** If you already have lots of embedded data, may not be worth re-embedding
- **Alternative:** Retrieve more chunks, pass to reranker instead

### Step 3: Multi-Task Training
```python
# Combine multiple similarity definitions
training_data = [
    *query_to_text_pairs,
    *query_to_image_summary_pairs,
    *query_to_table_pairs,
    *query_to_code_pairs
]
```

**Benefits:**
- Don't train separate models for each task
- Single model handles multiple similarity types
- Often leads to better results than task-specific models
- Can eventually replace OpenAI embeddings entirely

<!-- 
Jason's practical advice: Start with reranking because you don't need to re-embed existing data. If you already have lots of embedded data, it might not be worth fine-tuning embeddings - just retrieve more chunks and pass to a reranker. Multi-task training is powerful - don't train separate models for each task. One model can handle query-to-text, query-to-image-summary, query-to-table, etc. This often leads to better results than task-specific models.
-->

---

## Success Stories and Benchmarks

**Real-World Improvements:**
- **14% accuracy boost** with fine-tuned cross-encoders
- **12% increase in exact match** with passage encoders (bi-encoders)
- **20% improvement in response accuracy** with rerankers
- **30% reduction in irrelevant documents** retrieved
- **Note:** Irrelevant documents make answers worse depending on model used

**Data Requirements:**
- **100 examples:** Often enough to see improvement (some models beat OpenAI)
- **500-1,000 examples:** Solid performance gains  
- **6,000-10,000 examples:** Significant outperformance of OpenAI embeddings
- **Reality:** You don't need much data to get started

**Performance Examples:**
- MPNet-base-v2: Beats OpenAI at ~100 examples
- BGE-base-1.5: Beats OpenAI at ~500 examples
- Some models easier to train than others

<!-- 
Jason emphasizes you don't need much data to get started. Some models are easier to train than others. MPNet-base-v2 can beat OpenAI with just 100 examples, BGE-base-1.5 needs about 500. The key insight: focus on high-quality training examples rather than massive datasets. Data beats models - focus on quality over quantity.
-->

---

## Modern Tools and Resources

### Sentence Transformers
```python
from sentence_transformers import SentenceTransformer, InputExample
from sentence_transformers import losses

# Triplet loss training
train_examples = [
    InputExample(texts=['query', 'positive', 'negative']),
    # ... more examples
]
```

### Modern BERT (2024)
- **Old:** 512 token limit (older BERT architecture)
- **New:** 8,000 token context (HuggingFace + AnswerAI collaboration)
- **Benefit:** Embed entire documents, better performance
- **Note:** Many sentence-transformers models still use older architecture

### Cohere Rerank API
- **Easy:** Fine-tuning API available
- **Effective:** 300-500ms latency for 10% recall improvement
- **Practical:** Credits provided for course
- **Reality:** Haven't seen an application where adding reranker wasn't worth it
- **Typical Results:** ~10% improvement in recall for 300-500ms latency

### Modal Labs for Parallel Training
- **Speed:** Embed all of Wikipedia in 15 minutes
- **Efficiency:** Test 10-15 embedding models in parallel vs 9 hours sequentially
- **Training:** Allocate 50 GPUs for 20 minutes, train 200 different parameter combinations
- **Pick the best:** Drastically lower cost per experiment

<!-- 
Jason's experience with Modal Labs shows the power of parallelization. Instead of testing embedding models sequentially (9 hours each), test 10-15 in parallel (15 minutes total). For training, allocate 50 GPUs for 20 minutes, train 200 different parameter combinations, pick the best. This drastically lowers the cost per experiment and speeds up iteration. This is how modern ML teams work.
-->

---

## The Coffee Preference Example Resolved

**Training Data Creation:**

### Approach 1: Preference Compatibility
```python
similar_pairs = [
    ("I love coffee", "I love tea"),      # Both positive preferences
    ("I hate coffee", "I hate tea")       # Both negative preferences  
]

dissimilar_pairs = [
    ("I love coffee", "I hate coffee"),   # Opposite preferences
]
```

### Approach 2: Category Similarity
```python
similar_pairs = [
    ("I love coffee", "I hate coffee"),   # Both about coffee
    ("I love tea", "I hate tea")          # Both about tea
]
```

**Result:** Model learns YOUR definition of compatibility

<!-- 
This resolves the coffee preference example from earlier. You can explicitly define what similarity means for your use case. Approach 1: preference compatibility (love coffee + love tea are similar). Approach 2: category similarity (love coffee + hate coffee are similar because both are about coffee). The model learns YOUR definition of what matters.
-->

---

## Implementation Checklist

### Immediate Actions (This Week)
1. **Start logging:** Query + retrieved chunks + user interactions
2. **Generate synthetic pairs:** Use LLM to create training data
3. **Baseline testing:** Compare OpenAI vs domain-specific embeddings

### Short-term (Next Month)  
1. **Collect 1,000 examples:** Mix synthetic + real user data
2. **Fine-tune reranker:** Start with Cohere API
3. **A/B testing:** Measure recall improvements

### Long-term (3-6 Months)
1. **Custom embeddings:** Replace OpenAI entirely
2. **Multi-task training:** Combine multiple similarity definitions
3. **Continuous improvement:** Automated retraining pipeline

<!-- 
This is the roadmap Jason recommends. Start immediately with logging, move to reranking within a month, then build towards custom embeddings and automated retraining. The key is starting NOW - don't wait for the perfect setup. The competitive advantage window is closing.
-->

---

## Common Pitfalls to Avoid

### Data Quality Issues
- **Too easy:** Synthetic data that's obviously correct
- **Too hard:** Impossible edge cases
- **Bias:** Only positive examples, no hard negatives

### Training Issues  
- **Overfitting:** Too much training on small dataset
- **Wrong metrics:** Optimizing for wrong business objective
- **Model choice:** Using cross-encoder for retrieval (too slow)

### Production Issues
- **Latency:** Adding 500ms for 2% improvement
- **Maintenance:** Not updating model with new data
- **Evaluation:** Not measuring business impact

<!-- 
Common pitfalls Jason has observed: synthetic data that's too easy (obviously correct) or too hard (impossible edge cases). Training issues include overfitting on small datasets and optimizing for wrong metrics. Production issues include adding latency for minimal improvement. Always measure business impact, not just technical metrics.
-->

---

## The Wax On, Wax Off Pattern

**The Universal Pattern:**

```
Synthetic Data Generation
    ↓
Evaluation Dataset (20 examples)
    ↓  
Few-Shot Examples (200 examples)
    ↓
Fine-Tuning Dataset (2,000 examples)
    ↓
Production Model (Better relevance)
    ↓
More User Data → Repeat Cycle
```

**Key Insight:** Same data, different applications at different scales

<!-- 
This is the universal pattern that drives everything. The "Wax On, Wax Off" moment Jason keeps referencing. Synthetic data generation scales up through different applications: 20 examples for evaluation, 200 for few-shot, 2,000 for fine-tuning. Same data serves multiple purposes as you scale. This pattern repeats throughout the entire course and will be the foundation for all advanced techniques.
-->

---

## Next Week Preview: User Experience

**Session 3 Focus:**
- Building UX that collects better training data
- Fast feedback loops for continuous improvement
- User interaction patterns that improve models
- Product decisions that enable better AI

**Connection:** Fine-tuned models enable better user experiences, which generate better training data

<!-- 
This sets up the flywheel for Session 3. Better models create better user experiences, which generate better training data, which creates better models. This is the self-reinforcing cycle that separates great RAG systems from mediocre ones. The UX becomes a data collection mechanism.
-->

---

## Key Takeaways

### Technical Insights
1. **Similarity is subjective** - train for your business objective
2. **Start simple** - reranking before custom embeddings
3. **Multi-task training** - one model for multiple similarity types
4. **Data beats models** - focus on high-quality training examples

### Strategic Insights
1. **Start logging now** - don't wait for perfect setup
2. **Synthetic data works** - LLMs can generate quality training data
3. **Small improvements matter** - 10% recall improvement = better product
4. **Continuous improvement** - models should evolve with your product

<!-- 
Jason's core strategic insights: start logging immediately, synthetic data works for generating quality training data, small improvements (10% recall) make a big product difference, and models must evolve with your product. The technical insights: similarity is subjective, start with reranking, use multi-task training, and focus on high-quality examples over massive datasets.
-->

---

## This Week's Homework

### Technical Tasks
1. **Implement logging:** Capture query + results + user interactions
2. **Generate 100 training pairs:** Use synthetic data techniques
3. **Baseline comparison:** Test Sentence Transformers vs OpenAI embeddings
4. **Try Cohere Rerank:** Compare with and without reranking

### Strategic Tasks
1. **Define similarity:** What should "relevant" mean for your use case?
2. **Identify hard cases:** Where do current embeddings fail most?
3. **Plan data collection:** How will users provide relevance feedback?

<!-- 
This week's homework is designed to get you started on the data flywheel. The technical tasks build the foundation: logging, synthetic data generation, baseline comparisons, reranking experiments. The strategic tasks define your objectives: what does "relevant" mean for your use case? Where do current embeddings fail most? How will you collect user feedback?
-->

---

## Remember: The Modern ML Advantage

**Old World (Pre-LLM):**
- Months to collect training data
- $100k+ for human labeling
- Large teams required
- Slow iteration cycles

**New World (With LLMs):**
- Hours to generate training data  
- $100s for synthetic labeling
- Individual developers can fine-tune
- Rapid experimentation
- **Reality:** Get product for free, but forgetting to collect data to improve
- **Mindset shift:** Used to build product with no AI to collect data, then train model

**Seize this opportunity while it's still a competitive advantage**
- What used to be accessible only to large companies is now available to small teams
- Just need prompts, policy, and a for loop

<!-- 
Jason's final call to action emphasizes the dramatic shift in accessibility. What used to require huge teams and budgets now just needs prompts, policy, and a for loop. This is the mindset shift: we used to build products with no AI just to collect data, then train models. Now we get products for free but forget to collect data for improvement. The key insight: seize this opportunity while it's still a competitive advantage. The window won't stay open forever.
-->

---

## Thank You

**Questions for office hours:**
- How to define similarity for your specific use case?
- What's the right amount of training data to start?
- Which model architecture fits your needs?
- How to measure fine-tuning success?

**Next week:** Building user experiences that improve your models

*maven.com/applied-llms/rag-playbook*

<!-- 
End with Jason's key questions for office hours. These are the practical questions people should be asking: How to define similarity for your specific use case? What's the right amount of training data? Which model architecture fits your needs? How to measure fine-tuning success? Next week builds on this foundation with UX that improves models.
-->
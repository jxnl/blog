# Chapter 6 Slides

## jxnl.co

@jxnlco

## Systematically Improving RAG Applications

**Session 6:** Apply: Function Calling Done Right

Jason Liu

---

## Today's Goals

**Combining Search Indices into a Cohesive Application**

- Query routing vs. retrieval indices
- Query routing main challenges and solutions  
- Testing and evaluation strategies
- UI considerations for human-AI interaction
- Food for thought and practical applications

**Move from individual search indices to unified system**

<!-- This is our final core session of the course. We've spent the previous sessions learning how to improve search indices one by one - extracting data, generating summaries, combining lexical search filters with semantic search. Today we're bringing it all together into a cohesive application through intelligent query routing. The session will be quick but focused on practical implementation and UI considerations that make or break real applications. -->

---

## Building on Previous Sessions

**Sessions 4-5: Individual Search Indices**
- Documents, images, text-to-SQL
- Two improvement strategies:
  1. **Structured Data Extraction**
  2. **Text Summaries for Search**

**Today: Combination Strategy**
- Intelligent query routing
- Parallel tool calling
- Human-AI collaboration

<!-- We've learned two main strategies for improving search: turning chunk data into structured data, and building text summaries for better representation in full-text and embedding search. Now we're combining these approaches. This isn't just about the technical implementation - it's about understanding how these tools work together systematically. -->

---

## Case Study: Blueprint Search

**Scenario:** Construction company searches blueprint images

### Step 1: Extract into Index
- Blueprint extractor (OCR → description + date)
- Structured database storage
- Searchable fields

### Step 2: Define Search Tool
```python
class SearchBlueprint(BaseModel):
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
```

<!-- This is a concrete example I want you to really understand. Imagine you're a construction company that needs to search blueprint images. First, you define a blueprint extractor that uses OCR to pull out descriptions and dates. Then you save this structured data to a database. The SearchBlueprint model becomes your API for querying that database - it's like defining a REST API endpoint. This simple tool lets you test whether the documents you're looking for are actually returned with the arguments you specify. -->

---

## You Are a Framework Developer

**Key Insight:** Retrieval methods = REST API methods

**Why this matters:**
- **Modularity:** Multiple APIs query same DB differently
- **Team Scalability:** Individual teams per API type
- **Clean Boundaries:** Interface, implementation, routing

> "You are effectively a framework developer for the language model"

<!-- This is the key insight I want you to internalize. Each retrieval method should feel like a REST API method - a GET or POST request to a specific endpoint. You're building multiple APIs to query the same database in different ways. This allows for modularity where individual teams can work on specific APIs - whether it's searching emails, blueprints, or schedules. From my experience developing microservices for retrieval across multiple teams, this is going to feel a lot like building distributed microservices, but for LLMs. -->

---

## Three-Layer Architecture

### 1. Interface Layer
```python
class SearchText(BaseModel):
    search_query: str
    filter_by_type: Literal["contracts", "proposals", "bids", "all"]
```

### 2. Implementation Layer  
```python
async def execute(self):
    q = table.search(query=self.search_query)
    if self.filter_by_type != "all":
        q = q.filter(type=self.filter_by_type)
    return q.select(["title", "description"]).to_list()
```

### 3. Gateway Layer
```python
tools = [SearchBlueprint, SearchText, AnswerQuery]
# Route → Execute → Synthesize
```

<!-- This three-layer architecture is crucial for scaling teams. The interface layer defines your tool schemas - this is where you discover important capabilities through data analysis. Maybe you find that bids, proposals, and contracts are the key filter types through segmentation analysis. The implementation layer handles the actual search execution - it doesn't matter if you're using Lance, Chroma, Turbopuffer, or Postgres. The gateway layer orchestrates everything with routing and parallel function calling. -->

---

## Team Organization Benefits

**Interface Team**
- Tool segmentation and design
- A/B testing configurations

**Implementation Team**  
- Per-tool performance optimization
- Better embeddings, ranking models

**Gateway Team**
- Tool routing and orchestration
- Prompt engineering, model selection

<!-- These boundaries help you split your team and resources effectively. The interface team can experiment with tool segmentation and A/B test different configurations. The implementation team can focus on per-tool performance optimization - better embeddings, improved ranking models. The gateway team handles the orchestration, testing how tools connect together through the router system. This is exactly what we covered in sessions 4 and 5 for the first two layers. -->

---

## Parallel Tool Calling

**Why parallel tools are powerful:**
- **Speed:** Concurrent searches
- **Comprehensiveness:** Blueprint + text simultaneously  
- **Composability:** Search + clarification + answers

```python
class ToolSuite(BaseModel):
    search_blueprints: Optional[SearchBlueprint]
    search_text: Optional[SearchText]  
    clarify_question: Optional[ClarifyQuestion]
    answer_with_citations: Optional[AnswerQuery]
```

<!-- Notice I'm showing more than just two search tools. In reality, you'll want tools that clarify customer questions and provide answers with proper citations and follow-up questions. This can all be defined in a single model. When you execute a search query, you send it to the search function, return a list of results, gather everything, and pass it back to a language model that synthesizes the final answer. Parallel execution gives you speed, comprehensiveness, and composability. -->

---

## The Systematic Approach

**Same process, applied again:**

### Step 1: Create Test Dataset
```python
example_queries = [
    ("Find blueprints for city hall from 2010", ["search_blueprints"]),
    ("Show me contract proposals", ["search_text"]),  
]
```

### Step 2: Focus on Recall Metrics
- **Data is crucial** for tool evaluation
- **Precision matters later** (avoid wasted compute)
- **Synthetic data generation** requires good descriptions

<!-- We're going back to the same systematic approach - precision and recall. Create a simple dataset mapping queries to expected tools. Synthetic data can help dramatically here, but only if you have good descriptions of what these tools do. If you can't generate good synthetic queries, chances are your tool descriptions aren't detailed enough. This is a signal that you need to improve your prompts about what these tools are supposed to accomplish. -->

---

## Dynamic Few-Shot Examples

### V0: Hard-coded Examples
```python
# 10-40 examples per tool
search_blueprint_examples = [
    "Find city hall blueprints from 2010 → SearchBlueprint(...)",
    "Show school building plans from 2015 → SearchBlueprint(...)"
]
```

### Advanced: Search-Based Retrieval
1. **Build Example Database:** Query → tool mappings
2. **Runtime Retrieval:** Find relevant historical examples  
3. **Dynamic Prompting:** Inject examples into prompt
4. **Continuous Improvement:** More users = better examples

---

## The Complete RAG Improvement System

### 1. Synthetic Data Flywheel
Generate query-to-tool datasets for evaluation

### 2. Establish Recall Metrics  
Per-tool evaluation, system-wide metrics

### 3. Iterate on Few-Shot Examples
Static → Dynamic, 10-40 examples per tool

### 4. Build Example Search System
Store successful mappings, retrieve optimal examples

**Key:** Don't be surprised by 10-40 examples per tool!

<!-- I'm teaching the same system over and over again throughout this course. We start with synthetic data to produce query-to-tool mappings. This creates our recall metrics. Then we iterate on few-shot examples for each tool to improve recall and tool selection. Don't be surprised if you find yourself building prompts with 10-40 examples per tool - prompt caching makes this very tractable, and I've seen tons of examples used in production. As you get more data, you can test different numbers of examples to find your optimal accuracy, latency, and cost balance. -->

---

## Challenge 1: Low Per-Class Recall

**Problem:** 65% overall recall masks individual tool failures

| Expected Tools | Predicted | Issue |
|---|---|---|
| [search_text; search_blueprints] | [search_text] | Missing blueprints |
| [search_blueprints] | [search_text] | Wrong tool |

**Root Cause:** `search_blueprints` has 0% recall!

**Solutions:**
- Better tool descriptions
- Targeted few-shot examples  
- Address class imbalance

<!-- This is a critical debugging pattern. You might see 65% overall recall, but when you break it down per tool, you discover that search_blueprints has 0% recall while search_text is working fine. The system looks decent overall but one tool is completely failing. This is why you can't just look at system-wide metrics - you need per-class recall analysis. Once you know the specific problem, you can have a targeted intervention with better examples specifically for the failing tool. -->

---

## Challenge 2: Tool Confusion Matrix

| | Predicted: blueprints | Predicted: text |
|---|---|---|
| **Actual: blueprints** | 5 | 4 |  
| **Actual: text** | 0 | 9 |

**Blueprint queries misclassified as text search**

**Systematic Debugging:**
1. Filter for failures
2. Pattern analysis
3. Delineation examples
4. Positive/negative examples
5. Edge case coverage

<!-- This confusion matrix approach is systematic debugging in action. You filter for the failure modes, pull that data out of the database, and analyze those specific examples. Most of the work is figuring out what to look at and where to look. You might need to add more evaluations, but more importantly, you want to fix those examples, iterate on the prompt, and verify whether per-tool recall is actually improving. -->

---

## Warning: Data Leakage Prevention

**Critical Issue:** Test examples in few-shot prompts

**Why this happens:**
- Limited data (dozens of examples)
- Overlap between train/test
- Synthetic data similarity

**Consequences:**
- Overestimated performance
- Users see few-shot examples as answers
- Production failures

**Prevention:** Strict train/test splits

<!-- This is a critical warning from my client work. When you have limited data - maybe just dozens of examples - there's huge risk of overlap between training and test data. This dramatically overestimates your performance. Worse, if the data is memorized, you'll get embarrassing results in production where customers see the few-shot examples as actual answers. It's very confusing for everyone. You absolutely must maintain strict train/test splits to avoid this. -->

---

## Understanding System Performance

### The Core Equation
```
P(Correct chunk found) = P(Correct chunk | correct retriever) × P(correct retriever)
```

**Sessions 4-5:** Individual tool performance
**Session 6:** Router/gateway performance

**This identifies your limiting factor:**
- Router problem → Better prompts, examples
- Retriever problem → Better embeddings, filtering

<!-- This equation helps you identify your limiting factors. You're answering two questions: Does the search method find the right text chunk? Can the LLM choose the right search method for the job? That's it. You want a dashboard that shows both the conditional probability of finding the chunk and the probability of correct tool selection. Once you know which is the bottleneck, you know what to work on. Router issues need better few-shot examples and descriptions. Index issues need better embeddings, more training data, and improved filtering. This makes your improvement efforts very actionable. -->

---

## Extended Performance Formula

```
P(success) = P(correct tool | query) × P(success | correct tool) × P(query)
```

| Component | Represents | Improve With |
|---|---|---|
| P(query) | UI Design & Education | Better UX, training |
| P(success) | Overall App Quality | Satisfaction, reliability |
| P(success \| correct tool) | Retrieval Quality | Embeddings, ranking |  
| P(correct tool \| query) | Router Quality | Prompts, examples |

**Strategic:** Segmentation analysis → research vs product roadmap

<!-- This extended formula shows that P(query) is fundamentally a UI design and user education problem. P(success) is your overall app quality and user satisfaction. The other components are retrieval and routing quality. Remember from session 4 - when to double down and when to fold - running these segmentations helps you break down queries to throw away things you're bad at and double down on things you're good at. This is how I help teams plan both their research roadmap and product roadmap. -->

---

## UI Design Philosophy

**Don't Force Chat When Tools Are Better**

**Examples of specialized interfaces:**
- **YouTube:** Video search index
- **Google Maps:** Directions index  
- **LinkedIn:** Professional network
- **Google:** Everything else

> "When I want directions, I open Maps. For videos, YouTube. Don't force users to 'chat with x'"

<!-- This is a huge insight about UI philosophy. YouTube is Google's video index, Google Maps is the directions index, LinkedIn is your professional network index, and Google handles everything else. Even Google is very opinionated about what UI to show based on your search request. There's a massive opportunity to build UI that lets users naturally map their queries to the schemas we've been discussing. Building a chat bot is a feature, not a benefit. Most people want to answer questions and find data - building good search tools is crucial for them. -->

---

## JSON Schema → Form Generation

**Technical Implementation:**
- Each tool = JSON schema
- Auto-generate forms for humans
- Users review/correct parameters
- Enable AI + human access

**The P(query) Factor:**
- Expert users → P(correct tool) = 100%
- Why delegate to AI?
- Offer chat AND structured search

---

## Human-AI Training Loop

**User interactions become training data:**
- **Click-through data:** Which results selected?
- **Correction patterns:** When do users modify AI choices?
- **Usage analytics:** Tool effectiveness

**Result:** Human feedback improves ranking and routing

**Design Principle:** Build for both humans and AI

<!-- If your user is an expert, you can shift P(correct tool) to 100% by letting them choose directly. Why delegate to a model if they know what they want? I like to expose both freeform search that the LLM can use AND structured search tools that humans can use directly. This is like going directly to Maps for directions or YouTube for videos instead of googling everything. User interactions become valuable training data - click-through data, correction patterns, usage analytics - all of this improves your ranking and routing over time. -->

---

## Food for Thought

**Apply at work:**

### From Previous Sessions
- Generate synthetic data
- Topic modeling analysis
- User feedback mechanisms
- Entity-specific indices

### Query Routing Focus
1. Which search methods would you want?
2. Should tools be exposed to users?  
3. Can tools run in parallel?
4. How do users discover capabilities?

<!-- Apply this thinking at work. From previous sessions, consider synthetic data generation, topic modeling analysis, user feedback mechanisms, and entity-specific indices. For query routing specifically: What search methods would be most valuable? Should you expose tools directly to users? Can tools run in parallel effectively? How do users discover what's possible? These questions will guide your implementation decisions. -->

---

## Course Overview

### Sessions 4-5: Individual Indices
- Segmentation & topic modeling
- Specialized retrieval (docs, images, SQL)
- Query routing foundation

### Session 6: Combining Everything
- Tool architecture layers
- Query routing metrics
- RAG playbook applied to routing
- Human-AI collaboration

**Core Theme:** Same systematic process, different levels

<!-- We covered individual indices in sessions 4-5: segmentation, topic modeling, specialized retrieval for docs/images/SQL, and query routing foundations. Today we combined everything with tool architecture layers, routing metrics, and applying the RAG playbook to routing itself. The core theme is applying the same systematic process at different levels - that's why I called this course "Systematically Improving RAG Applications." -->

---

## Course Conclusion

### What You Must Internalize

**1. Evaluations Are Everything**
> "Evaluations are what you need to understand how to improve"

- Evaluations are datasets that inform decisions
- Power few-shot examples  
- Enable retrieval systems
- Become fine-tuning data

**Too many teams have 10-20 examples. Insufficient.**

<!-- This is what you absolutely must internalize. Way too many teams I work with have either no evaluations or tiny sets like 10-20 examples. But evaluations are critical to understanding how to improve your system. Evaluations represent the datasets you use to inform decision-making. Ideally, you can change how you run meetings so conversations aren't just about "making the AI better" but about "moving specific metrics." As you build more evaluations, they become few-shot examples that improve your system, which then become larger datasets for fine-tuning embedding models or re-rankers. -->

---

## Data Is the Foundation

**Synthetic data + customer feedback = same coin**
- All data augmentation at different scales
- Fundamental building blocks of ML products  
- Same process for 20+ years in ML

> "If you refuse to believe this, you're condemning yourself to being lost and confused in this hyped landscape"

<!-- Synthetic data and customer feedback are ultimately what you need to make applications go to the next level. This is the fundamental building block of creating successful machine learning products, and it's been the same process for 20+ years. There are always going to be new companies, new technologies, new frameworks with new names, but we're all doing essentially the same thing. If you refuse to believe this, you're condemning yourself to being lost and confused in this very hyped space. -->

---

## The Virtuous Cycle

```
Good Product (strong UX) 
    → Better Evaluations  
    → Better Models/Training
    → Even Better Product
    → Repeat...
```

**Data analysis over evaluation segments** → focus development

<!-- This is the virtuous cycle that drives everything. A good product with strong UX generates better evaluations. Better evaluations enable better models and training, which creates an even better product. Data analysis over your evaluation segments tells you where to focus development efforts. It's a continuous improvement loop powered by systematic measurement and analysis. -->

---

## Technology Changes, Fundamentals Endure

**Constants that matter:**
- **Strong fundamentals** over hype
- **Product-oriented thinking** over tech chasing  
- **Data-driven improvement** over intuition
- **Systematic evaluation** over ad-hoc testing

**What's new becomes old:**
- New companies, technologies, frameworks
- Same underlying principles
- Focus on transcendent fundamentals

<!-- Technology will always be changing, but the fundamentals endure. Focus on strong fundamentals over hype, product-oriented thinking over technology chasing, data-driven improvement over intuition, and systematic evaluation over ad-hoc testing. What's new today becomes old tomorrow - new companies, technologies, frameworks - but the underlying principles remain constant. Focus on what transcends the current moment. -->

---

## Thank You & Feedback

**Course Goal:** 
Convey importance of strong fundamentals for successful RAG

**Your Feedback:**
- Missing topics?
- Improvement suggestions?
- Better examples?

**Continuing Support:**
- Office hours all year
- Slack community
- Additional videos based on feedback

**Remember:** Technology changes, fundamentals endure

<!-- My goal is to convey the importance of strong fundamentals for successful RAG applications. A lot of this is product-oriented because the technology will always be changing. If you think this course can be improved for future iterations, please let me know. If there are topics you wish I covered but didn't, tell me and I'll work on additional videos for everyone. Thank you all - we'll see you on Slack and at office hours throughout the year. -->

---

## Course Complete

**Next:** Office hours, Q&A, community support

*maven.com/applied-llms/rag-playbook*
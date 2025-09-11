---
title: Tool Interfaces and Implementation
description: Learn how to implement tool interfaces for specialized retrievers and build an effective routing layer
authors:
  - Jason Liu
date: 2025-04-11
tags:
  - tool-interfaces
  - implementation
  - few-shot-learning
  - microservices
---

# Tool Interfaces and Implementation: Building the Components

### Key Insight

**Tools are just specialized retrievers with clear interfaces—success comes from matching tool capabilities to query patterns.** Don't build one monolithic system trying to handle everything. Build focused tools that excel at specific tasks (blueprint search, schedule lookup, document retrieval) and let the router orchestrate them. The interface is the contract that makes this work.

!!! info "Learn the Complete RAG Playbook"
    All of this content comes from my [Systematically Improving RAG Applications](https://maven.com/applied-llms/rag-playbook?promoCode=EBOOK) course. Readers get **20% off** with code EBOOK. Join 500+ engineers who've transformed their RAG systems from demos to production-ready applications.

## Learning Objectives

By the end of this chapter, you will:

1. **Build production-ready tool interfaces** - Create blueprint search, document search, and structured data tools with clear parameter specifications and error handling
2. **Master query routing with few-shot learning** - Implement intelligent routing using Instructor and structured outputs, with 10-40 examples per tool for production systems
3. **Design multi-agent vs single-agent architectures** - Understand when to use specialized agents vs unified routing, balancing token efficiency with system complexity
4. **Implement dynamic example selection** - Build systems that improve routing accuracy by retrieving relevant historical examples based on query similarity
5. **Create feedback loops for continuous improvement** - Turn routing decisions and user interactions into training data that enhances both routing and retrieval performance
6. **Apply RAG architecture evolution patterns** - Understand the progression from pure embeddings to hybrid search to tool-based systems and their trade-offs

## Introduction

## What This Chapter Covers

- Implementing tool interfaces for different content types
- Building query routers with few-shot examples
- Creating feedback loops for routing improvement
- Measuring router vs retriever performance

## Implementing Tool Interfaces

Here's how to implement tool interfaces for a construction information system with blueprints, documents, and schedules.

**Related concepts from previous chapters:**

- Chapter 1: Evaluation metrics for testing router accuracy
- Chapter 3: Feedback showing which tools users need
- Chapter 4: Query analysis for tool requirements
- Chapter 5: Specialized retrievers as tools

### Building a Blueprint Search Tool

Let's start with a concrete example from a construction company that wants to search over images of different blueprints. The process involves two steps:

1. **Blueprint Extractor**: Extract structured data from blueprint images
2. **Blueprint Search Tool**: Query the extracted data

#### Step 1: Blueprint Extractor

First, we need an extractor that processes blueprint images and saves structured data:

```python
from pydantic import BaseModel
from typing import Optional
import datetime

class BlueprintExtractor(BaseModel):
    """Extracts structured data from blueprint images using OCR and AI."""
    
    def extract_from_image(self, image_path: str) -> dict:
        """
        Extract date and description from blueprint image.
        
        Returns:
            dict: Extracted blueprint metadata
        """
        # Use OCR and vision models to extract text
        ocr_text = self._extract_text_from_image(image_path)
        
        # Use LLM to structure the extracted text
        structured_data = self._structure_blueprint_data(ocr_text)
        
        return {
            "description": structured_data.get("description", ""),
            "date": structured_data.get("date", None),
            "image_path": image_path,
            "extracted_at": datetime.datetime.now().isoformat()
        }
    
    def save_to_database(self, blueprint_data: dict):
        """Save extracted blueprint data to database for searching."""
        # Implementation would depend on your database choice
        # This creates the searchable index for our search tool
        pass
```

#### Step 2: Blueprint Search Tool

Now we can build a search tool that queries this structured data:

Based on our analysis in Chapter 5, we've determined that users often search for blueprints by description and date range. We'll define a tool interface that captures this functionality:

```python
from pydantic import BaseModel

class SearchBlueprint(BaseModel):
    description: str
    start_date: str | None = None
    end_date: str | None = None

    def execute(
        self,
    ) -> List[BlueprintResult]:
        """
        Search for blueprints matching the description and date range.

        Args:
            description: Text to search for in blueprint descriptions
            start_date: Optional start date in YYYY-MM-DD format
            end_date: Optional end date in YYYY-MM-DD format

        Returns:
            List of matching blueprint documents
        """
        # Implementation details would depend on your database
        query = self._build_query(
            query=self.description,
            start_date=self.start_date,
            end_date=self.end_date)
        results = self._execute_query(query)
        return self._format_results(results)

        ...
```

### Building a Document Search Tool

Similarly, we can define a tool for searching text documents:

```python
from pydantic import BaseModel

class SearchText(BaseModel):
    query: str
    document_type: Literal["contract", "proposal", "bid"] | None = None

    def execute(
        self,
    ) -> List[DocumentResult]:
        if self.document_type:
            filter_params["type"] = self.document_type

        results = self._search_database(
            query=self.query,
            filters=filter_params)
        return self._format_results(results)
```

### Tool Documentation Matters

Detailed docstrings help both developers and language models understand when to use each tool. Examples are especially important for pattern recognition.

### Tool Portfolio Design

**Key principle**: Tools don't map one-to-one with retrievers. Like command-line utilities, multiple tools can access the same underlying data in different ways.

    **Example: Document Retriever, Multiple Tools**
    ```python
    # One retriever, multiple access patterns
    class DocumentRetriever:
        """Core retrieval engine for all documents"""
        pass

    # Tool 1: Search by keyword
    class SearchDocuments(BaseModel):
        query: str

    # Tool 2: Find by metadata
    class FindDocumentsByMetadata(BaseModel):
        author: Optional[str]
        date_range: Optional[DateRange]
        document_type: Optional[str]

    # Tool 3: Get related documents
    class GetRelatedDocuments(BaseModel):
        document_id: str
        similarity_threshold: float = 0.8
    ```

    This separation allows users to access the same underlying data in ways that match their mental models.

### Model Context Protocol (MCP)

MCP is Anthropic's standard for connecting AI to data sources and tools. It's like USB-C for AI applications – a universal connection standard.

Benefits:

- **Standardization**: One protocol instead of many connectors
- **Interoperability**: Maintain context across tools
- **Ecosystem**: Reusable connectors for common systems
- **Security**: Built-in security considerations

MCP provides a standard way to implement the tools-as-APIs pattern.

**Note**: MCP is still new with limited production implementations. Early adopters should expect to build custom connectors and deal with an evolving standard.

## Building the Routing Layer

The routing layer needs to:

1. Understand the query
2. Select appropriate tools
3. Extract parameters
4. Execute tools
5. Combine results

Modern LLMs handle this well with clear tool definitions and examples.

**Important**: Distinguish between router performance (selecting tools) and retriever performance (finding information). Both need to work well for good results.

### Multi-Agent vs Single-Agent

**Multi-agent challenges:**

- Complex state sharing
- Message passing latency
- Harder debugging
- Error cascades

**Multi-agent benefits:**

- Token efficiency (each agent sees only relevant context)
- Specialization (different models for different tasks)
- Read/write separation for safety

**Example**: A coding assistant might use:

- Single agent for reading/analysis
- Specialized agent for code generation
- Separate agent for file operations

This separates safe read operations from potentially dangerous write operations.

### Implementing a Simple Router

Here's a basic implementation of a query router using the Instructor library for structured outputs:

```python
import instructor
from typing import List, Literal, Iterable
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()
client = instructor.from_openai(client)

class ClarifyQuestion(BaseModel):
    """Use this when you need more information from the user to understand their request."""
    question: str

class AnswerQuestion(BaseModel):
    """Use this when you can answer directly without retrieving documents."""
    content: str
    follow_ups: List[str] | None = None

class SearchBlueprint(BaseModel):
    """Use this to search for building plans and blueprints."""
    blueprint_description: str
    start_date: str | None = None
    end_date: str | None = None

class SearchText(BaseModel):
    """Use this to search for text documents like contracts, proposals, and bids."""
    query: str
    document_type: Literal["contract", "proposal", "bid"] | None = None

def route_query(query: str) -> Iterable[SearchBlueprint | SearchText | AnswerQuestion | ClarifyQuestion]:
    """
    Routes a user query to the appropriate tool(s) based on the query content.

    This function analyzes the user's query and determines which tool or tools
    would be most appropriate to handle it. Multiple tools can be returned if needed.

    Args:
        query: The user's natural language query

    Returns:
        An iterable of tool objects that should be used to process this query
    """
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are a query router for a construction information system.

                Your job is to analyze the user's query and decide which tool(s) should handle it.
                You can return multiple tools if the query requires different types of information.

                Available tools:
                - SearchBlueprint: For finding building plans and blueprints
                - SearchText: For finding text documents like contracts and proposals
                - AnswerQuestion: For directly answering conceptual questions without retrieval
                - ClarifyQuestion: For asking follow-up questions when the query is unclear

                Here are examples of how to route different types of queries:

                <examples>
                ...
                </examples>
                """
            },
            {
                "role": "user",
                "content": query
            }
        ],
        response_model=Iterable[SearchBlueprint | SearchText | AnswerQuestion | ClarifyQuestion]
    )

# Example usage
def process_user_query(query: str):
    """Process a user query by routing it to the appropriate tools and executing them."""
    # Step 1: Route the query to appropriate tools
    tools = route_query(query)

    # Step 2: Execute each tool and collect results
    results = []
    for tool in tools:
        if isinstance(tool, SearchBlueprint):
            # Execute blueprint search
            blueprints = search_blueprints(
                description=tool.blueprint_description,
                start_date=tool.start_date,
                end_date=tool.end_date
            )
            results.append({"type": "blueprints", "data": blueprints})

        elif isinstance(tool, SearchText):
            # Execute text search
            documents = search_documents(
                query=tool.query,
                document_type=tool.document_type
            )
            results.append({"type": "documents", "data": documents})

        elif isinstance(tool, AnswerQuestion):
            # Direct answer without retrieval
            results.append({"type": "answer", "data": tool.content})

        elif isinstance(tool, ClarifyQuestion):
            # Return clarification question to user
            return {"action": "clarify", "question": tool.question}

    # Step 3: Generate a response using the collected results
    return {"action": "respond", "results": results}
```

### Few-Shot Examples for Better Routing

Good examples are critical for router effectiveness. They help the model recognize patterns that should trigger specific tools.

### RAG Architecture Evolution

**Generation 1: Pure Embeddings**

- Single vector database
- Semantic search only
- Limited to similarity

**Generation 2: Hybrid Search**

- Semantic + lexical
- Metadata filtering
- Still retrieval-focused

**Generation 3: Tool-Based**

- Multiple specialized tools
- Beyond retrieval to computation
- Matches user mental models

**Example progression:**

- V1: "Find documents about project X"
- V2: "Find recent documents about project X by John"
- V3: "Compare project X budget vs actuals"

V3 requires computation tools, not just retrieval.

### How This Connects

This chapter combines concepts from throughout the book:

- Chapter 0: Improvement flywheel
- Chapter 1: Evaluation frameworks
- Chapter 2: Fine-tuning
- Chapter 3: Feedback loops
- Chapter 4: Query understanding
- Chapter 5: Specialized capabilities

The unified architecture brings these pieces together.

### Creating Effective Few-Shot Examples

1. **Cover edge cases**: Include ambiguous queries
2. **Multi-tool examples**: Show when to use multiple tools
3. **Hard decisions**: Similar queries, different tools
4. **Real queries**: Use actual user examples when possible
5. **Diversity**: Cover all tools and parameter combinations

For instance, a system prompt for routing might include examples like:

```
<examples>
- "Find blueprints for the city hall built in 2010."
{
    "blueprint_description": "city hall blueprints",
    "start_date": "2010-01-01",
    "end_date": "2010-12-31"
}
- "I need plans for residential buildings constructed after 2015."
{
    "blueprint_description": "residential building plans",
    "start_date": "2015-01-01",
    "end_date": null
}
- "Can you find me the plans for a the 123 main st building?"
{
    "blueprint_description": "123 main st building",
    "start_date": null,
    "end_date": null
}
- "Show me blueprints for schools built between 2018 and 2020."
{
    "blueprint_description": "school blueprints",
    "start_date": "2018-01-01",
    "end_date": "2020-12-31"
}
- "I need the contract for the Johnson project."
{
    "query": "Johnson project contract",
    "document_type": "contract"
}
- "What's the difference between a blueprint and a floor plan?"
{
    "content": "Blueprints are technical architectural drawings that include detailed specifications for construction, while floor plans focus primarily on the layout and dimensions of rooms and spaces within a building.",
    "follow_ups": ["How do I read a blueprint?", "Can you show me examples of floor plans?"]
}
- "Can you explain what a load-bearing wall is?"
{
    "content": "A load-bearing wall is a structural element that supports the weight of the building above it, helping to transfer the load to the foundation. Removing or modifying load-bearing walls requires careful engineering considerations.",
    "follow_ups": ["How can I identify a load-bearing wall?", "What happens if you remove a load-bearing wall?"]
}
- "I'm not sure what kind of building plans I need for my renovation."
{
    "question": "Could you tell me more about your renovation project? What type of building is it, what changes are you planning to make, and do you need plans for permits or for construction guidance?"
}
- "Find me school building plans from 2018-2020 and any related bid documents."
[
    {
        "blueprint_description": "school building plans",
        "start_date": "2018-01-01",
        "end_date": "2020-12-31"
    },
    {
        "query": "school building bids",
        "document_type": "bid"
    }
]
</examples>
```

### Dynamic Example Selection

Once you have enough interaction data, select relevant examples dynamically for each query:

```python
def get_dynamic_examples(query: str, example_database: List[dict], num_examples: int = 5) -> List[dict]:
    """
    Select the most relevant examples for a given query from an example database.

    Args:
        query: The user's query
        example_database: Database of previous successful interactions
        num_examples: Number of examples to return

    Returns:
        List of the most relevant examples for this query
    """
    # Embed the query
    query_embedding = get_embedding(query)

    # Calculate similarity with all examples in database
    similarities = []
    for example in example_database:
        example_embedding = example["embedding"]
        similarity = cosine_similarity(query_embedding, example_embedding)
        similarities.append((similarity, example))

    # Sort by similarity and return top examples
    similarities.sort(reverse=True)
    return [example for _, example in similarities[:num_examples]]

def route_query_with_dynamic_examples(query: str) -> Iterable[Tool]:
    """Route query using dynamically selected examples."""
    # Get relevant examples for this query
    relevant_examples = get_dynamic_examples(query, example_database)

    # Format examples for inclusion in prompt
    examples_text = format_examples(relevant_examples)

    # Create prompt with dynamic examples
    system_prompt = f"""
    You are a query router for a construction information system.
    Your job is to analyze the user's query and decide which tool(s) should handle it.

    Available tools:
    - SearchBlueprint: For finding building plans and blueprints
    - SearchText: For finding text documents like contracts and proposals
    - AnswerQuestion: For directly answering conceptual questions without retrieval
    - ClarifyQuestion: For asking follow-up questions when the query is unclear

    Here are examples of how to route different types of queries:

    {examples_text}
    """

    # Perform routing with dynamic prompt
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        response_model=Iterable[SearchBlueprint | SearchText | AnswerQuestion | ClarifyQuestion]
    )
```

This creates a learning system that improves routing based on successful interactions.

### Critical Warning: Preventing Data Leakage

**The Most Common Router Evaluation Mistake:**

When you have limited data (20-50 examples total), it's easy for your test queries to accidentally appear in your few-shot examples. This creates artificially high performance that doesn't generalize.

**Why This Happens:**
- Small datasets mean high overlap probability
- Synthetic data generation can create similar queries
- Teams reuse examples across different purposes

**Consequences:**
```
Development Results: 95% routing accuracy ✓
Production Reality: 60% routing accuracy ✗
User Experience: Getting few-shot examples as answers (very confusing)
```

**Prevention Strategy:**
1. **Strict Data Splits**: Create test set first, never let it contaminate few-shot examples
2. **Diverse Synthetic Data**: Generate test queries from different prompts than training examples
3. **Regular Auditing**: Check for semantic similarity between test and few-shot examples
4. **Production Validation**: Always validate performance on completely new user queries

### Advanced Router Challenges and Solutions

**Challenge 1: Low Per-Class Recall**

Imagine your router evaluation shows 65% overall recall, but when you break it down by tool:

| Tool | Expected | Correctly Selected | Per-Tool Recall |
|------|----------|-------------------|----------------|
| SearchText | 20 | 18 | 90% |
| SearchBlueprint | 10 | 2 | 20% |
| SearchSchedule | 8 | 6 | 75% |

**Root Cause**: SearchBlueprint has extremely low recall despite good overall metrics.

**Solution Strategy:**
- Add 10-15 specific examples for SearchBlueprint
- Improve tool description to differentiate from SearchText
- Create contrast examples: "similar query, different tools"

**Challenge 2: Tool Confusion Matrix**

| Expected\Predicted | SearchText | SearchBlueprint | SearchSchedule |
|--------------------|------------|-----------------|----------------|
| SearchText | 18 | 1 | 1 |
| SearchBlueprint | 8 | 2 | 0 |
| SearchSchedule | 2 | 0 | 6 |

**Analysis**: Blueprint queries are frequently misclassified as text search.

**Systematic Debugging Process:**
1. **Filter Failures**: Extract all queries where SearchBlueprint was expected but not selected
2. **Pattern Analysis**: Look for common characteristics in failed queries
3. **Targeted Examples**: Create specific few-shot examples addressing these patterns
4. **Delineation**: Add examples showing boundaries between blueprint vs text queries

### Production Scale Considerations

**Few-Shot Example Scale:**
- **Development**: Start with 5-10 examples per tool
- **Production**: Scale to 10-40 examples per tool (don't be surprised by this!)
- **Advanced**: Use dynamic example selection with 100+ historical examples per tool

**Why Large Example Sets Work:**
- **Prompt Caching**: Makes large contexts economical
- **Edge Case Coverage**: More examples = better handling of unusual queries
- **Continuous Learning**: Successful interactions automatically become examples

**Economic Considerations:**
```
Cost Analysis (GPT-4 with prompt caching):
- 40 examples per tool × 5 tools = 200 examples
- ~8,000 tokens cached context = $0.0025 per query
- vs Fine-tuning: $200+ upfront + retraining costs
- Break-even: ~80,000 queries (often worth it for production)
```

## This Week's Action Items

### Tool Interface Implementation (Week 1)
1. **Build Production-Ready Tool Interfaces**
   - [ ] Implement the blueprint search tool with date filtering and description search
   - [ ] Create document search tool with type filtering (contracts, proposals, bids)
   - [ ] Build structured data tools following the Pydantic patterns shown in the examples
   - [ ] Add comprehensive error handling and parameter validation to all tools

2. **Design Tool Portfolio Strategy**
   - [ ] Map your retrievers to multiple tool access patterns (like document retriever → multiple tools)
   - [ ] Design tools that match user mental models, not just technical boundaries
   - [ ] Create clear documentation strings that help both developers and LLMs understand usage
   - [ ] Plan tool interfaces that work for both LLM and direct human access

### Query Routing Implementation (Week 1-2)
3. **Build Intelligent Query Router**
   - [ ] Implement the Instructor-based routing system with structured outputs
   - [ ] Create 10-40 few-shot examples per tool (don't be surprised by this scale!)
   - [ ] Test parallel tool calling and result combination
   - [ ] Implement both ClarifyQuestion and AnswerQuestion tools for comprehensive coverage

4. **Master Few-Shot Example Management**
   - [ ] Create diverse examples covering edge cases and multi-tool scenarios
   - [ ] Include contrast examples for commonly confused tools
   - [ ] Test and prevent data leakage between few-shot examples and test sets
   - [ ] Implement example quality scoring and selection mechanisms

### Advanced Routing Strategies (Week 2-3)
5. **Implement Dynamic Example Selection**
   - [ ] Build example database with query embeddings for similarity matching
   - [ ] Implement runtime retrieval of most relevant historical routing examples  
   - [ ] Create continuous improvement cycle where successful interactions become examples
   - [ ] Test performance improvement from dynamic vs static examples

6. **Multi-Agent vs Single-Agent Decisions**
   - [ ] Analyze your use case for token efficiency vs specialization benefits
   - [ ] Consider read/write separation for safety in coding or file operations
   - [ ] Test different agent architectures for your specific domain
   - [ ] Implement state sharing mechanisms if using multi-agent approach

### Feedback Loop Creation (Week 2-3)
7. **Build Continuous Improvement System**
   - [ ] Implement routing decision logging and analysis
   - [ ] Create user feedback collection mechanisms from successful interactions
   - [ ] Build automated example database updates from high-quality routing decisions
   - [ ] Test feedback loop effectiveness on routing accuracy improvements

8. **Architecture Evolution Implementation**
   - [ ] Assess your current architecture: Generation 1 (embeddings), 2 (hybrid), or 3 (tools)
   - [ ] Plan migration path to more advanced architecture if needed
   - [ ] Implement Generation 3 capabilities: computation tools beyond just retrieval
   - [ ] Test user satisfaction with tool-based vs pure retrieval approaches

### Production Integration (Week 3-4)
9. **Model Context Protocol (MCP) Preparation**
   - [ ] Research MCP standards for your tool interfaces (early adoption consideration)
   - [ ] Design tools to be MCP-compatible for future interoperability
   - [ ] Plan for standardized tool connections across different AI systems
   - [ ] Consider building custom connectors if adopting MCP early

10. **Performance Optimization**
    - [ ] Implement prompt caching for large few-shot example sets
    - [ ] Optimize parallel tool execution for minimal latency
    - [ ] Build monitoring for routing accuracy and response times
    - [ ] Plan scaling strategy for increased query volume

### Success Metrics
- **Tool Interface Quality**: Clear, well-documented interfaces that work for both AI and humans
- **Routing Accuracy**: High precision (when tools selected, they're correct) and recall (all needed tools selected)
- **System Learning**: Measurable improvement in routing decisions from feedback loops
- **Architecture Maturity**: Successful migration to Generation 3 tool-based system with computation capabilities
- **User Experience**: Both AI routing and direct tool access provide value to different user types

!!! tip "Next Steps"
    	In [Chapter 6-3](chapter6-3.md), we'll implement comprehensive performance measurement and create user interfaces that leverage both AI routing and direct tool access.

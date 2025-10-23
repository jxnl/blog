---
title: "Beyond Chunks: Why Context Engineering is the Future of RAG"
description: "Learn how to move beyond traditional chunk-based RAG to context engineering that gives agents peripheral vision of data landscapes. Explore four levels from basic chunks to faceted search with business outcomes and practical implementation strategies."
date: 2025-08-27
slug: "facets-context-engineering"
tags:
  - Context Engineering
  - Agents
---

# Why Is Context Engineering the Future of RAG?

**The core insight:** In agentic systems, how we structure tool responses is as important as the information they contain.

_This is the first post in a series on context engineering. I'm starting here because it's the lowest hanging fruit—something every company can audit and experiment with immediately._

<!-- more -->

**Key Terms:**

- **Context Engineering:** Structuring tool responses and information flow to give agents the right data in the right format for effective reasoning
- **Faceted Search:** Exposing metadata aggregations (counts, categories, filters) alongside search results to reveal the data landscape
- **Agent Peripheral Vision:** Providing agents with structured metadata about the broader information space beyond just the top-k results
- **Tool Response as Prompt Engineering:** Using XML structure, metadata, and system instructions in tool outputs to guide future agent behavior

RAG worked brilliantly for the past few years. You'd embed documents, search for relevant chunks, stuff them into a prompt, and get surprisingly good answers. Simple, effective, solved real problems. I've written extensively about [systematically improving RAG applications](./systematically-improving-rag-raindrop.md) and [common RAG anti-patterns](./rag-anti-patterns-skylar.md) to avoid.

But agents changed the game. They're persistent, make multiple tool calls, and build understanding across conversations. They don't just need the right chunk—they need to understand the landscape of available information so they can decide what to explore, make plans and then execute. This shift is exemplified by successful coding agents like those discussed in our [Coding Agents Speaker Series](./coding-series-index.md), where simple tools with agentic loops consistently outperform complex retrieval systems.

I learned this through my consulting work and teaching at [improvingrag.com](https://improvingrag.com). I get to talk to a lot of companies building AI systems, plus I host office hours where teams bring their real production challenges. The pattern is consistent: teams have perfectly functional search systems returning relevant text chunks. Then users start asking "Who modified this document last?" and "How recent is this policy?" and teams start asking themselves, what is the work that these systems can really do?

The breakthrough came when we realized chunks themselves were the limitation. When search results showed multiple fragments from the same document, we were asking agents to piece together puzzles instead of loading complete pages. A simple `load_pages()` function improved agent reasoning dramatically.

Then we noticed something profound: these structured tool responses weren't just returning data—they were teaching agents how to think about the data. The metadata became prompt engineering itself.

This is the fundamental problem with chunk-based RAG in agentic systems. Agents aren't just looking for answers—they're trying to understand what questions to ask next. They need peripheral vision of the data landscape, not just the highest-scoring chunks.

**The paradigm shift:** As [Anthropic explains](https://www.anthropic.com/engineering/writing-tools-for-agents), tools represent a new kind of software contract—between deterministic systems and non-deterministic agents. Traditional functions like `getWeather("NYC")` work predictably every time. But when an agent asks "Should I bring an umbrella today?" it might call the weather tool, answer from memory, ask for location clarification, or even hallucinate. This fundamental non-determinism means we need to design tools that increase the surface area over which agents can be effective, not just return the "right" answer.

<!-- more -->

## What Are the Four Levels of Context Engineering?

I'll demonstrate this through four progressively complex levels:

**Level 1 — Minimal Chunks** - Basic tool responses without metadata
**Level 2 — Chunks with Source Metadata** - Enables citations and strategic document loading  
**Level 3 — Multi-Modal Content** - Optimizes tables, images, and structured data for agents
**Level 4 — Facets and Query Refinement** - Reveals the complete data landscape for strategic exploration

This progression leads to two key predictions:

1. **Tool results become prompt engineering** - Metadata teaches agents how to use tools in future calls
2. **Databases become reasoning partners** - Facets surface patterns that agents leverage but humans wouldn't think to ask for

## Why Is Search Quality Your Ceiling?

!!! warning "Hard Truth"
Good search is the ceiling on your RAG quality. If recall is poor, no prompt engineering or model upgrade will save you. I've seen teams spend weeks fine-tuning prompts when their real problem was that the relevant information simply wasn't being retrieved. This is why focusing on the right RAG evaluation metrics is crucial.

Context engineering goes beyond returning chunks. It's about returning actionable structure about the result set so the next tool call can be smarter. Think of it as giving agents peripheral vision about the data landscape.

!!! tip "Start Here: Audit Your Current Tools"
Before building new infrastructure, audit what your tools actually return. Most improvements are just better string formatting—wrapping results in XML, adding source metadata, including system instructions. No major architectural changes required.

**Design principle from [Anthropic's tool development guide](https://www.anthropic.com/engineering/writing-tools-for-agents):** Think of tool descriptions as prompt engineering for your agents. How you name functions, structure parameters, and format responses directly influences agent reasoning patterns. Clear tool boundaries and meaningful parameter names reduce confusion and hallucinations.

## How Should We Balance Complexity?

Here's the uncomfortable truth: there's no single right answer for how much metadata to include. Every system has different needs, and the more complex you make your tools, the higher the likelihood of hallucinations and tool misuse.

This reality demands two things from us as builders:

**Better prompts.** Complex tools require sophisticated instructions. You can't just throw a dozen parameters at an agent and hope it figures out the right combinations. Your system instructions become as important as your tool design.

**Better creativity in system design.** The same outcome can often be achieved through simpler tool compositions rather than one mega-tool. Sometimes it's better to have separate `search()` and `filter_by_date()` functions rather than cramming everything into a single interface with endless optional parameters.

!!! tip "Design Principle"
Recognize when complexity pays for itself. Metadata that doesn't change agent behavior is just expensive noise.

**Token efficiency insight:** [Anthropic's research](https://www.anthropic.com/engineering/writing-tools-for-agents) shows that tool responses should prioritize contextual relevance over flexibility. Return high-signal information that directly informs downstream actions, not low-level technical identifiers. Consider adding `response_format` parameters ("concise" vs "detailed") to let agents control verbosity based on their current reasoning needs. They recommend implementing pagination, filtering, and truncation with sensible defaults for any responses that could consume significant context.

    **The beauty of context engineering:** You don't need to redesign your tools or rebuild your infrastructure. Most improvements are XML structuring, source tracking, and system instructions—essentially better string formatting with potentially massive upside.

**Evaluation-driven improvement:** [Anthropic's research](https://www.anthropic.com/engineering/writing-tools-for-agents) shows that systematic evaluation is critical for tool optimization. Generate realistic test tasks based on your actual use cases, measure agent performance across tool response levels, and iterate based on concrete metrics rather than intuition. The teams that build comprehensive evaluations early dramatically outperform those that rely on ad-hoc testing.

### Level 1 — Minimal Chunks (No Metadata)

```python
def search(query: str, n_chunks: int = 10) -> list[str]:
    """
    Search documents and return relevant text chunks. No metadata or source
    information provided - you'll get raw text content only.

    Use this when you need quick answers but don't need to trace information
    back to sources or understand document structure.

    Args:
        query: What you're looking for in natural language
        n_chunks: How many text chunks to return (default: 10)

    Returns:
        List of text chunks that match your query
    """
    pass
```

```xml
<ToolResponse>
  <results query="find refund policy for enterprise plan">
    <chunk>Termination for Convenience. Either party may terminate this Agreement upon thirty (30) days' written notice...</chunk>
    <chunk>Confidentiality. Recipient shall not disclose any Confidential Information for five (5) years...</chunk>
    <chunk>Limitation of Liability. In no event shall aggregate liability exceed the fees paid in the twelve (12) months...</chunk>
  </results>
</ToolResponse>
```

**The limitation:** Without metadata, agents can't make strategic decisions about where to search next. They're flying blind.

### Level 2 — Chunks with Basic Source Metadata

**Available tools:**

```python
def search(query: str, source: str = None, n_chunks: int = 10) -> dict:
    """
    Search documents with source tracking. Returns chunks with metadata
    so you can cite sources and see document patterns.

    When you see multiple chunks from the same document, that usually means
    the document has comprehensive coverage of your topic.

    Args:
        query: What you're looking for in natural language
        source: Limit search to a specific document (optional)
        n_chunks: How many chunks to return (default: 10)

    Returns:
        Results with source files, page numbers, and chunk content
    """
    pass

def load_pages(source: str, pages: list[int]) -> dict:
    """
    Get full pages from a document when you need complete context instead
    of fragmented chunks.

    Use this when search results show multiple chunks from the same document -
    usually means you should read the full pages rather than piecing together
    fragments.

    Args:
        source: Document path (like "contracts/MSA-2024.pdf")
        pages: Which pages to load (like [3, 7, 12])

    Returns:
        Complete page content with source information
    """
    pass
```

**Example tool response:**

```xml
<ToolResponse>
  <results query="find refund policy for enterprise plan">
    <chunk id="1" source="contracts/MSA-2024-ACME.pdf" page="7">
      Refunds. Enterprise plan refunds require prior written approval by Customer's account administrator and must be submitted within sixty (60) days...
    </chunk>
    <chunk id="2" source="contracts/DPA-2024-ACME.pdf" page="3">
      Chargebacks and Adjustments. Provider may issue credits in lieu of refunds as mutually agreed in writing...
    </chunk>
    <chunk id="3" source="policies/refunds.md" page="1">
      Standard refunds are available within 30 days of purchase for all standard plan subscriptions; enterprise terms may supersede...
    </chunk>
  </results>

  <system-instruction>
    Key insight: Multiple chunks from same source = use load_pages() instead of fragments.
    Decision framework: Same source clustering → load full pages; Multiple sources → targeted follow-up searches.

    Tool usage guidance: When writing tool descriptions, think like you're training a new team member. Make implicit knowledge explicit—specialized query formats, terminology definitions, and relationships between resources. Ambiguous parameter names like "user" should become "user_id" for clarity.

    Error handling strategy: If tool calls fail validation, return actionable error messages that guide agents toward correct usage rather than cryptic error codes. For example: "Date filter requires YYYY-MM-DD format, received '2024/03/15'" instead of "ValueError: invalid date format".
  </system-instruction>
</ToolResponse>
```

**The breakthrough:** Agents now see document clustering patterns and can strategically load full pages instead of piecing together fragments. Citations become possible.

### Level 3 — Multi-Modal Content Representation

Modern documents aren't just text - they contain tables, charts, diagrams, code blocks, and other structured content. Agents need appropriate representations for different content modalities to reason effectively.

**Available tools:**

```python
def search(
    query: str,
    source: str = None,
    content_types: list[str] = None,  # ["text", "table", "image", "code"]
    n_chunks: int = 10
) -> dict:
    """
    Search documents and get back content in the right format for reasoning.
    Tables, images, and structured content are automatically formatted for
    optimal analysis.

    Simple tables return as Markdown for easy data work. Complex tables with
    merged cells return as HTML so you can understand the relationships.
    Images include both the visual content and searchable OCR text.

    Args:
        query: What you're looking for in natural language
        source: Limit to specific document (optional)
        content_types: Filter by content type like ["table"] or ["image"] (optional)
        n_chunks: How many chunks to return (default: 10)

    Returns:
        Content formatted appropriately for each type (Markdown, HTML, images with OCR)
    """
    pass

def load_pages(source: str, pages: list[int]) -> dict:
    """
    Get complete pages when you need full context instead of fragments.

    Use this when search shows multiple chunks from the same document -
    usually better to read full pages than piece together fragments.

    Args:
        source: Document path (like "reports/Q3-2024.pdf")
        pages: Which pages to load (like [3, 7, 12])

    Returns:
        Complete page content with all formatting preserved
    """
    pass
```

**Example with multi-modal content:**

```xml
<ToolResponse>
  <results query="quarterly performance metrics">
    <chunk id="1" source="reports/summary.pdf" page="3" content_type="table" table_complexity="simple">
      | Quarter | Revenue | Growth |
      |---------|---------|--------|
      | Q1 2024 | $45M    | 12%    |
      | Q2 2024 | $52M    | 18%    |
      | Q3 2024 | $58M    | 22%    |
    </chunk>

    <chunk id="2" source="reports/detailed.pdf" page="7" content_type="table" table_complexity="complex">
      <table>
        <thead>
          <tr><th rowspan="2">Region</th><th colspan="3">Q3 2024</th></tr>
          <tr><th>Revenue</th><th>Units</th><th>Margin</th></tr>
        </thead>
        <tbody>
          <tr><td>North America</td><td>$25.2M</td><td>1,250</td><td>34%</td></tr>
        </tbody>
      </table>
    </chunk>

    <chunk id="3" source="reports/charts.pdf" page="12" content_type="image">
      <image_data>
        <ocr_text>Q3 Revenue Breakdown • North America: $25.2M (43%) • Europe: $18.3M (32%)</ocr_text>
        <image_base64>[base64 encoded pie chart]</image_base64>
      </image_data>
    </chunk>
  </results>
</ToolResponse>
```

But even with perfectly formatted multi-modal content, agents still face a fundamental limitation: they can only see the top-k results. What about all the other relevant documents that didn't make the similarity cutoff? What patterns exist in the broader dataset that could guide their next search?

This is where facets transform the game entirely. Instead of just returning results, we start returning the _landscape_ of results.

### Level 4 — Facets and Query Refinement

At this level, we introduce facets - aggregated metadata that helps agents understand the data landscape and refine their queries iteratively, just like users do on e-commerce sites.

Think e-commerce: search "running shoes" → get results + facets (Nike: 45, Adidas: 32, 4-star: 28, 5-star: 12). Click "Nike" + "4+ stars" → refined results, still targeted.

Agents use the same pattern, but they already understand this instinctively. Consider how coding agents work today:

```bash
$ grep -r "UserService" . --include="*.py" | cut -d: -f1 | sort | uniq -c
      6 ./user_controller.py
      4 ./auth_service.py
      3 ./models.py
      2 ./test_user.py
```

The agent sees these file distribution counts and immediately recognizes that `user_controller.py` (6 occurrences) and `auth_service.py` (4 occurrences) deserve full attention. Instead of reading 20 disconnected grep snippets, it strategically calls `read_file()` on the files with the highest relevance signals.

This is exactly faceted search: aggregate counts reveal which documents deserve complete context rather than fragmented chunks.

**Available tools:**

The same `search()` function from previous levels, but now automatically returns facet information alongside results. The filter parameters align with the facet dimensions returned.

```python
def search(
    query: str,
    source: str = None,
    document_type: str = None,
    freshness_score_min: float = None,
    n_chunks: int = 10
) -> dict:
    """
    Semantic search that automatically returns results with facet information.

    Args:
        query: Natural language search query
        source: Optional filter by document source (aligns with source_facet)
        document_type: Optional filter by document category
        freshness_score_min: Optional minimum freshness score
        n_chunks: Number of chunks to return (default: 10)

    Returns:
        Dict with chunks, facets, and system instructions
    """
    pass
```

**Example search with facets:**

```xml
<ToolResponse>
  <results query="data processing requirements">
    <chunk id="1" source="contracts/MSA-2024-ACME.pdf" page="8" document_type="contract" freshness_score="0.94">
      Data Processing. All customer data shall be processed in accordance with applicable data protection laws, including GDPR and CCPA. Data residency requirements specify that EU customer data must remain within approved European data centers...
    </chunk>
    <chunk id="2" source="contracts/MSA-2024-ACME.pdf" page="12" document_type="contract" freshness_score="0.92">
      Data Subject Rights. Customer may request access, rectification, erasure, or portability of their personal data. Provider must respond to such requests within 30 days and provide mechanisms for automated data export...
    </chunk>
    <chunk id="3" source="policies/privacy-policy-v3.md" page="2" document_type="policy" freshness_score="0.89">
      Privacy Policy Updates. We collect and process personal information in accordance with our privacy policy. Data processing purposes include service delivery, analytics, and compliance with legal obligations...
    </chunk>
    <chunk id="4" source="contracts/MSA-2024-ACME.pdf" page="15" document_type="contract" freshness_score="0.91">
      Cross-Border Transfers. Any transfer of personal data outside the EEA requires adequate safeguards including Standard Contractual Clauses or adequacy decisions. Provider maintains current transfer impact assessments...
    </chunk>
    <chunk id="5" source="compliance/gdpr-checklist.md" page="1" document_type="compliance" freshness_score="0.95">
      GDPR Compliance Checklist. Ensure lawful basis for processing, implement data subject rights, conduct privacy impact assessments for high-risk processing activities...
    </chunk>
  </results>

  <facets>
    <source_facet>
      <value name="contracts/MSA-2024-ACME.pdf" count="7" />
      <value name="policies/privacy-policy-v3.md" count="4" />
      <value name="compliance/gdpr-checklist.md" count="5" />
      <value name="contracts/DPA-2024-ACME.pdf" count="2" />
    </source_facet>
  </facets>

  <system-instruction>
    Facets reveal the complete data landscape beyond top-k similarity cutoffs. Counts show the full scope of relevant information, not just what ranked highest.

    Key insight: High facet counts for sources with few/zero returned chunks indicate valuable information filtered out by similarity ranking.

    Decision framework:
    - High facet counts vs. low returned chunks: investigate with source filters
    - One source dominates results: consider loading full document pages
    - Clear clustering patterns: apply targeted filters for focused search

    Use document_type, source, and other metadata filters strategically based on facet distributions.
  </system-instruction>
</ToolResponse>
```

**The transformation:** Agents gain peripheral vision of the entire data landscape. Facets reveal hidden documents that similarity search missed, enabling strategic exploration beyond the top-k cutoff.

## What Types of Facet Data Sources Exist?

Facets can come from two primary sources: existing structured systems and AI-extracted metadata from unstructured documents.

### What Are Structured Systems for Facets?

CRMs, ERPs, HR systems, and other business databases already contain rich structured data that can power faceted search. These systems track entities, relationships, and metadata that users often don't realize can be leveraged for search.

#### How Would This Work for Linear Ticket Search?

```python
def search(
    query: str,
    team: Literal["Backend", "Frontend", "QA", "DevOps"] | None = None,
    status: Literal["Open", "Done", "In Progress", "Backlog"] | None = None,
    priority: Literal["High", "Medium", "Low", "Urgent"] | None = None,
    assignee: str | None = None,
    n_results: int = 10
) -> dict:
    """
    Search Linear tickets with faceted filtering.

    Args:
        query: Natural language search query
        team: Filter by team
        status: Filter by status
        priority: Filter by priority
        assignee: Filter by assigned user
        n_results: Number of tickets to return

    Returns:
        Dict with tickets, facets, and system instructions
    """
    pass
```

When an agent searches `search("API timeout issues")`, it gets:

```xml
<ToolResponse>
  <results query="API timeout issues">
    <ticket id="LIN-1247" team="Backend" status="Done" priority="High" assignee="alice">
      <title>API Gateway timeout after 30s on heavy load</title>
      <description>Fixed by increasing timeout thresholds to 60s and optimizing connection pooling. Load balancer 504 errors reduced by 95%...</description>
    </ticket>
    <ticket id="LIN-1189" team="Frontend" status="Done" priority="Medium" assignee="bob">
      <title>Client-side timeout handling for slow API responses</title>
      <description>Implemented retry logic and user feedback for API timeouts. Added exponential backoff and circuit breaker pattern...</description>
    </ticket>
    <ticket id="LIN-1203" team="Backend" status="Done" priority="High" assignee="alice">
      <title>Database query optimization causing API delays</title>
      <description>Resolved N+1 query problem by implementing batched queries and adding proper indexes. API response times improved 3x...</description>
    </ticket>
  </results>

  <facets>
    <team_facet>
      <value name="Backend" count="8" />
      <value name="Frontend" count="4" />
      <value name="QA" count="3" />
    </team_facet>
    <status_facet>
      <value name="Done" count="6" />
      <value name="Open" count="5" />
      <value name="In Progress" count="4" />
    </status_facet>
    <priority_facet>
      <value name="High" count="7" />
      <value name="Medium" count="6" />
      <value name="Low" count="2" />
    </priority_facet>
    <assignee_facet>
      <value name="alice" count="5" />
      <value name="bob" count="4" />
      <value name="charlie" count="3" />
    </assignee_facet>
  </facets>

  <system-instruction>
    Facets reveal metadata clustering patterns across team, status, priority, and assignee dimensions. High counts indicate where relevant information concentrates.

    Key insight: When all returned results share characteristics (like status="Done"), facets often reveal hidden relevant data with different values that need investigation.

    Decision framework:
    - All results share traits: check facets for hidden different values (e.g., "Open" tickets)
    - Strong clustering patterns: apply targeted filters for focused investigation
    - Uncertain relevance: surface metadata distributions to user for guidance

    Combine multiple filters (team + status + priority) to narrow search scope strategically.
  </system-instruction>
</ToolResponse>
```

!!! danger "Similarity Bias Alert"
All 3 returned tickets are "Done" but facets show 5 "Open" tickets exist. Resolved tickets have better documentation and rank higher in similarity search, while active issues get filtered out. Call `search("API timeout", status="Open")` to find them.

### What Are Extracted Facets?

Companies like Extend and Reducto can perform structured data extraction over documents to create facets that don't naturally exist in the raw text.

#### How Would This Work for Contract Analysis?

```python
def search(
    query: str,
    signature_status: Literal["Signed", "Unsigned", "Partially Signed"] | None = None,
    project: Literal["Project Alpha", "Project Beta", "General Services"] | None = None,
    document_type: Literal["contract", "amendment", "renewal"] | None = None,
    n_results: int = 10
) -> dict:
    """
    Search legal contracts with AI-extracted faceted filtering.

    Args:
        query: Natural language search query
        signature_status: Filter by signing status
        project: Filter by project classification
        document_type: Filter by document type
        n_results: Number of contracts to return

    Returns:
        Dict with contracts, facets, and system instructions
    """
    pass
```

An AI system first processes legal documents and extracts:

1. **Document type detection**: Uses classification to identify "contract" vs "amendment" vs "renewal"
2. **Signature extraction**: Analyzes signature blocks to determine signed/unsigned status
3. **Project classification**: Matches contract language to project codes or client names

When an agent searches `search("liability provisions")`, it gets:

```xml
<ToolResponse>
  <results query="liability provisions">
    <contract id="MSA-2024-ACME" signature_status="Signed" project="Project Alpha">
      <title>Master Service Agreement - ACME Corp</title>
      <content>Limitation of Liability. In no event shall either party's aggregate liability exceed the total fees paid under this Agreement in the twelve (12) months preceding the claim. This limitation applies to all claims in contract, tort, or otherwise...</content>
    </contract>
    <contract id="SOW-2024-BETA" signature_status="Signed" project="Project Beta">
      <title>Statement of Work - Beta Industries</title>
      <content>Liability Cap. Provider's liability is limited to direct damages only, not to exceed $100,000 per incident. Consequential, incidental, and punitive damages are excluded...</content>
    </contract>
    <contract id="AMEND-2024-GAMMA" signature_status="Signed" project="General Services">
      <title>Amendment to Services Agreement - Gamma LLC</title>
      <content>Modified Liability Terms. Section 8.3 is hereby amended to include joint liability provisions for third-party claims arising from data processing activities...</content>
    </contract>
  </results>

  <facets>
    <signature_status_facet>
      <value name="Signed" count="45" />
      <value name="Unsigned" count="12" />
      <value name="Partially Signed" count="3" />
    </signature_status_facet>
    <project_facet>
      <value name="Project Alpha" count="23" />
      <value name="Project Beta" count="18" />
      <value name="General Services" count="19" />
    </project_facet>
  </facets>

  <system-instruction>
    Facets expose the complete metadata landscape, revealing information patterns beyond similarity rankings. Extracted facets show clustering across signature status, project, and document type.

    Key insight: When returned results show bias (e.g., all signed contracts), facets often reveal critical hidden data with different characteristics that need attention.

    Decision framework:
    - Results show bias: investigate facet values not represented in top-k results
    - High clustering in facets: focused filtering more effective than broad search
    - Clear relevance patterns: apply filters autonomously for targeted investigation

    Use signature_status, project, document_type filters strategically based on facet distributions and business priorities.
  </system-instruction>
</ToolResponse>
```

!!! warning "Critical Documents Missing"
All 3 returned contracts are signed, but facets reveal 12 unsigned contracts exist in the broader result set. Signed contracts have better-developed liability language (higher similarity scores), while unsigned contracts with liability provisions didn't make the top-k cut. The agent should call `search("liability", signature_status="Unsigned")` to examine those hidden contracts - they need attention before signing.

## Why Does Agent Persistence Change Everything?

This is the paradigm shift most teams miss: agentic systems are incredibly persistent. Given enough budget and time, they'll keep searching until they find what they need. This fundamentally changes how we should think about search system design. This persistence enables continuous feedback loops that improve system performance over time.

Traditional RAG optimized for humans who make one query and expect comprehensive results. Miss something? The human has to think of a different search term or give up. This pressure created the "stuff everything relevant into the first response" mentality that led to context window bloat and degraded performance.

Agents operate differently. They're methodical, systematic, and don't get frustrated. Show them a facet indicating 47 relevant documents in a category they haven't explored? They'll investigate. Reveal that unsigned contracts contain different terms than signed ones? They'll filter specifically for unsigned contracts and analyze the gaps.

**The strategic implication:** You don't need perfect recall on query #1. You need to give agents enough context about the information landscape that they can systematically traverse it. Each faceted search reveals new dimensions to explore, creating an implicit knowledge graph that agents can navigate without you having to explicitly define node relationships.

This aligns perfectly with [Anthropic's observation](https://www.anthropic.com/engineering/writing-tools-for-agents) that effective tools increase the "surface area over which agents can be effective." Rather than trying to solve everything in one perfect retrieval, facets guide agents through multiple successful strategies until they achieve comprehensive coverage. The goal isn't perfect tools—it's tools that help agents pursue diverse paths to success.

Consider the contract example: the agent didn't need to find all liability provisions in one search. It needed to discover that liability provisions cluster around document types (contracts vs. amendments), signing status (signed vs. unsigned), and projects (Alpha vs. Beta vs. General). Armed with these facets, it can systematically explore each combination until it has complete coverage.

This transforms the database from a passive responder to an active reasoning partner. Facets surface patterns and gaps that agents can leverage but humans would never think to ask for directly.

## How Do We Evolve from Chunks to Context?

We've traced the evolution from basic chunks to sophisticated context engineering across four levels. Level 1 gives agents raw text but leaves them blind to metadata patterns. Level 2 adds source tracking, enabling strategic document loading and proper citations. Level 3 optimizes multi-modal content formatting so agents can reason about tables, images, and structured data. Level 4 introduces facets that reveal the complete data landscape, transforming search from similarity-based retrieval to exploration.

The progression shows a clear pattern: **each level adds peripheral vision about the information space.** Agents don't just get better answers—they get better context about what questions to ask next. Tool responses become teaching moments, showing agents how to think about the data systematically.

The business impacts are measurable: 90% reduction in clarification questions, 75% reduction in expert escalations, 95% reduction in 504 errors, 4x improvement in resolution times. But the deeper transformation is architectural—databases evolve from passive storage to active reasoning partners that surface patterns human users would never think to request.

## What Comes Next?

This is the first post in a series on context engineering. I started here because it's the most accessible entry point—something every team can experiment with today.

**Why this is the lowest hanging fruit:** Context engineering doesn't require rebuilding your infrastructure or redesigning your tools. It's primarily about better string formatting—wrapping responses in XML, adding source metadata, including strategic system instructions. Low technical lift, potentially massive business impact.

**The immediate action:** Go audit your current RAG implementation. Look at what your tools actually return. Are you giving agents peripheral vision of the data landscape, or just the highest-scoring chunks? Most teams can implement Level 2 (source metadata) in an afternoon.

**For rapid validation:** Use the [prototyping methodology](./context-engineering-agent-prototyping.md) to test different tool response levels quickly. Claude Code's project runner lets you experiment with minimal chunks vs faceted responses without building infrastructure—you can discover which level your use case needs through folder-based testing.

**Collaborative optimization:** One of Anthropic's most powerful insights is using Claude to optimize its own tools. After building your initial tools, have Claude analyze the tool responses, suggest improvements to the schemas and descriptions, and even generate better evaluation tasks. The tools that are most ergonomic for agents often end up being surprisingly intuitive for humans too.

**Adoption will follow the usual pattern:** The teams building agents today will implement context engineering first, then the tooling will catch up. Vector databases are already adding facet support (TurboPuffer ships facets and aggregations), but you don't need to wait for perfect tooling to start.

**Tool responses become teaching moments.** The XML structures and system instructions in your tool responses directly influence how agents think about subsequent searches. Design them intentionally. As [Anthropic's engineering team notes](https://www.anthropic.com/engineering/writing-tools-for-agents), effective tools help agents pursue diverse successful strategies by providing meaningful context that guides future reasoning patterns.

Next in this series: Advanced faceting strategies, when to use structured vs. extracted metadata, and measuring the business impact of context engineering improvements. For additional insights on building effective agent tools, see [Anthropic's comprehensive guide](https://www.anthropic.com/engineering/writing-tools-for-agents) on writing tools for agents. For those looking to dive deeper into RAG optimization, check out my posts on [RAG low-hanging fruit improvements](./rag-low-hanging-fruit.md) and [six key strategies for improving RAG](./rag-six-tips-improving.md).

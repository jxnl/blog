---
title: Why Most Document Parsing Sucks (Adit, Reducto)
speaker: Adit
cohort: 3
description: A conversation with Adit, CEO of Reducto, covering challenges of document ingestion, parsing tables and forms, hybrid CV + VLM pipelines, and optimizing representations for reliable AI systems.
tags: [document parsing, ingestion, Reducto, computer vision, VLM]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Why Most Document Parsing Sucks (Adit, Reducto)

I hosted a session with Adit, CEO of Reducto, to explore the challenges and solutions in document ingestion for AI systems. This conversation covered parsing complex documents, handling tables and forms, optimizing data representation for language models, and addressing the long tail of edge cases that make production-ready AI systems difficult to build.

<!-- more -->

[▶️ Discover Reducto's Document Parsing Secrets](https://maven.com/p/662e5f){: .md-button .md-button--primary}

## Why is accurate document parsing so critical for AI applications?

The fundamental challenge with document parsing isn't just extracting text - it's about providing high-quality inputs that enable language models to reason effectively. As Adit explained, "Models today, especially reasoning models, are incredible with reasoning on good data. What really ends up causing accuracy drifts is the long tail of cases."

When you pass documents directly to vision language models like GPT-4, they can fail in surprising ways - misreading tables, hallucinating content, or dropping information. These aren't necessarily model problems but input quality issues. The same models that struggle with raw documents can perform exceptionally well when given properly structured representations.

I've seen this pattern repeatedly in my consulting work - clients focus heavily on model selection and prompt engineering but underinvest in the quality of their document processing pipeline. This creates a ceiling on performance that no amount of prompt tuning can overcome.

**Key Takeaway:** Even the most advanced language models will produce unreliable outputs when given poor-quality inputs. Investing in robust document parsing is essential for production AI systems, especially in domains where accuracy is critical.

## What are the most challenging document elements to parse correctly?

Through their work with financial, legal, healthcare, and enterprise clients, Reducto has identified several consistently problematic document elements:

Hard tables - Especially those with merged cells, complex layouts, or that span multiple pages
Layout interpretation - Understanding indentation, list hierarchies, and associating related blocks of content
Form regions - Pairing key-value relationships (like knowing "Jason Liu" maps to "Name")
Reading order - Determining the correct sequence in multi-column layouts, slide decks, or documents with non-standard flows

Tables are particularly challenging because they represent two-dimensional associations of data that can be formatted in countless ways. The failures are often subtle - a model might extract what appears to be a valid table but silently drop rows, columns, or individual values.

What's particularly concerning is how these errors can be difficult to detect in production. Adit showed examples where vendor solutions using Gemini, Claude, and other models produced outputs that looked structurally correct but contained hallucinated values or missing data.

**Key Takeaway:** The most challenging parsing problems involve understanding document structure rather than just text extraction. Tables, forms, and complex layouts require specialized approaches beyond what general-purpose vision models can reliably handle.

## When should you use vision language models versus traditional computer vision?

I found Adit's perspective on this particularly interesting because it challenges the "just throw it all into a VLM" approach I've seen many teams adopt. Reducto has found that a hybrid approach works best:

Traditional CV excels at:

- Clean, structured information
- Providing precise bounding boxes
- Generating confidence scores
- Token-efficient processing

Vision language models excel at:

- Handwriting recognition
- Chart extraction
- Understanding figures and diagrams
- Handling visually complex layouts

"What we do see as a really effective place to use VLMs is things that traditional OCR has always been horrible at," Adit explained. For example, when Reducto first approached chart extraction, they tried using traditional CV to measure pixel values relative to axis labels. This approach failed because charts can be represented in so many different ways that VLMs simply perform better.

Their most effective approach uses a multi-pass system: traditional CV for the initial extraction, followed by VLMs that grade the outputs and make corrections. This allows them to triage simple pages to lightweight models while deploying more powerful VLMs only for complex cases.

**Key Takeaway:** Rather than choosing between traditional CV and VLMs, build a pipeline that leverages the strengths of each approach. Use traditional CV for structured content and VLMs for visually complex elements, with a multi-pass system to catch and correct errors.

## How should you evaluate document parsing performance?

Evaluation emerged as a critical but often overlooked aspect of building document processing systems. Adit emphasized that the biggest mistake teams make is conducting "back of the napkin" tests with just a few hard documents before moving to production.

This approach is dangerous because ingestion errors get magnified downstream in retrieval and inference steps. Without thorough evaluation of each component, it becomes impossible to isolate where problems originate.

Reducto's approach includes:

- Creating benchmarks with diverse, hand-labeled examples (they've open-sourced RD Table Bench with 1,000 diverse cases)
- Developing scoring frameworks that evaluate both text accuracy and structural correctness
- Recommending that teams compile 100-200 hard cases from their specific document distribution

What struck me is how this evaluation process isn't just about measuring performance - it's about understanding failure modes. The examples Adit showed revealed how models can fail in ways that look correct at first glance but contain subtle errors that would be catastrophic in sensitive domains.

**Key Takeaway:** Invest in rigorous evaluation of your document processing pipeline using representative examples from your domain. Test each component separately to isolate errors, and focus on understanding failure modes rather than just overall accuracy.

## What's the best way to represent document data for language models?

The ideal output structure depends heavily on the type of document you're processing. For simple content, Markdown provides a clean, token-efficient representation. But for complex structures like tables with merged cells, HTML often works better despite being more verbose.

Reducto has developed specific heuristics based on document complexity:

- For tables with 3+ merged cells, they use HTML
- For simpler tables, they use Markdown for token efficiency
- For figures and visual elements, they sometimes preserve the original image region

This approach recognizes that different document elements have different optimal representations. As Adit explained, "If you have a table like this, if you try to encode this in Markdown, you're going to end up with something really cumbersome."

I've seen similar issues in my consulting work - teams often standardize on a single representation format without considering how it handles different document types. This one-size-fits-all approach creates unnecessary challenges for the language model.

**Key Takeaway:** Choose representation formats based on document complexity rather than standardizing on a single approach. Consider token efficiency, structural fidelity, and how well the format preserves the information needed for reasoning.

## How should you approach chunking documents for retrieval?

While chunking has become less critical as context windows have expanded, it remains important for efficient retrieval across large document collections. Adit shared several principles that have proven effective:

1. Never split individual blocks of information (keep paragraphs, tables, and other logical units intact)
2. Consider both semantic information and structural signals like section headers and position
3. Dynamically adjust chunk sizes rather than enforcing rigid token limits

What I found particularly interesting was Adit's observation about position as a signal: "Position is a surprisingly high value signal for chunking because humans inherently, when we create documents, encode things like grouping similar text together."

This insight aligns with my experience - document authors naturally organize related information spatially, making position a strong proxy for semantic relatedness that's computationally cheap to extract.

**Key Takeaway:** Develop a chunking strategy that preserves logical document units and leverages both semantic and structural signals. Position within the document often provides valuable information about content relationships.

## How do you optimize document data for retrieval?

One of the most valuable insights from our conversation was recognizing that embedding models and LLMs have different limitations that your ingestion pipeline should account for.

While LLMs can reason effectively with dense HTML structures, embedding models often struggle with them. As Adit explained, "If you had a table that contains revenue over time, your end user is probably going to say something like, 'How did revenue change over time?' They're probably not going to phrase the question as 'In fiscal year 14, how did the number change from 210 to something else?'"

This creates a mismatch between user queries and document representations that naive cosine similarity can't bridge. Reducto addresses this by creating embedding-optimized representations for each chunk:

- Generating natural language summaries of table contents
- Adding context about document sections
- Creating modified representations specifically optimized for embedding similarity

I've seen similar approaches work well in my consulting projects - creating "retrieval-friendly" versions of complex document elements that maintain the semantic meaning while being more aligned with how users phrase queries.

**Key Takeaway:** Create separate representations optimized for embedding models and LLMs. For complex elements like tables, generate natural language summaries that describe the content in ways that align with likely user queries.

## What are the unique challenges of processing Excel files?

While much of the discussion focused on PDFs, Adit shared fascinating insights about Excel processing that I hadn't considered before. The challenges are quite different from PDFs:

1. Scale issues - Spreadsheets can contain hundreds of thousands of rows, easily exceeding model context windows
2. Information clustering - A single spreadsheet might contain multiple unrelated tables with arbitrary spacing between them
3. Header preservation - When chunking large tables, headers need to be repeated with each section

Reducto's approach includes breaking large tables into smaller chunks with headers preserved, and using a combination of data density analysis and visual information to identify separate clusters of information within a sheet.

What I found most interesting was their experimental work on using vision models specifically for spreadsheet clustering: "We are training a vision model specifically for spreadsheet clustering. And we've just found that that works better."

This highlights how specialized the solutions need to be for different document types - the techniques that work for PDFs often don't transfer directly to spreadsheets.

**Key Takeaway:** Excel processing requires specialized approaches that address scale challenges and information clustering. Consider using visual representations to identify logical groupings within spreadsheets rather than relying solely on cell-based analysis.

## What surprising edge cases have emerged in document processing?

Some of the most interesting insights came from discussing unexpected challenges that only became apparent through extensive production experience:

- Minor skews (1-2 degrees) can dramatically impact extraction quality, even with VLMs
- Reading order determination is far more complex than anticipated, especially with multi-column layouts
- Watermarks can confuse models and corrupt extracted text
- Model refusals occur when content appears to violate safety guidelines (like medical prescriptions)
- Checkboxes are surprisingly difficult for VLMs to interpret consistently

The checkbox issue is particularly problematic in healthcare: "Checkboxes are one of the things that I see vision language models out of the box struggle with the most... They'll sort of arbitrarily decide whether or not the checkbox is filled or not. Those are like complete bipolar meanings - you can't say, was the patient vaccinated yes or no, and choose arbitrarily with 50-50 probability."

These edge cases highlight the gap between demo-quality and production-quality systems. While models might handle 95% of cases well, the remaining 5% often require specialized solutions.

**Key Takeaway:** Production document processing systems need to address a long tail of edge cases that aren't apparent in initial testing. Invest in preprocessing, confidence scoring, and fallback mechanisms to handle these challenging scenarios.

## How is document processing evolving with newer AI capabilities?

Throughout our conversation, Adit shared perspectives on how document processing is likely to evolve:

- VLMs will continue improving but aren't yet reliable enough for sensitive use cases without additional safeguards
- Agentic approaches are emerging that can reason about what information to extract and how to structure it
- Multi-pass systems that combine traditional methods with AI verification show promise for high-accuracy applications
- Evaluation remains critical and will likely become more sophisticated as applications mature

I was particularly interested in Adit's thoughts on agentic RAG, where models reason about what information to retrieve rather than relying solely on embedding similarity: "The cases where it is really helpful is when a given answer needs to be composed of information from a lot of different sources."

This aligns with my experience - as we move beyond simple question-answering to more complex reasoning tasks, the limitations of traditional retrieval become more apparent.

**Key Takeaway:** Document processing is evolving toward more intelligent, multi-stage pipelines that combine traditional methods with AI reasoning. While VLMs will continue improving, hybrid approaches that leverage the strengths of different techniques will likely remain dominant for production systems.

## How should teams approach building document processing systems?

Based on our conversation, I'd recommend several principles for teams building document processing systems:

1. Use a hybrid approach combining traditional CV and VLMs based on document characteristics
2. Invest heavily in evaluation using representative examples from your domain
3. Choose representation formats based on document complexity rather than standardizing on one approach
4. Create separate representations optimized for embedding models versus LLMs
5. Build multi-pass systems that can verify and correct initial extraction results
6. Develop specialized approaches for different document types (PDFs, Excel, forms, etc.)
7. Focus on understanding and addressing the long tail of edge cases

The most successful teams I've worked with treat document processing as a critical foundation rather than just a preprocessing step. They recognize that the quality of their document understanding directly impacts everything downstream.

As Adit summarized: "Accurate parsing is really critical. You should try to use the best tools that are available for you... The best way to do that is to use a combination of both traditional CV for the things that traditional CV is good at, and also VLMs and document metadata."

**Key Takeaway:** Document processing requires a thoughtful, multi-faceted approach that combines different techniques based on document characteristics. Invest in this foundation to enable reliable, accurate AI applications, especially in domains where precision matters.

---

## FAQs

**What is document ingestion in the context of AI applications?**

Document ingestion refers to the process of extracting, processing, and structuring data from various document formats (like PDFs, Excel files, images) so they can be effectively used by AI models. This includes parsing text, understanding document structure, recognizing tables, and preparing the data in a format that language models can reason with accurately.

**Why is accurate document parsing so important for AI applications?**

Accurate parsing is critical because even the most advanced AI reasoning models can only provide quality outputs when given quality inputs. Inaccurate parsing leads to hallucinations, missing information, or incorrect interpretations. In sensitive industries like healthcare, finance, and legal, even minor errors in document parsing can have significant consequences, potentially impacting decisions worth millions of dollars.

**What are the main challenges in document parsing?**

The most common challenges include:

- Extracting complex tables with merged cells
- Interpreting document layout correctly (indentation, list hierarchies)
- Pairing form fields with their values
- Determining the correct reading order, especially in multi-column layouts
- Processing handwritten text
- Handling charts and figures
- Managing document skew and rotation
- Working with multilingual documents that have different reading directions

**How do Vision Language Models (VLMs) compare to traditional OCR for document parsing?**

VLMs excel at tasks that traditional OCR struggles with, such as handwriting recognition and chart extraction. However, they can sometimes hallucinate content or drop information in structured formats like tables. The most effective approach is often a hybrid one, using traditional computer vision models for clean structured content and VLMs for more complex visual elements like figures, handwriting, and charts.

**What's the best approach for handling tables in documents?**

Tables require special attention because they associate data in two dimensions. The most effective approach involves:

1. Properly detecting the table structure including merged cells

2. Preserving the relationships between headers and data

3. Using HTML format for complex tables with multiple merged cells

4. Using Markdown for simpler tables to maintain token efficiency

5. Creating natural language summaries of tables to improve retrieval

**How should document data be represented for language models?**

The ideal representation depends on the content:

- Simple text works well in Markdown format
- Complex tables with merged cells are better represented in HTML
- Large tables may need to be broken down with headers repeated for each section
- Images and figures are sometimes best left as cropped images passed directly to the model
- For forms, it's important to pair keys with their values

**What are best practices for chunking documents?**

Effective chunking strategies include:

- Never splitting individual blocks of information (keeping paragraphs and tables intact)
- Considering section information and position when creating chunks
- Using embedding similarity to group related content
- Dynamically adjusting chunk size based on content type rather than using fixed sizes
- Preserving document structure and hierarchy

**How can document ingestion be optimized for retrieval?**

To improve retrieval performance:

- Create embedding-optimized representations for each chunk
- For tables, generate natural language summaries describing the content
- Add context about document sections
- Include metadata that helps tie document data to potential user queries
- Consider how users actually phrase their questions rather than just the literal content

**Why do embedding models and language models need different optimizations?**

Embedding models and language models have different limitations. While language models can reason through complex HTML structures, embedding models may struggle with matching user queries to content that contains mostly HTML tags and numbers. Creating natural language descriptions of structured content helps bridge this gap and improves retrieval performance.

**How should document parsing quality be evaluated?**

Evaluation should be thorough and context-dependent:

- Test on your own data rather than generic benchmarks
- Develop a comprehensive evaluation framework with at least 100-200 hard cases
- Evaluate both text accuracy and structural preservation
- Test each component of your pipeline separately to isolate issues
- Consider edge cases specific to your document types

**What are common failure modes in document parsing?**

Common failures include:

- Hallucinating content in tables
- Dropping rows or columns
- Misinterpreting checkboxes and form elements
- Struggling with document skew or rotation
- Incorrectly determining reading order in complex layouts
- Model refusals when content appears to violate safety guidelines
- Watermarks interfering with text extraction

**How should Excel files be handled differently from PDFs?**

Excel files present unique challenges:

- They can contain massive amounts of data exceeding model context windows
- A single spreadsheet may contain multiple unrelated tables or data clusters
- Data representation isn't always in a clean grid format
- Effective approaches include:
- Breaking large tables into smaller chunks with headers repeated
- Using visual information to detect natural clusters of data
- Analyzing data density to identify separate information regions

**How can handwritten documents be processed effectively?**

Handwritten documents are best processed using VLMs, which perform much better than traditional OCR for this task. For particularly difficult cases, a multi-pass approach works well:

1. Make an initial prediction

2. Use a VLM specifically fine-tuned to grade those outputs

3. Use another VLM to make corrections based on the reasoning trace

This approach significantly improves accuracy for handwritten content.

**How much data is needed to fine-tune models for document extraction?**

Fine-tuning VLMs for document extraction tasks can be effective with hundreds to perhaps a thousand examples. However, the quality of the training data is far more important than quantity. Even minor issues in labels can be amplified during fine-tuning, so it's critical to have genuinely perfect inputs rather than a large volume of imperfect data.

**What's the role of "agentic RAG" in document processing?**

Agentic RAG involves adding reasoning capabilities to determine what information to pass to the final inference step. This approach is particularly valuable when answers need to be composed from multiple different sources. Rather than relying solely on similarity-based retrieval, an agent can identify which specific snippets are most relevant to answering a particular question.

---

--8<--
"snippets/enrollment-button.md"
--8<--

---

---
title: "Encoder Stacking and Multi-Modal Retrieval (Daniel, Superlinked)"
speaker: Daniel
cohort: 3
description: "Guest lecture with Daniel from Superlinked on improving retrieval systems using specialized encoders for different data types, moving beyond text-only embeddings"
tags:
  [
    encoder stacking,
    multi-modal retrieval,
    specialized encoders,
    Superlinked,
    recommender systems,
    data types,
  ]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Encoder Stacking and Multi-Modal Retrieval (Daniel, Superlinked)

I hosted a special session with Daniel from Superlinked to explore how we can improve retrieval systems by applying lessons from recommender systems. This conversation revealed critical insights about the limitations of current search approaches and how to build more sophisticated retrieval architectures that handle diverse data types beyond just text.

<!-- more -->

[▶️ Master Multi-Modal Retrieval Techniques](https://maven.com/p/56f424){: .md-button .md-button--primary}

**Why traditional retrieval systems fall short for complex queries**

When we look at complex queries like "popular family-friendly hotels with good Wi-Fi near Manhattan midtown under $400," traditional retrieval systems struggle because they're trying to handle multiple types of data with tools designed primarily for text.

Each component of this query represents either a bias (steering results toward certain attributes) or a filter (binary yes/no conditions):

- "Popular" is a numerical bias
- "Family-friendly" is a categorical bias
- "Good Wi-Fi" is a semantic bias found in reviews
- "Near Manhattan midtown" is a location bias
- "Under $400" is a price filter

If your toolkit is just a text embedding model, it simply can't understand these different data types effectively. The current approach using text-to-SQL or similar query generation has significant limitations in latency, reliability, and handling non-textual inputs like user clicks or contextual parameters.

**_Key Takeaway:_** Complex queries contain multiple data types that text embedding models alone can't properly understand. We need specialized approaches for handling numerical, categorical, location, and other non-textual data.

**Three fundamental problems with current search systems**

I've observed that even if you generate the perfect query, today's search systems have three fundamental flaws:

1. Overuse of filters instead of biases
   When users say "near Manhattan midtown," they don't mean "exactly within X kilometers" - they have a preference that gradually decreases with distance. But systems typically implement this as a hard Boolean filter (a step function) rather than a smooth bias (a sigmoid function), creating an artificial cutoff that excludes potentially excellent results.
2. Reliance on re-ranking as a hack
   Re-ranking exists because our underlying retrieval is inadequate. If retrieval worked properly, you wouldn't need to shuffle results afterward. The problem is that re-ranking only applies to a tiny fraction of your database (typically less than 1%), so whatever you miss in candidate selection can't be fixed through re-ranking.
3. Misuse of text embeddings for non-textual data
   People try to stringify everything (JSON objects, numbers, etc.) and feed it to text embedding models. This fundamentally doesn't work because these models understand numbers through co-occurrence in training data, not as actual numerical values. If you stringify integers and calculate similarities between their embeddings, there's no concept that "49 is one less than 50" in the latent space.

**_Key Takeaway:_** Current systems rely too heavily on Boolean filters instead of smooth biases, use re-ranking to compensate for poor retrieval, and misapply text embeddings to non-textual data. These fundamental issues limit search quality regardless of prompt engineering.

**A better approach: Mixture of encoders**

Instead of forcing everything through text embeddings, we should use specialized encoders for different data types and then combine their outputs. This "encoder stacking" or "mixture of encoders" approach works like this:

1. Break down the query into components using a DSPy-style optimized prompt
2. Feed each component to the appropriate specialized encoder:
   - Text to a text encoder
   - Numbers to a numerical encoder
   - Locations to a location encoder
   - User interactions to a graph encoder
3. Each encoder produces an embedding that natively understands its data type
4. Combine these embeddings with appropriate weights to create a final query vector
5. Add any necessary filter predicates for binary conditions
6. Send this to a vector database for retrieval

This approach compresses all biases into a single embedding while maintaining the ability to filter when absolutely necessary. The result is more accurate retrieval without needing extensive re-ranking or complex boosting logic.

**_Key Takeaway:_** By using specialized encoders for different data types rather than forcing everything through text embeddings, we can create retrieval systems that better understand user intent and produce higher quality results.

**The pilot that sees the world as strings**

One metaphor that really captures the current limitations is that language models are like "pilots that see the whole world as strings." This creates fundamental problems when dealing with non-textual data.

Consider how LLMs handle numbers - they don't truly understand numerical relationships. That's why they might think 3.11 is larger than 3.9, or struggle with basic arithmetic. This isn't just a minor issue but a gateway to a much deeper problem: we can't effectively stringify the world and expect models to understand it properly.

This limitation extends to graph-based approaches too. If you're using an LLM to navigate a graph where nodes have non-textual metadata, you're still forcing that data through a text-based understanding that fundamentally misrepresents its nature.

**_Key Takeaway:_** Language models fundamentally see everything as text, which creates inherent limitations when dealing with numerical data, location data, or other non-textual information. This "world as strings" problem requires specialized solutions.

**Practical implementation considerations**

When implementing these systems in production, several practical considerations emerge:

1. Refreshing embedding models
   With traditional approaches, distribution drift on any property forces you to retrain the entire model. With a mixture of encoders, you can selectively update individual components as needed, making maintenance more manageable.
2. Handling data updates
   If a hotel's popularity changes but its description doesn't, you don't need to re-encode the entire entity - just update the specific embedding signal for popularity and recombine it with the rest.
3. Sparse vs. dense representations
   The more efficient and dense your encoders, the worse they respond to aggregation. If you average several dense embeddings together, you often destroy information. More sparse encoders (closer to bag-of-words) handle aggregation better because they represent a union of features rather than a point in a compressed space.
4. Keyword-heavy queries
   For exact matches, you can either treat these as part of the filtering system or incorporate sparse representations alongside dense ones, depending on your vector database capabilities.

**_Key Takeaway:_** A modular approach with specialized encoders makes systems more maintainable, allowing selective updates to components affected by data drift rather than requiring complete retraining.

**What we're not asking about retrieval systems**

There are several critical issues that aren't getting enough attention in discussions about retrieval:

1. We need to look at the world through lenses beyond text tokenization
   Text is just one data type among many, and forcing everything through text encoders fundamentally limits what we can achieve.
2. Re-ranking is overused and often masks deeper problems
   Rather than fixing poor retrieval with re-ranking, we should improve the underlying retrieval to make re-ranking less necessary.
3. Boolean filters are poor approximations of user preferences
   Most user preferences are gradual rather than binary, but we implement them as hard filters that exclude potentially valuable results.

The future likely involves more sophisticated encoders that can handle diverse data types natively, but until then, we need to combine specialized encoders for different data types to get the maximum signal and control over our results.

**_Key Takeaway:_** The field needs to move beyond text-centric approaches, reduce reliance on re-ranking, and replace hard Boolean filters with smooth biases that better represent user preferences. This requires fundamentally rethinking how we encode and retrieve information.

---

FAQs

## What are the limitations of current search systems?

Most search systems today have three fundamental limitations. First, they overuse filters to approximate user preferences instead of using smoother bias functions. Second, they rely heavily on re-ranking, which is essentially a workaround for poor initial retrieval. Third, they misuse text embeddings by trying to encode non-textual data (like numbers) through text models, which creates inaccurate representations.

## How do traditional search systems handle complex queries?

Traditional systems typically use a text-to-SQL approach where they convert natural language queries into database queries. This process often struggles with non-textual inputs (like user clicks or contextual data), has latency issues, and can be unreliable when generating complex queries. The resulting search pipeline usually involves pre-filters, boosting, vector search, re-ranking, and post-filtering—a complicated process with many potential failure points.

## What's wrong with using text embedding models for all search needs?

Text embedding models understand the world as strings, which creates fundamental limitations. They process numbers by how they co-occur in training data rather than understanding their mathematical properties. For example, these models don't inherently understand that 49 is one less than 50 in their latent space. This makes them poorly suited for handling numerical data, location data, and other non-textual information that's critical in real-world search applications.

## What is encoder stacking (or mixture of encoders)?

Encoder stacking is an approach that uses specialized encoders for different types of data instead of relying solely on text encoders. It involves breaking down a query into components and routing each component to the appropriate specialized encoder—such as numerical encoders for popularity scores, location encoders for geographical data, or graph encoders for user interaction patterns. The outputs from these encoders are then aggregated into a final embedding that captures all relevant signals.

## How does encoder stacking handle a complex travel query?

For a query like "popular, family-friendly hotels with good Wi-Fi near Manhattan midtown under $400," encoder stacking would:

1. Route "popular" to a numerical encoder that creates a bias toward highly-rated properties

2. Send "family-friendly" to a categorical encoder that biases toward that attribute

3. Process "good Wi-Fi" through a semantic encoder that understands sentiment in reviews

4. Direct "near Manhattan midtown" to a location encoder that understands geographical proximity

5. Create a filter predicate for "under $400"

6. Combine all these signals into a single embedding that captures all these preferences

## What are the benefits of using specialized encoders?

Specialized encoders provide more accurate representations of different data types than text-only models. They allow for smoother bias functions rather than rigid filters, eliminate the need for re-ranking by getting better initial results, and handle non-textual data properly. This approach also makes it easier to update individual components when data distributions change, rather than retraining an entire model.

## How does Superlinked implement encoder stacking?

Superlinked provides an open-source framework that allows developers to create a system of specialized encoders. The framework includes components for query understanding, encoder routing, and result aggregation. It works with various vector databases (including Redis, MongoDB, and Quadrant) and provides APIs for building retrieval systems for RAG, recommendation systems, and search applications.

## How often do you need to refresh embedding models in this approach?

One advantage of encoder stacking is that you can selectively update individual encoders when their specific data distributions change, rather than retraining the entire system. This modular approach makes maintenance more manageable. You can also implement caching at the individual encoder level, allowing you to update only the affected parts of an embedding when certain attributes change.

## How do you handle keyword-heavy queries in this framework?

Keyword queries are typically handled through the filter component of the system. While sparse data structures (like traditional keyword search) could theoretically be integrated into the encoder framework, current vector databases are more optimized for handling these as filters. Superlinked uses the underlying sparse indexing capabilities (like BM25) of the database for keyword matching.

## How should encoders be designed and combined?

Encoders should be designed to produce dense vector representations of their specific input types. These outputs are then aggregated—typically by normalizing each encoder's output and concatenating them dimension-wise into a larger vector. This approach preserves the signal from each encoder in separate dimensions, which helps with explainability and allows for query-time weighting of different signals.

## Will text models eventually replace specialized encoders?

While large companies with massive data might be able to train transformers that outperform specialized encoders, most organizations benefit from having a toolkit that allows them to build systems specific to their needs. Until we reach true AGI, specialized encoders will likely remain valuable for handling non-textual data types and providing more control over search results.

## What should we be focusing on to improve search systems?

## We should focus on three key areas: 1) Looking at the world through lenses beyond text tokenization, 2) Reducing our reliance on re-ranking by improving initial retrieval, and 3) Using smooth bias functions instead of rigid Boolean filters. These approaches will lead to more accurate, efficient, and controllable search systems.

--8<--
"snippets/enrollment-button.md"
--8<--

---

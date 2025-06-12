---
title: "Fine-Tuning Embedding Models for Enterprise RAG: Lessons from Glean"
date: 2025-03-06
description: "A deep dive into the challenges and best practices for fine-tuning embedding models in enterprise RAG systems, based on insights from Manav Rathod of Glean."
author:
  - jxnl
comments: true
---

# Fine-Tuning Embedding Models for Enterprise RAG: Lessons from Glean

!!! note "Systematically improving RAG systems"

    This transcript is based off of a guest lecture given in my course, [Systematically Improving RAG Applications](../../systematically-improve-your-rag.md)

<iframe width="560" height="315" src="https://www.youtube.com/embed/jTBsWJ2TKy8" title="Fine-Tuning Embedding Models for Enterprise RAG: Lessons from Glean" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Retrieval-Augmented Generation (RAG) systems have become essential tools for enterprises looking to harness their vast repositories of internal knowledge. While the theoretical foundations of RAG are well-understood, implementing these systems effectively in enterprise environments presents unique challenges that aren't addressed in academic literature or consumer applications. This article delves into advanced techniques for fine-tuning embedding models in enterprise RAG systems, based on insights from Manav Rathod, a software engineer at Glean who specializes in semantic search and ML systems for search ranking and assistant quality.

The discussion focuses on a critical yet often overlooked component of RAG systems: custom-trained embedding models that understand company-specific language, terminology, and document relationships. As Jason Liu aptly noted during the session, "If you're not fine-tuning your embeddings, you're more like a Blockbuster than a Netflix." This perspective highlights how critical embedding fine-tuning has become for competitive enterprise AI systems.

<!-- more -->

## The Enterprise RAG Challenge

Enterprise data differs fundamentally from internet data in several key ways that affect how we build and fine-tune embedding models:

1. **Heterogeneous Data Sources**: Enterprise data spans numerous applications and formats—from Google Drive and Confluence documents to Slack messages, meeting transcripts, and GitHub pull requests. Each requires different handling strategies.

2. **Company-Specific Language**: Every organization develops its unique terminology, acronyms, project names, and language patterns that general-purpose embedding models won't understand without specific training.

3. **Evolving Knowledge**: Enterprise knowledge changes constantly. New projects emerge, old ones become obsolete, and terminology shifts. Embedding models must adapt to these changes.

4. **Security and Privacy Constraints**: Enterprise data is sensitive and often cannot be directly accessed for model training purposes, creating challenges for data preparation.

5. **Lack of Labeled Data**: Unlike consumer applications with abundant user interaction data, enterprise systems often start with little to no labeled data for training.

## When to Fine-Tune Embedding Models

A key question practitioners face is determining when embedding fine-tuning is necessary versus using out-of-the-box models. According to Manav, fine-tuning becomes essential when:

1. **Your users employ company-specific terminology** that general models won't understand
2. **Search quality metrics plateau** despite improvements in other system components
3. **You have sufficient company-specific data** to make fine-tuning effective
4. **Different query patterns emerge** that standard models don't handle well

While some scenarios can be addressed through retrieval strategies like query expansion or re-ranking, embedding fine-tuning becomes unavoidable when the semantic gap between general language and company-specific language is significant. As one attendee aptly phrased it, "look at your data!" — understanding your specific use case is crucial for determining when fine-tuning is necessary.

## Glean's Approach to Embedding Fine-Tuning

Glean builds custom embedding models for each of their customers, recognizing that one-size-fits-all approaches don't work for enterprise search. Their process involves multiple stages:

### 1. Continued Pre-Training with Masked Language Modeling

The foundation of Glean's approach begins with continued pre-training of base models (typically BERT-based) using masked language modeling (MLM) on company-specific corpora. This technique has been proven effective for domain adaptation for many years.

The process works by:

- Taking sentences from the company's corpus
- Blanking out certain words
- Training the model to predict the masked words

This forces the model to develop a nuanced understanding of both general English and company-specific language. The technique is especially effective when carefully selecting which words to mask, focusing on domain-specific terms.

MLM is particularly valuable in enterprise settings because:

- It can utilize all text data without requiring labels
- It works effectively regardless of corpus size
- It adapts the model to understand company jargon, product names, and internal terminology
- It enables the model to incorporate new vocabulary specific to the business into the embedding space, integrating it with the dimensions of the pre-trained BERT model

### 2. Converting Language Models to Embedding Models

While masked language modeling helps the model understand company language, it doesn't necessarily optimize embeddings for search tasks. To create effective search embeddings, Glean uses several techniques to generate training pairs:

#### Title-Body Pairs

One effective approach is creating "title-body" pairs that map document titles to passages from the document body. This provides a weak but useful training signal since titles typically relate semantically to the content they describe.

#### Anchor Data

Drawing inspiration from Google's PageRank, Glean leverages document references as signals for relevance. When one document links to another, they likely share semantic relationships. These connections can be used to create pairs for training:

- Titles of documents that reference each other
- Context around the anchor text paired with the referenced document

#### Co-Access Patterns

When users research a topic, they often access multiple related documents in a short time window. This "co-access" pattern provides valuable signals about document relationships. Glean captures these patterns by creating positive pairs from documents accessed together by the same user within a time threshold.

#### Public Datasets

While company-specific data is crucial, public datasets still provide value. Glean incorporates established datasets like MS MARCO to ensure models maintain general language understanding while adding company-specific knowledge.

### 3. Handling Application-Specific Data

Different application data requires specialized processing to extract high-quality training pairs. For example, Slack messages present unique challenges:

- Individual messages often lack context and are too short to be meaningful
- Messages don't have titles, making title-body pairing difficult
- Not all channels contain equally valuable information

Glean addresses these challenges by:

- Creating "conversation documents" from message threads or time-based clusters
- Using the first message as a proxy for a title when needed
- Filtering out low-value channels (e.g., "random" or "happy birthday" channels)
- Leveraging emoji reactions as relevance signals—messages with 👍 or similar positive reactions can be treated as "answers" or high-quality responses, creating additional training pairs

Understanding these application-specific nuances is critical for creating high-quality training data. As emphasized in the discussion, there's no substitute for deeply examining your data and understanding user behaviors before designing training strategies.

### 4. Leveraging Synthetic Data

For smaller corpora or when starting with new customers, Glean uses large language models (LLMs) to generate synthetic question-answer pairs:

- LLMs analyze documents and generate potential questions users might ask
- Careful prompt engineering ensures questions resemble actual user queries rather than just reformatting document text
- Generation focuses on popular, high-value documents to maximize return on compute costs

This approach provides "infinite" training data but requires careful implementation:

- Prompts must encourage variation in wording rather than exact matches
- Generated questions should account for how users actually phrase queries (using acronyms, omitting details, etc.)
- Questions should cover diverse query patterns, not just simple factoid questions

### 5. Learning from User Feedback

The most valuable training signal comes from actual user interactions. Glean leverages several feedback mechanisms:

#### Search Interactions

In their search product, click data provides direct relevance signals. When users search and click on results, these query-document pairs become valuable training data.

#### RAG Assistant Feedback

For RAG-only scenarios (like their Glean Assistant), feedback collection is more challenging. Approaches include:

- Upvote/downvote systems (though engagement is typically sparse)
- Citation clicks (when users click to read source documents)
- Follow-up question patterns

These signals may be individually weak, but combined across many interactions, they provide valuable training data.

#### Creative Feedback Collection

Improving user engagement with feedback mechanisms remains an ongoing challenge. During the discussion, innovative approaches were suggested, such as gamifying the feedback experience: "Instead of passive thumbs up/down, a ball drops, and users steer it into 'good' or 'bad' buckets—actively engaging with feedback." Such creative approaches can increase the quantity of feedback signals available for model improvement.

## Query Pattern Recognition

An important aspect of embedding fine-tuning involves recognizing different query patterns. As mentioned during the discussion, queries often fall into categories like:

- **Factoid questions**: Seeking specific pieces of information
- **Enumeration queries**: Requesting lists of items (e.g., "What are all the projects in the finance department?")
- **Inventory queries**: Looking for assets like meetings, presentations, etc.
- **Navigational queries**: Trying to find specific documents

Training embedding models to recognize these patterns and handle them accordingly leads to more effective retrieval. This often requires creating synthetic examples that represent each pattern and fine-tuning the model to recognize the underlying intent behind different query structures.

## Evaluating Embedding Models

Evaluating embedding models in enterprise settings presents unique challenges, particularly when dealing with hundreds of customer-specific models and limited data access. Glean's approach emphasizes:

### Focused Unit Testing

Rather than relying solely on end-to-end evaluation, Glean builds targeted evaluations for specific capabilities:

- Paraphrase recognition: Testing whether models recognize different phrasings of the same question
- Entity resolution: Testing recognition of company-specific entities and terms
- Document relevance: Testing retrieval performance for key documents

This "unit testing" approach helps identify specific weaknesses in models and provides clear targets for improvement.

### User Satisfaction Metrics

Beyond technical evaluations, Glean tracks business outcomes:

- Session satisfaction: What percentage of search sessions end with users finding relevant documents?
- Usage metrics: Are users increasing their engagement with the system?
- Explicit feedback: Upvote/downvote ratios and trends

### LLM-Based Evaluation

For certain aspects of system performance, Glean employs LLM-based judges to evaluate response quality along dimensions like:

- Factuality
- Relevance
- Context usage
- Correctness

These evaluations help identify improvements or regressions when making system changes.

## Handling Enterprise-Specific Challenges

### Document Supersession

One common challenge in enterprise settings is determining when documents have been superseded by newer information. Glean approaches this through a concept they call "authoritativeness," which considers:

- Recency: When was the document last updated?
- References: Do other documents link to this one as an authoritative source?
- User interactions: Do users still find and engage with this document?

Documents like WiFi passwords might be old but remain authoritative if they're still regularly accessed and referenced. This was highlighted as "one of the hardest aspects of enterprise RAG" during the discussion, requiring both algorithmic solutions and human judgment.

### Security and Privacy

Working with sensitive enterprise data requires strict security protocols. Glean emphasizes:

- A unified data model that maintains security boundaries
- Customer-specific models that don't share data between organizations
- Careful handling of permissions (ACLs) to ensure retrieved content respects access controls

Regarding ACL (Access Control List) handling, Manav clarified that access controls are applied post-retrieval rather than pre-filtering the corpus. This allows the system to consider all documents during retrieval and then filter results based on the user's permissions before presenting them, maintaining both relevance quality and security compliance. This approach requires careful integration with existing permission systems and strict security validation to ensure no unauthorized access occurs.

## Lessons Learned and Best Practices

From Glean's experience, several best practices emerge for fine-tuning embedding models in enterprise RAG systems:

1. **Unified Data Modeling is Critical**: Building a consistent schema across heterogeneous data sources enables systematic training and evaluation.

2. **Creative Data Generation Matters**: Finding ways to extract training signals from existing data is often more valuable than collecting new annotations.

3. **User Feedback is Gold**: Even sparse signals from real users outperform synthetic data when available.

4. **Understand User Query Patterns**: Different types of queries require different optimization approaches; understanding these patterns enables targeted improvements.

5. **Isolate Components for Improvement**: Rather than optimizing end-to-end performance, focus on improving specific components with clear metrics.

6. **Don't Overlook Traditional Search Techniques**: Basic signals like recency and exact matching still solve 60-70% of enterprise search queries; semantic search should complement, not replace these approaches.

7. **Continuous Learning is Essential**: Models should be regularly retrained (monthly for Glean) to adapt to evolving company knowledge and terminology.

8. **Look at Your Data**: This simple but powerful advice was emphasized repeatedly—there's no substitute for deeply understanding your specific data and use cases.

## Conclusion

Fine-tuning embedding models for enterprise RAG represents a unique set of challenges distinct from both academic research and consumer applications. Glean's approach demonstrates that success requires a sophisticated multi-stage training process that combines continued pre-training, creative data pair generation, synthetic data, and user feedback signals.

The most effective systems combine the strengths of traditional search techniques with the power of semantic search, rather than relying exclusively on embedding-based retrieval. As Manav Rathod noted, "Using traditional basic search techniques and using these traditional signals is super important, and it'll never be outdated. Any system that doesn't use that is a questionable search system."

For practitioners building enterprise RAG systems, this underscores the importance of a pragmatic approach: fine-tune embeddings to understand company-specific language, but don't abandon proven information retrieval techniques that continue to provide value.

## Advanced Topics and Implementation Considerations

The following section explores advanced topics and practical implementation considerations for teams building enterprise RAG systems with fine-tuned embeddings. These insights combine direct statements from Manav Rathod with general industry practices.

### Data Freshness vs. Model Stability

**Challenge**: Enterprises face a trade-off between keeping embedding models up-to-date with evolving terminology and the computational cost of re-indexing large document collections.

**Manav's Approach**: Glean retrains their models on a monthly basis, which provides a good balance for most enterprise environments. As Manav explained:

> "We do things on a monthly basis. I think it does really just depend on the company whether or not that makes the most sense... because I think it's very rare where, like a brand new concept appears and become super important in the company, like over just the span of a week, or even a month, depending on the size of the company."

When models are updated, Glean completely re-indexes all content rather than attempting to maintain vector stability across versions. This ensures consistent quality but requires efficient infrastructure for regular re-indexing.

**Industry Practices**: Beyond what was explicitly discussed, many organizations implement:

- Incremental embedding updates for new or changed documents
- Importance-based prioritization focusing on frequently accessed content
- Vector database partitioning to update segments independently

### Evaluation at Scale

**Challenge**: Evaluating embedding models in enterprise settings presents unique challenges, particularly when dealing with hundreds of customer-specific models and limited data access.

**Manav's Approach**: Glean builds "unit tests" for their models to evaluate specific behaviors and capabilities:

> "We unit test our code. We also unit test our models in a lot of ways. An example of this is that you want to pick out behaviors of a model that you find desirable, and build an Eval set for them and make sure a model is kind of doing well on that particular type of query stream."

Manav emphasized testing specific capabilities like paraphrase understanding:

> "A good semantic search model should be really good at paraphrasing. I understand that paraphrases of the same sentence or a particular query, are actually mean the exact same thing."

For generating evaluation data, Manav suggested using existing datasets or LLMs:

> "You can take examples of queries, or like existing data sets of like paraphrases of like sentences. Or you can use LMs to create more of them on your own."

Glean also uses A/B testing with LLM judges to evaluate system improvements:

> "You can do a simple AB test like you ask hundreds of questions based on what users previously asked, and then with you using your old system and then on your new system, and you can use like a simple judge framework broken down, based on these different subcategories."

**User Satisfaction Metrics**: Beyond technical evaluations, Glean tracks business outcomes:

> "For search, where the main thing we look at is like this notion of session satisfaction, like, essentially, when user ask a question or they start searching for something. What percent of the time do they find a relevant document based on their click patterns?"

### Security and Privacy Considerations

**Challenge**: Working with sensitive enterprise data requires strict security protocols.

**Manav's Observations**: Manav highlighted the challenges of evaluating models when you can't directly access customer data:

> "It becomes particularly challenging in the enterprise setting where you don't have access to your customer data, and you have enterprise, specific models for each of your customers."

For evaluation without accessing data directly, Manav mentioned using closed-loop environments with LLMs:

> "If within a closed loop environment where you use an LLM to judge the quality of your responses, you can get a lot of useful signal out of that for understanding if you're making improving things."

**ACL Handling**: Regarding access control, Manav clarified that security is applied post-retrieval rather than pre-filtering the corpus, allowing the system to consider all documents during retrieval and then filter results based on permissions.

### Application-Specific Data Processing

**Challenge**: Different data sources require specialized processing to extract high-quality training pairs.

**Manav's Approach**: For Slack messages, which present unique challenges, Manav suggested:

> "Instead of thinking about individual messages as documents, think about like threads as documents, or like a time span of messages as a document."

As noted in the chat log, emoji reactions can provide valuable signals:

> "Users emoji (thumbs up) responses that are 'answers' or high quality responses. Use that as signal for positive pairs."

For PDFs and other visual content, Manav mentioned:

> "PDFs are probably the main source of like images or image, like data that we have in the enterprise... There's a variety of different like, pretty powerful out of the box tools you have for, like PDF parsing, and we mainly leverage those. But we primarily work in the textual space because that's just kind of where most enterprise data lives."

### Document Supersession and Relevance

**Challenge**: One common challenge in enterprise settings is determining when documents have been superseded by newer information.

**Manav's Insights**: When asked about handling outdated documents, Manav explained:

> "We have this notion of like authoritativeness... like, how authoritative is this document? And that's based on a lot of different signals. Like, how many people reference this document? How many people look at this document? How recent is this document?"

He provided a practical example:

> "A good example is like a WiFi password document. It might be really old, but it's still the WiFi password document. And so it's still authoritative, even if it's old."

This was highlighted in the chat as "one of the hardest aspects of enterprise RAG."

### Balancing Traditional and Semantic Search

**Challenge**: Development teams must decide how to balance embedding-based retrieval with traditional search techniques.

**Manav's Perspective**: Manav emphasized the importance of isolating and improving individual components:

> "Isolating and improving individual components of your RAG system altogether is always going to be the best way to kind of move forward... if you want to really make good, tangible progress, like day by day, isolating and optimizing individual components, is always going to be like much more scalable than trying to improve everything altogether all at once."

In previous sections, he stressed that traditional search techniques remain essential and that "any system that doesn't use that is a questionable search system."

## Conclusion

Fine-tuning embedding models for enterprise RAG represents a unique set of challenges distinct from both academic research and consumer applications. Glean's approach demonstrates that success requires a sophisticated multi-stage training process that combines continued pre-training, creative data pair generation, synthetic data, and user feedback signals.

The most effective systems combine the strengths of traditional search techniques with the power of semantic search, rather than relying exclusively on embedding-based retrieval. As Manav Rathod noted, "Using traditional basic search techniques and using these traditional signals is super important, and it'll never be outdated. Any system that doesn't use that is a questionable search system."

For practitioners building enterprise RAG systems, this underscores the importance of a pragmatic approach: fine-tune embeddings to understand company-specific language, but don't abandon proven information retrieval techniques that continue to provide value.

## Questions to Consider

1. **When should you fine-tune embeddings vs. using out-of-the-box models?**

   - Consider fine-tuning when your users employ company-specific terminology that general models won't understand
   - Look for plateaus in search quality metrics despite improvements in other system components
   - Ensure you have sufficient company-specific data to make fine-tuning effective
   - As Manav emphasized: "Look at your data!" Understanding your specific use case is crucial

2. **How can you generate high-quality training data in enterprise settings?**

   - Leverage document structure (title-body pairs)
   - Analyze document references and links (anchor data)
   - Study user behavior (co-access patterns)
   - Use synthetic data generation with LLMs
   - Collect and learn from user feedback

3. **What evaluation strategies work best for enterprise embedding models?**

   - Build targeted "unit tests" for specific model capabilities
   - Track user satisfaction and business outcomes
   - Use LLM-based judges for systematic evaluation
   - Compare model iterations rather than focusing on absolute metrics

4. **How frequently should embedding models be updated?**

   - Glean retrains on a monthly basis, which works well for most enterprises
   - Consider your company's pace of change and the emergence of new terminology
   - Balance freshness with the computational cost of re-indexing

5. **How can you handle the challenge of document supersession?**
   - Develop a notion of "authoritativeness" based on references, user engagement, and context
   - Recognize that recency isn't always the best indicator of relevance
   - Consider both algorithmic solutions and human judgment

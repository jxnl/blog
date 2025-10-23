---
title: The 12% RAG Performance Boost You're Missing (Ayush, LanceDB)
speaker: Ayush
cohort: 3
description: Practical approaches to enhancing retrieval quality through fine-tuning, re-ranking, and understanding trade-offs in RAG systems
tags: [fine-tuning, re-rankers, embedding models, LanceDB, RAG performance]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# The 12% RAG Performance Boost You're Missing (Ayush, LanceDB)

I hosted a session with Ayush, an ML Engineer at LanceDB, to explore how fine-tuning re-rankers and embedding models can significantly improve retrieval performance in RAG systems. We discussed practical approaches to enhancing retrieval quality, the trade-offs involved, and when these techniques make the most business sense.

<!-- more -->

[▶️ Get the 12% Performance Boost Technique](https://maven.com/p/935d62){: .md-button .md-button--primary}

## What are re-rankers and why should we use them in RAG systems?

Re-rankers fit into the RAG pipeline after retrieval and before the context is provided to the LLM. When you retrieve documents from a vector database, the embedding model gets these documents based on semantic search. Re-rankers then rearrange them so that the most relevant documents to the query rank at the top.

The power of re-rankers comes from their architecture. While embedding models (bi-encoders) calculate embeddings independently for documents and queries, cross-encoders process both together, allowing them to attend to each other throughout the pipeline. This cross-attention enables much better similarity assessment than independent embeddings.

You might wonder why we don't just use cross-encoders for retrieval directly. The answer is computational intensity - comparing a query with each document in your database isn't feasible at scale. However, once you've narrowed down to your top 5-10 results, re-ranking becomes practical and only adds milliseconds to your pipeline.

**Key Takeaway:** Re-rankers are a "low-hanging fruit" for improving RAG systems because they don't disrupt your pipeline - you don't need to re-ingest data into your embedding database. They simply plug in after retrieval and before sending context to the LLM.

## How do you train a re-ranker from scratch?

Training a re-ranker requires query-context pairs, similar to training embedding models. In Ayush's benchmark, he used Google's QA dataset with 3 million query-context pairs, using 2 million for training and 5,000 for evaluation.

The training process involves providing an anchor (the query) along with positive examples (correct answers) and negative examples (incorrect answers). The most effective approach is mining "hard negatives" - wrong answers that are very close to the query in embedding space. These challenge the model to learn subtle distinctions.

For the base architecture, Ayush experimented with two models:
MiniLM - A small 6 million parameter model that's easy to train and test
Modern BERT - A 150 million parameter model developed by AnswerAI that performs better than some billion-parameter models

On top of these base models, he attached re-ranking heads (either cross-encoder or ColBERT) and trained them to function as re-rankers. The results showed significant improvements:
Vector search improved by 12% at top-5 and 6% at top-10
Full-text search saw improvements up to 20% in some cases
Even the small MiniLM model showed improvements over baseline performance

**Key Takeaway:** Even a small re-ranker model can provide significant retrieval improvements. If you're unsure whether re-ranking will help your specific data, try training a small model in 30-60 minutes to get a signal before investing in more sophisticated approaches.

## What is the ColBERT architecture and how does it compare to cross-encoders?

ColBERT is a late interaction model that offers a middle ground between bi-encoders and cross-encoders. It independently calculates document embeddings offline (which can be stored in a vector database), but at query time, it compares token-level embeddings with the query.

This approach allows for more nuanced matching than standard bi-encoders while being more computationally efficient than cross-encoders. In Ayush's benchmarks, ColBERT architectures performed well, particularly when built on top of the Modern BERT base model.

The key advantage of ColBERT is that it still attends to token-level features but does so in two stages - the part that can be calculated offline is saved in a vector database, and at query time, it performs a maximum operation on token-level similarities to find the best match.

## Should I fine-tune an existing re-ranker or train one from scratch?

When deciding whether to train a re-ranker from scratch or fine-tune an existing one, consider these factors:

If there are no re-rankers available for your base model of choice, you'll need to train from scratch.
If your dataset has become specialized enough (drifted from the original data the model was trained on), you should fine-tune to align with your distribution.

In Ayush's experiments, using an off-the-shelf re-ranker (AnswerAI's ColBERT Small) immediately improved performance by about 10% over the baseline. Fine-tuning that model further improved results by an additional 2-3%.

Fine-tuning has practical advantages - it converges much faster since the weights aren't random and already have context. However, be careful about catastrophic forgetting - if you fine-tune for too long on low-quality data, the model's performance can degrade from its baseline.

**Key Takeaway:** Start with an existing re-ranker if available for your use case, and fine-tune it on your domain-specific data. This approach is faster and often produces better results than training from scratch.

## What are the trade-offs when implementing re-rankers?

The main trade-off with re-rankers is added latency. Ayush presented latency comparisons on an L4 GPU (similar to a T4 with larger memory):
Without re-ranking: Baseline latency
With ColBERT on Modern BERT: ~30ms additional latency
With smaller models like MiniLM: Negligible additional latency on GPU

When fetching larger result sets (overfetching documents to then re-rank them), the slowdown factor ranges from 2-3x. On CPU, the penalty is larger - up to 4-5x depending on the architecture.

Given these trade-offs, who should use re-rankers? Ayush suggests that rather than asking who should use them, we should ask who shouldn't:
If latency is absolutely critical (even 10ms matters), you might want to skip re-ranking
In all other cases where a few hundred milliseconds doesn't matter (which is most use cases), re-rankers are worth implementing

**Key Takeaway:** Re-rankers add some latency to your pipeline, but for most applications, the performance improvement outweighs this cost. Only the most latency-sensitive applications should avoid them.

## How effective is fine-tuning embedding models?

Embedding models fit into your retriever when you ingest data - they create vector representations of your documents that get stored in your database. Fine-tuning these models can also improve retrieval performance.

In Ayush's experiments with the MiniLM model:
Baseline performance at top-5: 48%
After fine-tuning: 58% (a 10% improvement)
Similar improvements at top-10

However, not all embedding models should be fine-tuned. The ideal scenario for fine-tuning is when:
Your domain-specific data has drifted from the original training distribution
You have a sufficiently large dataset (tens of thousands of examples)

If your data is just a subset of what the model was already trained on, fine-tuning might lead to overfitting and catastrophic forgetting. This was demonstrated when fine-tuning on the Stanford Question Answering Dataset (SQuAD) - only 3 of the fine-tuned models performed better than baseline because most embedding models are already trained on this common dataset.

**Key Takeaway:** Fine-tune embedding models when you have domain-specific data that differs from general web content, and when you have enough examples to properly train the model.

## Can we combine re-ranking and embedding model fine-tuning?

Yes, and this approach yields the best results. In Ayush's experiments:
Baseline: 48% (top-5) and 60% (top-10)
Best embedding-tuned model: 62% (top-5) and 69% (top-10)
Combined with best re-ranking model: 64% (top-5) and 71% (top-10)

This gives you flexibility in addressing trade-offs. If latency is a concern, you might focus more on embedding model improvements. If re-ingesting data is problematic (e.g., with billions of entries), you might emphasize re-ranking instead.

## How do you find and use hard negatives for training?

Hard negatives are incorrect answers that are very similar to the query in embedding space. To mine them:
Take your corpus and use an independent embedding model (not the one in your RAG pipeline)
Find wrong answers that are closest to your query according to the embedding model
Use these as negative examples during training

In real-world applications, there are other ways to find negatives:
If a user deletes a citation that an LLM provided, that's a strong negative signal
You can use an LLM to propose potential negatives and verify them

These approaches help create training data that challenges the model to learn subtle distinctions between relevant and irrelevant content.

## What are real-world examples where fine-tuning makes sense?

Fine-tuning is particularly valuable in specialized domains like legal or healthcare, where general training data from the internet doesn't contain all the necessary information or where much of the information is proprietary.

Another scenario is when you understand the specific types of queries users are asking. For example, if you know users frequently ask about timing-related information, but the relevant text doesn't contain explicit time words, fine-tuning can help bridge that semantic gap.

Project-specific terminology is another case - if your company uses internal codenames or jargon (like Pokemon names for projects), fine-tuning helps the model understand these connections.

**Key Takeaway:** Fine-tuning is most valuable when dealing with domain-specific knowledge, proprietary information, or company-specific terminology that general models wouldn't have encountered during training.

## Should I use data augmentation or synthetic data generation?

Ayush cautions against confusing these two approaches:
Data augmentation helps generalize an already good dataset with more examples to prevent overfitting
Synthetic data generation creates new examples from an existing dataset

The problem with synthetic data generation is that LLMs (even powerful ones like GPT-4) can hallucinate up to 70% of the time when creating synthetic query-context pairs. This means you might be adding low-quality data to your training set.

In Ayush's experiments with SQuAD, synthetic data generation consistently produced worse results than baseline. Be very careful with this approach and verify the quality of synthetic data before using it.

## What's the business benefit of all this fine-tuning work?

As I explained during the session, if you're not fine-tuning your embedding models or re-rankers, you're probably closer to Blockbuster than Netflix in your approach. At some point, these performance improvements directly correlate with business outcomes.

For example:
In product recommendations, better re-ranking might mean fewer returns or higher sales volume
For content platforms like Netflix, better embeddings ensure users find relevant content without scrolling
For search experiences, the difference between the 1st and 10th result is enormous for user experience

Whenever you're building for humans (rather than AI), ranking quality matters tremendously. Even small improvements in retrieval performance can translate to significant business value.

## What should we be thinking about next in retrieval systems?

Ayush highlighted multimodality as the next frontier. While we've made significant progress with text retrieval, humans interact with technology in multimodal ways (text, images, audio, video).

The default approach for multimodal embeddings has been CLIP, with many architectures built on top of it. However, we've come a long way from the original CLIP model, and there hasn't been enough content written about these advances.

Building better benchmarks for multimodal data retrieval and establishing stronger baselines for multimodal RAG systems represents a significant opportunity. While companies like Cohere now offer RAG over PDF screenshots, it's unclear how well these approaches extend to scenes in movies, audio clips, or podcasts.

**Key Takeaway:** Multimodal retrieval is likely the next wave of innovation in RAG systems, but we still lack established benchmarks and best practices in this area.

## How should I approach model selection for my RAG system?

When selecting models for your RAG pipeline, it's never just about which model has the best performance. Instead, you need to consider a portfolio of factors:
Maintenance costs
Inference complexity
Latency requirements
Performance improvements

You might love using a powerful model like GPT-3 as a re-ranker, but if it takes 2 minutes per API call, that's probably not practical for most applications. The best model is the one that balances these considerations for your specific use case.

This is why having a range of options - from lightweight models like MiniLM to more powerful ones like Modern BERT - gives you flexibility in designing your system. Start with simpler approaches, measure their impact, and scale up complexity only when necessary.

**Key Takeaway:** Model selection should be driven by your specific constraints and requirements, not just raw performance numbers. Consider the entire system when making these decisions.

## FAQs

## What are re-rankers and why should I use them?

Re-rankers are models that improve retrieval quality by reordering documents after they've been retrieved from a database. They fit into your pipeline after retrieval and before the context is provided to an LLM, helping to ensure the most relevant documents appear at the top. Re-rankers are particularly valuable because they don't disrupt your existing pipeline—you don't need to re-ingest your entire dataset, making them a low-hanging fruit for improving retrieval performance.

## How do re-rankers work compared to embedding models?

While embedding models (bi-encoders) calculate embeddings for documents and queries independently, re-rankers (cross-encoders) process document-query pairs together, allowing them to calculate cross-attention between both inputs. This enables re-rankers to better understand the relevance between a query and document, resulting in more accurate rankings. However, this power comes with higher computational costs, which is why re-rankers are typically used only on a small subset of already retrieved documents.

## What performance improvements can I expect from re-rankers?

Based on extensive benchmarking, re-rankers typically improve retrieval performance by 10-20% depending on the algorithm used. In the experiments presented, vector search results improved by 12% for top-5 retrieval and 6% for top-10 retrieval. Full-text search saw even more dramatic improvements, with some models showing up to 20% better performance.

## What are the trade-offs when using re-rankers?

The main trade-off is latency. Re-rankers add processing time after retrieval, typically in the range of tens of milliseconds when using a GPU. On CPUs, the latency penalty is higher, potentially 3-4x the baseline retrieval time. For most applications, this additional latency is acceptable, but if your use case is extremely latency-sensitive (where even 10ms matters), you might want to consider other approaches.

## What re-ranker architectures are available?

There are two main re-ranker architectures:
Cross-encoders: These process the query and document together, allowing for maximum interaction but requiring more computation.
ColBERT: This "late interaction" architecture calculates document embeddings offline and compares token-level embeddings with the query at retrieval time, offering a balance between performance and speed.

## When should I train a re-ranker from scratch versus fine-tuning an existing one?

Train a re-ranker from scratch when:
There are no re-rankers available for your preferred base model
Your dataset has become highly specialized or has drifted significantly from general data
Fine-tune an existing re-ranker when:
You want faster convergence during training
You have a specialized dataset but don't want to risk catastrophic forgetting
Remember that fine-tuning typically converges much faster since the weights aren't random, but training for too long on low-quality data can lead to performance degradation.

## How do I train a re-ranker?

To train a re-ranker, you need query-context pairs with positive (relevant) and negative (irrelevant) examples. The most effective approach is to mine "hard negatives"—documents that are semantically similar to the query but aren't actually relevant answers. This challenges the model to learn nuanced distinctions. Tools like sentence-transformers provide frameworks for training re-rankers with appropriate loss functions.

## Should I fine-tune my embedding models as well?

Fine-tuning embedding models can also improve retrieval performance by 8-10%, but it's more disruptive to your pipeline since it requires re-embedding your entire dataset. Consider fine-tuning your embedding model when:
Your data has a different distribution than what the model was originally trained on
You have a sufficiently large dataset (tens of thousands of examples)
Your data is domain-specific (like legal or medical content)

## Can I combine re-ranking with fine-tuned embedding models?

Yes, and this approach can yield even better results. In the experiments presented, combining the best fine-tuned embedding model with the best re-ranker improved performance from a baseline of 48% to 64% for top-5 retrieval, and from 60% to 71% for top-10 retrieval. This gives you flexibility to choose the approach that best fits your latency and performance requirements.

## What about data augmentation and synthetic data generation?

Be cautious with synthetic data generation. While it might seem like a solution for limited data, LLMs can hallucinate up to 70% of the time when generating synthetic query-context pairs. Data augmentation works best when you already have a good dataset and want to prevent overfitting, not as a solution for poor-quality data.

## How do I evaluate if re-ranking will help my specific use case?

Start with a small experiment using a lightweight model that you can train quickly (like MiniLM). If you see improvements with this simple approach, it's a strong signal that investing in more sophisticated re-ranking will yield even better results. This allows you to validate the approach before committing significant resources.

## What's the future of retrieval improvement beyond re-ranking?

## Multimodal retrieval is likely the next frontier. While much work has been done on text retrieval, there's still significant room for improvement in retrieving and ranking content across different modalities like images, audio, and video. Building better benchmarks and baselines for multimodal RAG systems represents an important area for future development.

--8<--
"snippets/enrollment-button.md"
--8<--

---

---
title: Why I Stopped Using RAG for Coding Agents (And You Should Too)
speaker: Nik Pash, Cline
cohort: 3
description: Why leading coding agent companies are abandoning embedding-based RAG in favor of direct, agentic approaches to code exploration that mirror how senior engineers actually work.
tags: [RAG, coding agents, embeddings, agentic exploration, code understanding]
date: 2025-09-11
categories: [Speaker Series, RAG, Coding Agent Series]
---

# Why I Stopped Using RAG for Coding Agents (And You Should Too)

I hosted a discussion with Nik Pash, head of AI at Cline, about his viral essay "Why I No Longer Recommend RAG for Autonomous Coding Agents." We explored why embedding-based retrieval systems are being abandoned by leading coding agent companies in favor of more direct, agentic approaches to code exploration.

<!-- more -->

## Why are coding agent companies moving away from embedding-based RAG?

Nik's journey with RAG began when he built Vault, a popular open-source project for ingesting documents and creating knowledge bases. Despite his extensive experience optimizing RAG pipelines, he's now actively against using embedding-based RAG for coding agents.

The fundamental issue is that embedding search creates unnecessary complexity for coding agents. Code is inherently logical and structured, making it more suitable for direct exploration rather than vector similarity search. As Nik explained:

> "At Cline, I became the number one advocate against using RAG, even though RAG has been my bread and butter for so long. I'm just actively anti-RAG at Cline, and I think in general for any coding agent company."

This shift isn't unique to Cline - Boris from Cloud Code shared similar experiences on the Latent Space podcast, noting that they tried RAG but found it disappointing and ultimately abandoned it in favor of agentic exploration.

**Key Takeaway:** Despite the massive investment in vector databases and embedding technologies, leading coding agent companies have discovered that direct code exploration produces better results than embedding-based retrieval for coding tasks.

## How do coding agents navigate codebases without RAG?

Instead of embedding search, modern coding agents like Cline use a "plan and act" paradigm that mimics how senior engineers actually explore codebases:

1. First, they examine the folder structure and file names
2. They read files in their entirety to understand imports and dependencies
3. They use tools like grep to search for specific patterns
4. They build an understanding through agentic discovery

This approach maintains what Cline calls "narrative integrity" - allowing the agent to follow a coherent thought process rather than jumping between disconnected code chunks retrieved by similarity search.

> "When you show a senior engineer a new codebase, what do they do? They look at the folder structure, they look at the names of the folders, they look at the files, they might read in a file and see 'okay, this file imports this other file, let's go check out what this other file has.' And then you generally build an understanding using this agentic discovery approach."

The agent first gathers all necessary information in a "plan mode," then switches to "act mode" to implement the solution. This pattern is becoming increasingly common across coding agents, with Cloud Code recently adding a similar plan and act paradigm.

**Key Takeaway:** Modern coding agents work best when they can explore code like humans do - reading entire files, following imports, and building a coherent understanding rather than relying on embedding search to surface relevant code snippets.

## What are the problems with embedding-based RAG for code?

Embedding-based RAG creates several significant challenges for coding agents:

- **Security concerns:** Indexing your entire codebase is a security risk, as embeddings can be reverse-engineered to recover the original content.
- **Maintenance overhead:** Embeddings need to be stored, updated, and maintained, creating additional complexity.
- **Distraction for the agent:** Even with perfect chunking algorithms, the agent receives disconnected code snippets from across the codebase, making it harder to build a coherent understanding.
- **Resource drain:** Optimizing RAG pipelines becomes a "black hole" that consumes endless resources for marginal improvements.

Nik described this as "schizophrenic mind map of 4-dimensional clustered embeddings floating around in its head" - a source of distraction rather than help for the coding agent.

When Pinecone responded to Nik's article with a proposal for "agentic RAG," he viewed it as "slapping 'agentic' on top of an outdated solution" that just adds more complexity to an already complex system.

**Key Takeaway:** Embedding-based RAG creates unnecessary complexity, security risks, and maintenance overhead while actually reducing the agent's ability to understand code coherently.

## When might RAG still make sense for coding agents?

Despite his strong stance against RAG for high-quality coding agents, Nik acknowledged some scenarios where it might still be appropriate:

- **Cost optimization:** If your business model requires minimizing token usage (e.g., offering a $20/month subscription), RAG can reduce costs by avoiding loading entire files into context.
- **Perfunctory performance:** When you need basic functionality rather than high-quality intelligence, RAG can provide adequate results with lower token consumption.
- **High-volume, low-stakes tasks:** For tasks like reviewing thousands of PRs where the cost of full context processing can't be justified.

Nik noted that Cursor employs this strategy to support their $20/month subscription model, while Cline takes a different approach:

> "From the very beginning at Cline, we were just 'bring your own API keys' and use Cline however you like. We go full context-heavy and don't take any shortcuts around context. And we find that it works just so much better for agent coding."

**Key Takeaway:** RAG may still be appropriate when optimizing for cost rather than quality, but for serious engineering teams working on production code, the full context approach produces significantly better results.

## How do coding agents maintain context in long-running tasks?

For managing context in long-running tasks, Cline offers several approaches:

- **Compacting with slash commands:** Users can use "/sum" to compact the conversation.
- **Task handoff with "/new task":** This creates a summary of everything done so far, as if handing off to a new engineer, and starts a fresh context window.
- **Algorithmic context management:** Cline previously used an algorithmic approach to remove duplicate file reads while maintaining narrative integrity.

Interestingly, Nik noted that simple summarization is proving more effective than complex context management strategies:

> "What we're finding now is that actually summarization just works better. In our internal testing, you can have these long-running tasks with resets of the context window many times over with just a very detailed summary."

This aligns with the "bitter lesson" in AI - that simpler approaches often outperform complex engineered solutions as models improve. Cline is also experimenting with to-do lists as a way to help agents track progress across context resets.

**Key Takeaway:** Simple summarization is proving more effective than complex context management strategies for maintaining agent performance across context window limitations.

## What's the "bitter lesson" for AI application developers?

The ["bitter lesson" in AI](http://www.incompleteideas.net/IncIdeas/BitterLesson.html), as Nik describes it, is that the application layer is shrinking over time. With traditional ML, developers needed extensive code to make models useful, but with modern LLMs, the amount of code required is decreasing:

> "The bitter lesson to me, what it really means, is that this application layer is just shrinking over time. Every day it's just growing smaller and smaller."

Instead of trying to maintain complex systems like RAG pipelines, Nik recommends embracing this trend:

> "Just throw it all out. Let the model do its job. Stop trying to get in the way of the model. It's almost like cleaning a mirror and letting more light shine through."

This pattern extends beyond RAG to other areas:

- **Fast API:** Similar principles apply to API design
- **Static analysis tools:** Companies like Codegen spent years building knowledge graphs for code, only to abandon them for simpler approaches
- **Multi-agents:** Nik suspects that complex multi-agent systems may follow the same pattern

**Key Takeaway:** As AI models improve, complex application layers often become unnecessary overhead. The most effective approach is often to simplify and let the model's capabilities shine through rather than building elaborate systems around them. This aligns with the [Context Engineering principles](../context-engineering-index.md) of designing simple, effective tool responses rather than complex retrieval systems.

## What about multi-agent approaches for coding tasks?

When asked about questions people aren't asking in the coding agent world, Nik raised an interesting point about multi-agent systems:

> "What's better - a team of geniuses working together, or a bunch of solo geniuses working separately in isolation?"

He believes solo geniuses often produce breakthroughs, and this applies to coding agents as well. Despite the appeal of multi-agent systems like Auto-GPT and Crew AI, which promised to overcome context window limitations by having multiple agents collaborate, Nik remains skeptical:

> "It just never worked. It was just a fast way to burn a whole bunch of tokens and get nowhere."

He sees parallels between the RAG narrative and the current excitement around multi-agents, suggesting the industry may be repeating the same pattern of unnecessary complexity:

> "I'm kind of on the side of keeping it single-threaded, keeping it one agent. For things like read-only it might make sense if you're just gathering things in context, but even there... Anthropic uses multi-agents in their research mode, OpenAI doesn't, and OpenAI just works so much better for me."

**Key Takeaway:** Despite the appeal of multi-agent systems, single-agent approaches may prove more effective for coding tasks, following the same pattern we've seen with RAG - simpler approaches often win as model capabilities improve.

## How do tools and interfaces affect coding agent performance?

Cline and other coding agents provide both specialized tools (read file, search directory) and general-purpose tools (terminal access). Nik explained that this hybrid approach serves several purposes:

- **UX considerations:** Specialized tools allow for custom interfaces that improve the user experience
- **Permission management:** Specialized tools enable fine-grained access controls
- **Error reduction:** Specialized tools reduce the surface area for potential errors

However, Nik acknowledged that this might be transitional:

> "We have considered internally, what if we just only use the terminal tool and the agent would figure things out from there? I think eventually we might move in that direction, but for the time being it is helpful to have this little sandbox for the agent."

For model selection, Nik noted that Cline users often employ different models for different phases:

> "A common pattern a lot of people use is they use a very large context window model like Gemini Pro 2.5 for the planning phase, and then for the act phase, once they've come up with a plan, read in all of the files into context, and come up with a very solid plan, then for the execution phase they switch to Sonnet."

**Key Takeaway:** While specialized tools currently provide UX benefits and safety guardrails, the industry may eventually move toward simpler interfaces as models become more capable. Different models excel at different phases of the coding process, with large context models for planning and specialized coding models for execution.

## How do coding agents handle memory and knowledge management?

For persistent knowledge, Cline offers several approaches:

- **Client Rules:** Files containing knowledge or instructions that Cline should know for every task, similar to a memory system
- **Workflows:** Markdown files that define sequences of repetitive tasks
- **Knowledge Engine:** Coming in their enterprise product

Nik expressed caution about automatic memory updates like those in ChatGPT:

> "You really gotta be careful with this because oftentimes using ChatGPT, it's just like 'memory updated' - it's like 'Oh, memorize something that I didn't want it remembering. Stop doing this!'"

He suggested that embedding-based approaches might actually be appropriate for managing collections of memory snippets, showing that while he's against RAG for code exploration, he sees potential value in similar technologies for different use cases.

**Key Takeaway:** Memory management for coding agents requires careful design to balance automation with user control. While embedding-based approaches might be appropriate for managing collections of memories, they're still problematic for code exploration.

## What's next for Cline and coding agents?

Cline is expanding their offerings with several new developments:

- **Enterprise product** launching the same week as this talk
- **JetBrains integration** coming soon
- **CLI version** of Cline for terminal users

Nik mentioned that many large enterprises are already using Cline through their open-source offering and are eager for an enterprise version to manage security, costs, and permissions:

> "We started getting flooded with all these enterprises, booking meetings with Fortune 5 companies, not even 500, but massive companies with massive engineering teams and massive codebases coming to us saying 'Hey, we already have hundreds of engineers using Cline in our organization because you guys are open source and we passed the security audits.'"

These companies reported that Cline works well in their massive codebases using the basic tools Cline already provides, validating the agentic approach even at enterprise scale.

**Key Takeaway:** The agentic approach to code exploration is proving effective even in massive enterprise codebases, and companies are eager to adopt these tools with proper enterprise controls for security and cost management.

---

## FAQs

## What is RAG and why was it initially popular?

RAG (Retrieval-Augmented Generation) was initially promoted as a solution to give AI models "long-term memory" when context windows were very limited. Companies like Pinecone marketed embedding-based search as a way to ground AI responses in real documents, reduce hallucinations, and simulate infinite context windows. This approach gained significant investment from major venture capital firms and became a standard recommendation for many AI applications.

## Why is RAG no longer recommended for coding agents?

For coding agents specifically, RAG (particularly embedding-based search) has proven unnecessary and potentially counterproductive. Modern coding agents perform better when allowed to explore code bases naturally—reading files, using grep commands, and navigating directory structures—similar to how human engineers work. This approach maintains "narrative integrity" where the agent follows a logical thought process rather than jumping between disconnected code snippets surfaced by embedding search.

## What alternatives work better than RAG for coding agents?

The most effective approach is giving coding agents access to basic tools like file reading, directory navigation, and terminal commands (grep, search). This allows agents to explore code bases organically, building understanding through a logical progression. Many leading coding agents like Cline and Cloud Code have adopted a "plan and act" paradigm where the agent first gathers information and creates a plan, then executes it—all without relying on embedding search.

## Doesn't RAG help with large code bases?

Surprisingly, even with very large code bases, the agentic exploration approach works better than embedding search. Major enterprises with massive code bases have found that tools like Cline work effectively without RAG. The agent simply needs access to the file structure, basic search capabilities, and the ability to read files in context to navigate even complex code repositories.

## What about hallucinations? Doesn't RAG help prevent those?

For coding agents, hallucinations are rarely an issue when using the agentic approach. By reading files in full context and setting temperature to 0, modern models can maintain accuracy without embedding search. The hallucination concern is largely outdated with today's flagship models and their expanded context windows.

## Are there any situations where RAG is still useful?

RAG can still be valuable in certain scenarios:

- When trying to reduce costs (embedding search can use fewer tokens than reading entire files)
- For applications with massive unstructured data lakes
- For human-readable documents like legal texts (though even here, agentic exploration is increasingly effective)
- When building applications with tight budget constraints that need to optimize token usage

## What is the "bitter lesson" regarding RAG and coding agents?

The "bitter lesson" refers to the realization that as AI models improve, many complex engineering solutions become unnecessary. For coding agents, this means that elaborate systems like embedding search, knowledge graphs, and complex indexing are being outperformed by simply letting the model do what it does best with minimal interference. The application layer is shrinking, and developers should focus on removing barriers rather than adding complexity.

## How do coding agents maintain context in long-running tasks?

Rather than using RAG for memory, effective coding agents use techniques like:

- Summarization of previous work
- Task handoff with detailed context summaries
- To-do lists that track completed and remaining items
- Structured workflows that maintain logical progression

These approaches have proven more effective than embedding-based memory systems for maintaining context in extended coding sessions.

## What about multi-agent systems? Are they better than single agents?

The evidence suggests that single, powerful agents often outperform multi-agent systems for coding tasks. Similar to the RAG situation, there's a tendency to add complexity (multiple specialized agents) when a single capable agent with the right tools can perform better. While the jury is still out, early indications suggest that maintaining "narrative integrity" with a single agent leads to more coherent and effective results.

## How should tools be provided to coding agents?

There's a balance between providing specialized tools (read file, search directory) versus general-purpose tools (terminal access). Specialized tools offer better UX, permissions control, and error prevention, while general-purpose tools provide flexibility. Most successful coding agents offer both, with specialized tools for common operations and terminal access for everything else. As models improve, the need for specialized tools may diminish.

---

--8<--
"snippets/enrollment-button.md"
--8<--

---

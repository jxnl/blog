---
title: "Rethinking RAG Architecture for the Age of Agents"
author:
  name: Beyang Liu
  company: Sourcegraph
  title: CTO
cohort: 3
description: "CTO of Sourcegraph explores how the evolution of AI models has fundamentally changed agent architecture, requiring a complete rethinking of context management, tool design, and model selection"
tags: [agents, RAG architecture, coding agents, context management, tool design, model selection]
date: 2025-09-11
categories: [Speaker Series, RAG, Coding Agent Series]
---

# Rethinking RAG Architecture for the Age of Agents - Beyang Liu (Sourcegraph)

I hosted a session with Beyang Liu, CTO of Sourcegraph, to explore how the evolution of AI models has fundamentally changed how we should approach building agent systems. This discussion revealed why many best practices from the chat LLM era are becoming obsolete, and how the architecture of effective agents requires rethinking context management, tool design, and model selection from first principles.

<!-- more -->

[▶️ See Sourcegraph's Agent Architecture Revolution](https://maven.com/p/be969c){: .md-button .md-button--primary}

## Why are we rethinking agent architecture from first principles?

The evolution of AI has progressed through three distinct eras, each requiring different application architectures. We started with the autocomplete era (GPT-3), moved to the RAG chat era (ChatGPT, GPT-3.5/4), and now we're in the agentic era (GPT-3.7, Claude Sonnet, Claude 4).

The fundamental shift between the RAG chat era and the agentic era is the inversion of context fetching. In the RAG chat era, a monolithic context engine would fetch relevant snippets before sending them to the LLM. With agents, the model itself decides which tools to invoke to fetch appropriate context.

This seemingly minor change has profound implications for user experience and system architecture. As Beyang explained, "It seems like a minor change - in the picture just moving the green box down to the bottom. But it actually has some pretty big implications for what the user experience is and what the architecture is."

**_Key Takeaway:_** The shift from RAG chat to agentic architecture isn't just a technical implementation detail - it represents a fundamental inversion of control that changes how we should design AI systems from the ground up.

How does this architectural shift change the user experience?
The dominant interaction paradigm has completely transformed. In the chat world, humans were deeply involved in the inner loop of model interaction - checking output after every LLM turn, refining it, and manually applying changes. This created a lot of "ping pong" with the model just to make one atomic change.

In the agentic world, users can articulate what they want upfront and have the agent do extensive work on its own - reading files, editing files, searching for related information, executing commands, and checking outputs. This dramatically reduces the need for human babysitting and allows for much faster completion of complex tasks.

Beyang's team at Sourcegraph made several controversial design decisions for their Amp coding agent that reflect this paradigm shift:

Minimal UI with focus on agent design and feedback loops rather than complex interfaces for selecting context

Bias toward action - the agent often edits files without asking permission first

No model selector - intentional coupling between models and tools

Unix philosophy of composability rather than vertically integrated thick clients

Usage-based pricing to avoid perverse incentives that would lead to "dumbing down" agent capabilities

"We're really focusing on the design of the agent and feedback loops rather than a complex graphical user interface for selecting context," Beyang noted. This approach has received positive feedback from users who find it more effective than both traditional AI IDEs and other coding agents.

Key Takeaway: The agentic paradigm allows for much more autonomous work with less human intervention, but requires rethinking interface design to focus on agent capabilities rather than human context selection.

What does RAG look like in the era of agents?
The traditional RAG engine from the chat era was typically a monolithic system with keyword indexes, embedding models, domain-specific chunkers, and re-rankers. In contrast, many popular agents today rely on much simpler retrieval tools like grep.

This doesn't mean retrieval is unimportant - rather, the approach to retrieval has fundamentally changed. Beyang suggests thinking about agent design in three main categories:

Tool selection - beyond just retrieval tools, consider feedback tools and planning tools

Context window management - how to keep the context window focused and avoid tool overload

Model choices - tight coupling between models and tools requires intentional model selection

"RAG is not strictly about retrieval anymore," Beyang explained. "It's really about molding the underlying model to be able to do what you need it to do in a particular application setting or for a specific set of workflows."

For Amp, the tool panel includes multiple simple tools rather than one monolithic RAG engine. These include grep and glob for basic searches, a search sub-agent that performs multiple queries and refinements, web documentation tools, and specialized services.

Key Takeaway: Instead of building complex monolithic RAG engines, focus on providing agents with a thoughtfully designed portfolio of simple tools that can be composed to solve complex problems. The [Context Engineering series](../context-engineering-index.md) explores exactly how to design these tool portfolios for maximum agent effectiveness.

How do sub-agents extend agent capabilities?
One of the most important innovations in agent architecture is the use of sub-agents to extend the effective context window. While techniques like compaction (summarizing previous interactions) can help, they're lossy and often lose important details.

Sub-agents provide a more intentional approach to managing context. Amp implements several types of sub-agents:

Code-based search sub-agent - handles exploration and query refinement to find relevant code snippets

Generic sub-agent - allows the main agent to invoke itself to perform tasks in parallel

"Oracle" sub-agent - uses a different model (Claude 3) that's better at nuanced thinking about complex code

The search sub-agent is particularly valuable because it can use a significant portion of its context window for exploration without consuming the main agent's context. "All the exploration it does when refining different queries and trying different things to find what the user is looking for - that eats up context window. But because the sub-agent, once it's found the right snippets and returned them to the main agent, you can essentially throw away the context that was used for the sub-agent," Beyang explained.

This approach allows for much more complex workflows than would be possible with a single agent constrained by context window limitations.

Key Takeaway: Sub-agents are a powerful technique for extending agent capabilities beyond context window limitations, allowing specialized models to handle specific tasks while preserving the main agent's context for core reasoning.

Why is model selection no longer agnostic?
In the chat LLM era, the coupling between retrieval mechanisms and models was loose, making it easy to swap models. The flow was simple: user message → retrieve context → put in LLM → generate response.

With agents, the flow is much more complex. The agent LLM uses various tools, each tool description becomes part of the effective prompt, and some tools are agents themselves with their own models. This creates tight coupling between models and tools.

"If we were to offer up to end users a way to easily swap out any of these LLMs for another model that's not been tuned to those tool descriptions, or has other tool use capabilities or characteristics, it's just a recipe for a bad user experience," Beyang argued.

Instead of model agnosticism, Amp takes an intentional approach to model selection, using different models for different purposes. The "Oracle" sub-agent, for example, uses Claude 3 specifically because it's better at nuanced thinking about complex code.

Key Takeaway: The era of model-agnostic architectures is ending. Effective agent design requires intentional selection of models based on their specific capabilities and how they interact with your tools.

How do agents change the ceiling of what's possible?
Chat-based applications were constrained by the tree retrieval engine model - essentially "search plus plus" that could only go so far. Agents have a much higher ceiling but require users to get better at prompting to unlock their full potential.

Amp includes a built-in collaboration mechanism where users can see threads their teammates are having with the agent. "I've learned so much just from watching how other people on the team are doing prompts," Beyang shared. "There's some people who write paragraph, essay-long prompts, and are able to get enough context in there to get the agent to do much, much more."

This highlights an important tension in agent design: making tools accessible to new users versus preserving power and composability for advanced users. Beyang argues that we should be careful not to artificially limit agent capabilities just to make them seem more magical for beginners.

Key Takeaway: Agents have a much higher ceiling than chat-based applications, but unlocking their full potential requires thoughtful prompting and a willingness to learn from how others use them effectively.

How well do these principles generalize beyond coding?
While Amp is focused on coding, many of the architectural principles apply to other domains. Beyang has observed users applying Amp to various non-coding tasks like research and troubleshooting.

The workflows that generalize best are those that can be done using tools similar to what you have in a development environment - basic search, execution, and document retrieval. "There's a whole bunch of knowledge work that falls under the umbrella of like, as long as you have some tools that look like that, you as a human can get it done, and therefore the agent could probably do a pretty good job as well," Beyang explained.

However, some specialized domains may require different approaches. The key insight is that workflows that can be captured by the reinforcement learning environment of the models will become increasingly automated, while the remaining workflows will expand to take up more of people's time "because that's where the interesting alpha remains."

Key Takeaway: The principles of agent architecture generalize well to many knowledge work domains, particularly those involving search, retrieval, and execution of commands, but specialized domains may require domain-specific tools and approaches.

What should we question when building agents?
Beyang suggests asking three key questions when building agents:

What are you cargo culting from the Chat LLM era? Have you actually thought about whether that's the best construction for building an agent?

Are you treating context not just as a retrieval exercise, but as a broader set of things that provide relevant information for the context window?

Are you thinking about how to unlock the ceiling of what agents can do?

"A lot of the best practices that people developed during the chat LLM era are no longer relevant at best, and in the worst case, actually run in direct tension with what the emerging best practices for building agents are," Beyang warned.

The future of agent development likely lies in composable, Unix-like tools rather than vertically integrated solutions. While vertically integrated approaches might create snazzier demos in the short term, they tend to be brittle when faced with the diversity of real-world codebases and workflows.

Key Takeaway: Question your assumptions from the chat LLM era, focus on composability over vertical integration, and design intentionally to preserve the power and flexibility that makes agents truly transformative.

How should we evaluate agent performance?
Traditional RAG evaluation metrics like recall percentages become less relevant in the agentic paradigm. If an agent gets 62% recall instead of 72%, it might just take a few more searches to achieve the same result.

Beyang suggests that evaluation should be motivated by actual pain points experienced as a user rather than abstract metrics. "All new things, in my view, are motivated by vibes. That thing was painful, I want it to be better."

Evaluations should function more like unit tests or smoke tests - ensuring that workflows that currently work well continue to work well even as you make changes to improve other aspects of the system.

"You should never use evals as a way to guide your product development because evals are always kind of downstream of the vibes," Beyang explained. "Evals are in some sense an attempt to quantify the vibes."

Key Takeaway: Focus evaluation on real user pain points rather than abstract metrics, and use evals as guardrails to prevent regression rather than as primary guides for product development.

Final thoughts on building effective agents
The shift from chat LLMs to agents represents a fundamental change in how we should approach AI system design. By inverting the context fetching process, agents can achieve much more autonomous and powerful workflows, but this requires rethinking many assumptions from the previous era.

Effective agent design involves thoughtful tool selection, context window management, intentional model choices, and the strategic use of sub-agents. Rather than building monolithic RAG engines, focus on providing a portfolio of simple, composable tools that agents can use to solve complex problems.

As Beyang summarized, "The potential here is far greater for agents to be able to automate and accelerate much more of knowledge work, but it does require thinking about how you design intentionally for that rather than just how do I provide the smoothest ladder for newbie users into this product experience."

By questioning our assumptions and designing from first principles, we can build agents that truly transform how we work with AI systems across domains.

FAQs:

What is the key difference between chat-based LLMs and coding agents?

The fundamental difference lies in how context is managed. In chat-based systems, a monolithic context engine fetches relevant snippets before sending them to the language model. With agents, this process is inverted—the model decides which tools to invoke to fetch appropriate context based on the user's request. This seemingly minor change has significant implications for user experience and system architecture.

How have AI systems evolved over time?

AI systems have progressed through three distinct phases. First was the autocomplete era with GPT-3, where applications were limited to text completion. Next came the RAG chat era with ChatGPT and GPT-3.5/4, enabling instruction following and reasoning about factual information. Now we're in the agent era with models like GPT-3.7, Sonnet, and Claude 4, which can perform complex sequences of actions autonomously.

What are the key design principles behind modern coding agents like Amp?

Modern coding agents like Amp focus on simplicity and effectiveness rather than complex interfaces. They're designed to take action without excessive user confirmation, don't include model selectors, follow a Unix philosophy of composability, and typically use usage-based pricing to align incentives. These design choices enable agents to accomplish more complex tasks with less human intervention.

How does the user interaction paradigm differ with agents?

In the chat-based paradigm, humans were deeply involved in the interaction loop, checking and refining output after every model turn. With agents, users can articulate what they want upfront and let the agent handle multiple steps autonomously—reading files, editing code, searching for related information, and validating changes—without constant supervision.

What tools do effective coding agents use?

Rather than relying on complex monolithic retrieval engines, effective coding agents use a portfolio of simpler tools including:

Context retrieval tools (like grep, glob, and search)

Feedback tools (bash commands for testing, editor diagnostics, screenshots)

Planning tools (to structure longer sequences of actions)

Sub-agents (specialized agents for specific tasks)

What are sub-agents and why are they important?

Sub-agents are specialized agents that can be invoked by the main agent to perform specific tasks. They're crucial for extending the effective context window of the main agent. For example, a search sub-agent can explore and refine queries to find relevant code snippets without consuming the main agent's context window. Other examples include parallel task sub-agents and specialized "oracle" sub-agents that excel at deep thinking about complex problems.

Why is model selection less important in the agent era?

Unlike chat-based systems where models could be easily swapped, agents have tighter coupling between the model and its tools. Different models have varying capabilities for tool use, and tool descriptions are often tuned for specific models. Swapping models can lead to poor user experiences as the new model may not effectively utilize the tools provided.

How should developers approach context window management in agents?

As agents perform longer sequences of actions, context window management becomes critical. Strategies include:

Keeping the context window focused on relevant information

Avoiding tool overload by carefully selecting which tools to expose

Using context compaction to summarize previous interactions

Leveraging sub-agents to perform tasks that would otherwise consume the main agent's context

What's the future of RAG (Retrieval-Augmented Generation) in the agent era?

Traditional RAG is evolving beyond simple retrieval. In the agent era, it encompasses three main considerations:

A broader set of tools beyond just retrieval (including feedback and planning tools)

Sophisticated context window management

Strategic use of sub-agents to extend capabilities

How can developers start building their own agents?

Building a basic agent is simpler than many people think—it's essentially "invoking the model in a for loop," with sub-agents being like nested loops. Developers can start with a simple CLI-based agent with basic tools, then iterate based on user feedback. The blog post "How to Build an Agent" provides a starting point, and interestingly, you can even have an existing agent read the blog post and generate an agent for you.

What lessons from coding agents might apply to other domains?

Many principles from coding agents can generalize to other knowledge work domains, particularly workflows that involve search, document retrieval, and structured execution. The key is identifying which tools and feedback mechanisms are most relevant to your specific domain. Coding agents provide a glimpse into how AI systems will evolve across all regulated domains.

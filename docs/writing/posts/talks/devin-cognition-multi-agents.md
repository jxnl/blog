---
title: Why Cognition does not use multi-agent systems
speaker: Walden Yan
cohort: 3
description: A deep dive into why multi-agent systems might not be the optimal approach for coding contexts, exploring context engineering, challenges of context passing between agents, and how single agents with proper context management can outperform multi-agent setups.
tags: [multi-agent systems, context engineering, coding, agent development]
date: 2025-09-11
categories: [Speaker Series, RAG, Coding Agent Series]
---

# Why Cognition does not use multi-agent systems

I hosted a session with Walden Yan, co-founder and CPO of Cognition, to explore why multi-agent systems might not be the optimal approach for coding contexts. We discussed the theory of context engineering, the challenges of context passing between agents, and how single agents with proper context management can often outperform multi-agent setups.

<!-- more -->

[▶️ Learn Why Devin Chose Single Agents](https://maven.com/p/446ea1){: .md-button .md-button--primary}

## Why are multi-agent systems problematic for coding tasks?

The fundamental issue with multi-agent systems is context management. When you split a task between multiple agents, you're essentially playing a game of telephone where critical information can get lost in transmission.

Consider a simple example: building a Flappy Bird clone. If you assign one agent to build the background with green pipes and hitboxes, and another agent to create the bird asset, they might develop completely incompatible components. The first agent might create something resembling
Mario's environment, while the second creates a bird from an entirely different game.

This miscommunication happens because each agent only understands what it was told by the main agent. While this example might seem extreme, these issues compound dramatically when dealing with complex tasks at scale:

> "You're gonna find lots of places where miscommunications like this are just gonna get introduced in your system, especially as you as the when the user is talking with the system back and forth many times when these sub agents are getting more and more nuanced tasks, and you forget to pass some details through."

The context isn't just the user's message but includes everything the agent has done - code files examined, questions asked, and answers received. These full agent traces should ideally be passed to all agents in the system.

**Key Takeaway:** Multi-agent systems often break down due to context loss between agents. What seems like a minor miscommunication in simple examples becomes a significant problem at scale with complex tasks. This connects to the broader [Context Engineering principles](../context-engineering-index.md) around managing information flow and avoiding context pollution in AI systems.

## How can we improve context passing between agents?

To minimize the "telephone game" problem, we need to ensure sub-agents have at least the same context as the main agent. This means:

- Sub-agents should see everything the main agent saw
- Sub-agents should have access to the full history of actions taken by the main agent
- The final agent should see everything from all previous agents

Even with this improved context passing, problems still arise when sub-agents work in parallel. They can't communicate with each other, leading to conflicts in style, APIs used, or duplicated code. When sub-agent one commits to certain decisions and sub-agent two commits to different decisions, these conflicts create integration problems.

> "With any agentic system, lots of actions can basically carry these implicit decisions being made... anytime these decisions are made, you almost always have to actually make sure this decision is shared with everyone else, or else you might just get these conflicting decisions."

A more reliable approach is a linear system where agents work sequentially. Sub-agent one completes its task, then sub-agent two works with full knowledge of what sub-agent one did, avoiding conflicts in decisions.

**Key Takeaway:** Passing full context between agents helps but doesn't solve all problems. When agents work in parallel, they make conflicting implicit decisions that create integration challenges.

## What are the limitations of simple linear agent systems?

While linear agent systems solve many coordination problems, they quickly run into context window limitations. As the task progresses, the context grows larger until it exceeds what the model can effectively process.

> "With the simple agent, you know, if you're just collecting everything that this agent's been doing, and especially for these longer tasks, you'll quickly run to context overflow issues, especially as you go down the line towards the end of your task."

One solution is implementing a context compressor that intelligently selects what information to pass from one agent to the next. However, this adds complexity and requires careful engineering to ensure important details aren't lost.

At Cognition, they trained a specialized model to identify and preserve critical information from earlier conversations. This approach requires significant investment but can be worthwhile for complex engineering tasks.

> "You have to think very carefully about. Are you willing to put in the work to kind of squeeze out this extra juice from your system. In our case it makes sense, because our entire goal is to make sure that we can take on harder and harder engineering tasks."

**Key Takeaway:** Simple linear agent systems eventually hit context window limits. Context compression can help but adds complexity and requires careful engineering to avoid losing critical information.

## What real-world approaches exist for managing agent context?

Several practical approaches have emerged for managing context in agent systems:

### Read-only sub-agents

Both Claude Code and OpenCode use sub-agents that only read and don't make decisions. These agents perform tasks like listing project files, examining packages, or looking for imports, then report back to the main agent.

> "The designers of these systems of these agent builders are very careful to constrain their sub agents to only doing read-only tasks. I think if you read the cloud Sys prompt. If you read open code Sysprompt, you'll probably find stuff that's like you should only use subagents for things that involve reading code."

### Edit-apply models

Systems like Cursor and Windsurf use a two-stage approach where a smart coding model generates human-readable instructions for code changes, and a simpler "edit-apply" model implements those changes. This approach can be fragile if the instructions aren't perfectly clear.

> "When you see complaints online about, hey? Sometimes in these code editors the edit will be like wrong and or mess something up. It is often because of this that the smart coding agent left out some important detail, or wasn't specific enough about something."

Even read-only sub-agents can create problems when they return conflicting information, leaving the main agent to resolve contradictions without full context.

**Key Takeaway:** Read-only sub-agents and specialized edit-apply models can help manage context, but each approach has limitations and potential failure points.

## Why should systems feel like a single agent to users?

Even if your system has complex internal components, it should present itself to users as a single, coherent entity. This creates a more intuitive user experience and avoids confusion.

> "If you're abiding by like kind of principles of good context, engineering your system as a whole, even if it has like subparts and tasks. It kind of should feel to the user like a single agent, because the user has to feel like they're they're talking with one continuous decision maker, one continuous like consciousness."

True multi-agent collaboration requires sophisticated capabilities that current models don't yet possess. Effective collaboration between humans requires mentally modeling what others know and don't know - a complex skill that LLMs haven't mastered.

> "It actually requires being very intelligent to be good at collaborating with other people like when when I'm working with another engineer on my team, if I am mentally modeling at the same time what they know, what they don't understand and what I have to tell them."

The path forward likely involves making single agents smarter and more collaborative, which will eventually enable effective multi-agent systems.

**Key Takeaway:** Systems should present as a single coherent entity to users. True multi-agent collaboration requires sophisticated capabilities that will emerge naturally as single agents become more intelligent.

## What skills are current agents lacking for effective collaboration?

Current agents struggle with several key collaboration skills:

### Escalation awareness

Recognizing when they've reached the limits of their decision-making authority and need human input.

> "When can a system recognize when it reaches its own limits of the decisions it is allowed to make... How do you know, like a you should? Either way, you should notify the human that like, Hey, there's something weird that's happening here."

### Confidence assessment

Accurately evaluating and communicating their confidence in proposed solutions.

> "In Devin. One thing we do is when you collaborating with your agent, when you collaborate when you're collaborating with Devin, Devin will give you the how confident it is in its plan. And that way you, as a human, can say, like, okay, Devin is like 99% confident that this is going to work, you can roughly be hands off."

### Concise communication

Providing key information without overwhelming users with unnecessary details.

> "People hate how like, you know, Llms will just send you like a wall of text, and Markdown, a smart engineer will like manage to hone in on the key problems and the key things you have to think about with like minimal words, one sentence, 2 sentence of words."

These skills are particularly important for human-agent collaboration, where the human should remain the ultimate decision-maker while the agent handles appropriate tasks autonomously.

**Key Takeaway:** Effective collaboration requires agents to know when to escalate decisions, accurately assess their confidence, and communicate concisely - skills that current systems are still developing.

## How important is planning in agent systems?

Planning serves as a crucial form of context management in agent systems. By committing to a structure upfront, agents can avoid the constant recompression of information that happens in more dynamic approaches.

> "Planning is something that we do. And the context of planning emergency came up for us is actually a form of context management. Because, again, it's about avoiding this game of telephone where you you have to constantly recompress and the information that you're you're sending to your agent."

At Cognition, Devin spends significant time reading code and generating a plan at the start of any task. This planning phase is one area where sub-agent-like components might be useful, though they're integrated in a way that still feels like a single system to the user.

While detailed planning (like creating extensive plan.md files) can improve results, Walden believes these capabilities will eventually be built into the systems themselves:

> "You can be shown the plan. You can click this button to like view the full plan that the agent's working on. But the agent will work on this internally for its own sake. You know whether or not like you, tell it to or not."

**Key Takeaway:** Planning is a powerful context management technique that helps agents maintain coherence throughout complex tasks. While users can create detailed plans, these capabilities are increasingly being built into agent systems.

## What frameworks and patterns show promise for agent development?

We're still in the early stages of agent development - comparable to the HTML/CSS/JavaScript era of web development before frameworks like React emerged. However, some promising patterns are emerging:

### Cache-aware frameworks

Systems that optimize for caching, even before API-level caching was available.

> "Our system has been built with caching kind of like being a very core condition. So even as you scale out and do these sub agents and things like that, having a system that still manages to like optimally cache work from before, I think is going to be important thing."

### Integrated evaluation systems

Frameworks that tightly couple agent code with evaluation systems.

> "We kind of like segment functionalities of our system into modules and these modules are tagged in such a way that not only are things that go through those modules, things that like we can track and feed into eval systems. When we change code inside these modules, we can then also back, run them against evals from before."

### Universal tools over specialized integrations

Providing agents with powerful general-purpose tools like shell access rather than numerous specialized integrations.

> "I personally like to just like, give our agent the most universal tools possible, and make sure there's very easy to use. So the shell command, like the the bash tool, for example, is so fucking powerful, it like literally, it means like anything you can do on a computer like your agent can do now."

CLI tools can sometimes be more powerful than formal integrations because they can interact with the agent in sophisticated ways, almost becoming part of the agent system itself.

**Key Takeaway:** While we're still early in agent framework development, patterns around caching, evaluation integration, and universal tools are showing promise for building robust systems.

## How is code review evolving with AI agents?

As AI generates more code, the review process is evolving to minimize the work required to verify changes. Walden highlighted how they're leveraging existing tools like Vercel's preview links:

> "I tag Devin on slack. I go away. I do my thing. And 1st of all, I always tell Devin to send me a screenshot of the visual changes it makes, so I don't have to even leave slack. I will immediately see a screenshot of like, okay, is this even something reasonable that I want to review?"

This approach allows for quick visual verification before diving into code details. Similar infrastructure for backend systems would be valuable but hasn't been heavily invested in yet.

The future of code review likely involves more automated verification and visualization tools that help humans quickly understand and validate AI-generated changes.

**Key Takeaway:** Code review is evolving to minimize human effort through screenshots, preview environments, and other tools that provide quick verification of AI-generated changes.

## What exciting developments are coming for developer tools?

Walden is particularly excited about creating better synergies between local development environments and remote agents. One area with significant potential is improving code reading and understanding:

> "Actually reading code reading code, understanding code planning how you want to make changes. Because when you're an individual developer, you're actually oftentimes you're working a massive code based searching code that isn't yours. You're trying to understand it."

While current AI tools can help with implementing specific tasks, there's a cap to what they can handle without proper planning. AI has a unique advantage in reading and understanding code much faster than humans, which could transform how developers approach large codebases.

> "The AI, even though it can like only edit code serially, it could read codes like so much faster than any of us can. And so I'm very excited about things we're going to be doing and just making that process and experience be a lot easier."

**Key Takeaway:** The next frontier for developer tools involves better code reading, understanding, and planning capabilities that leverage AI's ability to process large codebases quickly.

## Final thoughts on the future of agent development

Walden believes we're just beginning to develop the concepts and principles that will become fundamental to agent development. In the future, these ideas will likely be taught in entry-level college courses.

The field is evolving rapidly, with practitioners discovering new patterns and approaches through experimentation. While multi-agent systems have captured popular imagination, the immediate future likely belongs to increasingly sophisticated single agents that can handle complex tasks with proper context management.

As these systems mature, the principles of context engineering will become more formalized, eventually leading to frameworks that make building robust agent systems more accessible to developers without requiring deep expertise in prompt engineering or context management.

**Key Takeaway:** We're in the early stages of developing fundamental concepts for agent systems. While multi-agent approaches capture imagination, near-term progress will come from improving single agents with better context management.

---

## FAQs

### What are the main issues with multi-agent systems in coding?

Multi-agent systems often suffer from context loss and conflicting decisions. When multiple agents work in parallel, they may not share the same understanding of the original task or see each other's work, leading to inconsistencies. This creates a "telephone game" effect where important details get lost as information passes from one agent to another, resulting in incompatible outputs that don't work well together.

### What is context engineering and why is it important?

Context engineering is the practice of carefully managing what information is available to AI agents at each step of their work. Unlike prompt engineering (which focuses on how you phrase instructions), context engineering focuses on ensuring agents have all the necessary background information and history they need to make good decisions. As models become more capable, the limiting factor is increasingly how much relevant context they have access to rather than how you phrase your prompts.

### What are the two core design principles for building reliable agent systems?

The two core principles are: 1) Always share full context and agent traces between components, ensuring each agent can see what happened before, and 2) Carefully track decisions to prevent agents from making conflicting choices. These principles help maintain consistency throughout the system and prevent the "telephone game" problem where important details get lost between agents.

### How can context overflow be managed in agent systems?

As agents work on longer tasks, they can quickly hit context window limits. One approach is using a "context compressor" that intelligently summarizes previous context before passing it to the next agent. This requires careful engineering to ensure important details aren't lost during compression. Another approach is designing systems that are inherently cache-aware, allowing for efficient reuse of previous computations without redundant processing.

### What are "read-only subagents" and when are they useful?

Read-only subagents are limited to gathering information without making decisions that affect the system. They're useful for tasks like searching code, listing files, or checking imports without introducing conflicts. Both Claude and other systems constrain their subagents to these read-only tasks specifically to avoid the problems that arise when multiple agents make independent decisions in parallel.

### Why might a single agent approach be more reliable than multi-agent systems?

Single agent systems avoid the problem of conflicting decisions and context loss between agents. They maintain a continuous "consciousness" with full access to previous context and actions. While they may be slower (lacking parallelism), they're typically more reliable because they don't suffer from coordination problems. A well-designed single agent can still use specialized components internally while presenting a unified interface to users.

### How should agents handle tasks they're uncertain about?

Agents should be designed to recognize their limitations and escalate decisions to humans when appropriate. This includes providing confidence scores with their plans and outputs, so users know when to pay closer attention. Unlike how models are typically trained (to always provide an answer), agents should be willing to say "I don't know" or "I need help" rather than guessing when they lack sufficient information or expertise.

### What's the "edit-apply model" pattern and what are its limitations?

The edit-apply model pattern uses two specialized components: a smart coding model that generates human-readable instructions for code changes, and a simpler, faster model that applies those changes to the code. This pattern can be efficient but introduces fragility because the edit-apply model lacks the full context and intelligence of the main model, making it vulnerable to misinterpreting instructions if they're not perfectly clear.

### Why are current frameworks for building agents considered premature?

Current agent frameworks are considered premature because we're still discovering the fundamental principles and patterns for building reliable agent systems. Similar to web development before React, we're in an early phase where developers are still identifying best practices. Eventually, frameworks will emerge that codify these principles, but for now, it's important to focus on understanding the core concepts like context engineering.

### How might agent collaboration evolve in the future?

While current multi-agent systems face significant challenges, future systems may enable more effective collaboration as models become more intelligent. The ability to model what other agents know and need is a sophisticated skill that requires advanced intelligence. As single agents become more capable, they'll naturally develop the ability to collaborate effectively with other agents, similar to how humans collaborate with teammates.

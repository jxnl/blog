---
title: "How OpenBB Ditched APIs and Put RAG in the Browser (Michael Struwig)"
speaker: Michael Struwig
cohort: 3
description: A novel approach to RAG systems that leverages the browser as a data layer, connecting agents to sensitive data without traditional APIs.
tags: [RAG, browser, function calling, data security, OpenBB]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# How OpenBB Ditched APIs and Put RAG in the Browser (Michael Struwig)

I hosted a session with Michael Struwig, Head of AI at OpenBB, who shared a fascinating approach to RAG systems that leverages the browser as a data layer. This conversation explored how financial data platforms can connect agents to sensitive data without traditional APIs, creating more secure and flexible AI-powered analysis tools.

<!-- more -->

[▶️ See OpenBB's Browser-First RAG Architecture](https://maven.com/p/18bf94){: .md-button .md-button--primary}

## Why is the browser the most natural system for connecting LLMs to data?

Michael's core thesis is that in the age of web apps, the browser serves as the most natural intermediary for shuffling data between systems, particularly for LLMs. While this might seem counterintuitive at first, it elegantly solves several critical problems in the financial industry.

The traditional approach to RAG involves building APIs that allow agents to pull data from external services. OpenBB takes a different path - they use the browser itself as the data layer, allowing their workspace application to connect directly to data sources without requiring data to flow through backend servers.

This browser-first approach provides significant advantages:

- You don't have to distribute sensitive financial data through your servers
- It creates excellent security since you must be on the same network as the data
- You can serve data directly from localhost, which is fantastic for development
- It eliminates legal concerns around data distribution licenses

As Michael explained, "We don't want to distribute your data... there's a lot of legal fuzziness around what counts as distribution. If you've purchased a data license somewhere, are you allowed to distribute it in this way?"

**_Key Takeaway:_** Using the browser as a data layer creates a clean separation between data integration and agent functionality. Once data is integrated into the platform for human use, it's instantly available to AI agents without requiring separate API development or data redistribution.

## How does OpenBB's agent protocol work?

OpenBB developed a protocol that allows agents to request data through the browser rather than directly accessing APIs. The workflow is elegantly simple:

1. The frontend application makes a query request to the agent, specifying available widgets containing data, their descriptions, and parameters

1. If the agent needs specific information, it submits a function call back to the frontend

1. A function calling handler running in the browser locally interprets this call, executes it, and fetches the data

1. The handler responds with a follow-up query containing both the original messages and the results

This creates a powerful separation of concerns - you integrate data once, and your agent doesn't need to know anything about how to access it. The agent simply specifies which widget and input arguments it wants, using a unified interface.

When designing this protocol, Michael emphasized several priorities:

- It must be easy to debug, test, and reason about
- It should use standards people are already familiar with
- It should avoid being overly clever or complex

The resulting API is stateless (the agent doesn't handle state), uses REST (familiar to all web developers), and employs server-sent events (the standard for LLM communication). They've published the entire protocol on GitHub as the "OpenBB custom agent SDK."

I found it particularly interesting how they've created a system with minimal primitives that handle all essential functions - yielding message chunks, reasoning steps, widget data requests, citations, and charts - all through simple yield statements in the execution loop.

**_Key Takeaway:_** By creating a simple, stateless protocol that runs in the browser, OpenBB allows agents to access data that might otherwise be inaccessible due to network constraints or security concerns, all while maintaining a clean separation between data integration and agent functionality.

## What is OpenBB Workspace and how does it leverage this approach?

OpenBB Workspace is an AI-driven analysis tool primarily focused on financial data. It provides a dashboard interface where users can:

- View various data sources like news, watchlists, and company information
- Ask questions to an AI copilot that can access all visible data
- Create charts and visualizations based on analysis
- Bring in custom data backends and write custom widgets

The platform treats the browser as a data layer, allowing users to connect to data sources running on localhost or available via their network. This creates a powerful environment where:

- Users can bring their own data without it flowing through OpenBB's servers
- The AI agent can access this data through the browser
- Everything the human can do, the agent can do as well

Michael emphasized their philosophy that "anything the human can do, the AI must be able to do, and vice versa." This creates a unified interface where humans and AI can collaborate effectively, with the AI leveraging the same tools and data access that humans have.

For enterprise customers, this approach is particularly valuable because they already have their data and don't want data provisioning - they just want a way to analyze it effectively with AI assistance.

**_Key Takeaway:_** OpenBB's approach creates a platform where data flows directly through the browser to both humans and AI agents, maintaining security while enabling powerful analysis capabilities without requiring data to be redistributed through third-party servers.

## How does OpenBB handle state management and function execution?

One of the most interesting aspects of OpenBB's approach is how they handle function execution. Michael described two types of functions:

1. Locally executed functions - The traditional approach where functions run in the same environment where they're called

1. Remotely executed functions - A novel approach where functions are executed in the browser through a mini-interpreter

This remote execution model allows the agent to request data from widgets in the browser without needing direct API access to the data sources. As Michael explained, "Nobody said anything about where the function call needs to be executed."

For state management, OpenBB takes a stateless approach where the workspace handles all state, not the agent. This makes debugging easier, creates reproducible behavior, and simplifies testing since you can hit an endpoint with a payload and get a predictable response without managing complex state.

Their architecture resembles a state machine model with a main execution loop that can drop into sub-modules for specific tasks. For example, when analyzing a PDF, the main agent might recognize it's a PDF and call a sub-agent with its own execution loop specifically designed for PDF analysis. These sub-agents can yield events back up to the main loop, which then yields them to the client.

**_Key Takeaway:_** By using remotely executed functions and a stateless architecture, OpenBB creates a system that's easy to reason about while enabling powerful capabilities like accessing data that would otherwise be inaccessible to remote agents.

## How does OpenBB handle error management and system improvement?

When I asked about their approach to error management and system improvement, Michael's answer was refreshingly straightforward: they look at the logs.

Rather than building complex systems to analyze errors, they:

1. Ensure they have good error messages that help the model try again

1. Keep detailed logs of what goes wrong

1. Look for patterns in those logs

1. Fix the system to make errors less likely

As Michael put it, "It's astounding how just looking at logs... we don't do any crazy, smart stuff. We're a small team. We want to move fast, and we want our systems to be reliable. No, we just go look."

He shared an example where they noticed their agent was consistently generating input arguments for a particular data source even when instructed not to. By identifying this pattern, they realized they needed to make certain input arguments optional, fixing the system rather than trying to improve the prompting.

This approach reminded me of Toyota sending executives to Namibia to watch what breaks on their vehicles in harsh conditions. As Michael noted, "That is surprisingly effective. You don't need workflows. You don't need crazy tooling. Sometimes, just putting your boots on the ground and looking at what's going wrong - that's the highest information signal you can get."

**_Key Takeaway:_** Sometimes the simplest approaches are most effective. Rather than building complex systems to analyze errors, directly examining logs and identifying patterns can provide the highest-quality information for improving your AI systems.

## How does OpenBB manage latency expectations?

For managing user expectations around latency, OpenBB employs two key strategies:

1. Providing continuous status updates - Similar to how ChatGPT shows "searching the web" indicators, OpenBB shows step-by-step reasoning as the agent works. This includes information about which widgets are being accessed, what queries are being made, and what the agent is thinking. As Michael noted, "One of the things you don't want is to have a user sit there wondering what's happening."

1. Parallelizing independent tasks - When querying multiple data sources that don't need to interact, they split the work into parallel processes. For example, when summarizing 10 PDFs, they'll summarize them simultaneously and combine the results rather than processing them sequentially.

These approaches keep users engaged and informed while minimizing perceived latency. As Michael observed, "Users don't seem to complain. You can only read so fast, anyway."

I found his comment about anthropomorphizing LLMs particularly insightful: "Sometimes I think anthropomorphizing LLMs more is a good thing, not a bad thing." Good error messages help both humans and LLMs understand what went wrong, as models are trained on human data and respond well to the same clear communication that helps people.

## What's the future of browser-based AI?

Michael posed a fascinating question that he believes more people should be asking: "When will locally running language models be integrated into browsers, and when will a web standard be published that allows web apps and websites to interact with those language models in a native way?"

He predicts that browsers will eventually have built-in LLMs, with standardized interfaces for web applications to leverage these models. This makes sense because:

- The browser is the most important application on most computers
- The web is effectively "the operating system of the world" now
- Most users won't install specialized AI software, but they already use browsers
- Edge computing for AI is becoming increasingly feasible

When I asked whether this would happen first on desktop or mobile, Michael was confident: "Mobile, almost certainly mobile." The challenge remains monetization - how do big tech companies justify the investment in building these capabilities if they can't generate revenue from them?

**_Key Takeaway:_** The future may involve browsers with native LLM capabilities and standardized interfaces for web applications to leverage these models, creating a more accessible AI ecosystem that doesn't require users to install specialized software.

## How does OpenBB approach testing and evaluation?

Evaluating AI systems in financial analysis presents unique challenges. Unlike code generation where you can run unit tests to verify correctness, financial analysis often involves subjective judgments without clear right or wrong answers.

OpenBB takes a multi-faceted approach to evaluation:

1. User feedback through thumbs up/down ratings (though only about 1% of users provide this)

1. "Radical observability" - providing full citation traces for every answer

1. Direct observation of user interactions and "vibe checks"

1. Detailed logging and pattern recognition

Michael emphasized that "vibe checks" provide surprisingly high-quality information. By examining what the agent saw and the answer it provided, they can identify and fix issues more effectively than through automated systems.

For monitoring and tracing, they use two main tools:

- Magnetic (by Jack Collins) - A minimal LLM framework that provides the right abstraction level
- Logfire - For fast tracing with a good UI and OpenTelemetry compatibility

**_Key Takeaway:_** In domains where evaluation is subjective, combining user feedback with radical observability and direct examination of system behavior can be more effective than complex automated evaluation systems.

## What are the limitations of frameworks like LangChain?

When I asked about his "God forbid" comment regarding LangChain, Michael clarified that while LangChain popularized the important concept of chaining LLM calls together, it has significant limitations:

"It's heavily abstracted. It makes a lot of strong assumptions about how your business logic should work, and it ends up solving the average of a lot of problems. And the issue with solving the average of a lot of problems is... you solve no one's problem."

He explained that LangChain works well for "Hello World" examples, but as soon as you need custom functionality, you find yourself fighting the framework. This has been his experience and that of many others who have tried to build production systems with it.

Instead, OpenBB prefers more minimal abstractions that give them greater control over execution flow. They've found that a state machine model with execution loops works better for their needs, allowing them to drop into specialized sub-modules for specific tasks while maintaining a clean overall architecture.

**_Key Takeaway:_** While frameworks like LangChain can help with initial development, they often become limiting when building production systems that require custom functionality. More minimal abstractions that give you direct control over execution flow can be more effective for complex applications.

**Final thoughts on browser-based RAG**

The browser-as-data-layer approach that OpenBB has developed offers a compelling alternative to traditional API-based RAG systems, particularly for sensitive data in regulated industries. By leveraging the browser's existing capabilities and security model, they've created a system that:

1. Keeps data secure and compliant with licensing requirements

1. Simplifies development by eliminating the need for separate API integration

1. Creates a unified interface for both humans and AI

1. Enables access to data that might otherwise be inaccessible to remote agents

This approach represents a pragmatic solution to real-world constraints around data access and security, demonstrating that sometimes the most elegant solutions come from rethinking fundamental assumptions rather than adding more complexity.

As AI becomes more integrated into our daily tools, approaches like this that leverage existing infrastructure rather than building entirely new systems may prove to be the most sustainable path forward.

---

FAQs:

## What is the main concept behind OpenBB's approach to data integration?

The browser is the most natural system for shuffling data between different systems, particularly when working with Large Language Models (LLMs). Rather than using traditional APIs where an agent hits an endpoint to pull data from external services, OpenBB leverages the browser itself as a data layer. This approach allows you to connect data running on localhost or your local network to an agent running elsewhere, creating a more seamless integration experience.

## What is OpenBB Workspace?

OpenBB Workspace is an AI-driven analysis tool primarily focused on financial data. It features a series of dashboards with various data sources including news, watchlists, company information, and price targets. The platform includes OpenBB Copilot (an AI assistant) on the right side of the application that can answer questions, produce charts, and provide full citations for its responses. Users can create custom widgets, bring in their own data backends, and perform comprehensive analysis.

## Why did OpenBB choose a browser-based approach instead of traditional APIs?

There are several key reasons:

- It eliminates the need to distribute user data through OpenBB's systems, which is resource-intensive and costly
- It avoids legal complications around data distribution, especially with licensed financial data
- It removes the requirement for data to be reachable over a public network
- It provides excellent security since you must be on the same network as the data
- It allows users to serve data directly from localhost, which is ideal for development

## How does the browser-based data integration work technically?

The system uses what OpenBB calls the "agent protocol." When a user makes a query, the front-end application sends a request to the agent with messages and information about available widgets containing data. If the agent needs specific information to answer the query, it submits a function call back to the front-end with parameters specifying which widget to access and which input arguments to use. A function-calling handler running in the browser locally interprets this call, executes it, fetches the data, and responds with the results back to the agent.

## What are the benefits of this approach for developers?

This approach offers several advantages:

- You only need to integrate your data once into OpenBB Workspace
- The agent doesn't need to know how to access the data directly
- There's a clear separation of concerns between data integration and agent functionality
- The system works with any AI system (OpenAI, Anthropic, Google, etc.)
- The protocol is stateless, making it easy to debug, test, and reason about
- It uses familiar REST APIs and server-sent events, which are standard for web development

## Is the agent protocol publicly available?

Yes, OpenBB has published the entire protocol on GitHub. It's called the "OpenBB Custom Agent SDK" and is pip-installable. This is the same protocol used for OpenBB's own copilot, and they encourage users to build their own agents with it.

## What primitives does the agent protocol provide?

The protocol includes several simple primitives:

- Yielding message chunks to stream text back to the front-end
- Yielding reasoning steps to provide status updates about what the agent is doing
- Fetching widget data from OpenBB Workspace
- Producing citations for information sources
- Returning tables and various chart types (pie, line, bar, scatter)

## How do you handle latency in complex workflows?

OpenBB manages user expectations around latency in two main ways:

1. Providing continuous feedback through status updates that show what the model is doing (querying widgets, writing SQL, analyzing data)

1. Parallelizing tasks when possible (e.g., summarizing multiple PDFs simultaneously rather than sequentially)

## How does OpenBB approach error handling and system improvement?

Rather than building complex self-improving systems, OpenBB focuses on:

- Creating clear, informative error messages that help the model try again
- Maintaining detailed logs of errors and identifying common patterns
- Having team members regularly review these logs to spot trends
- Modifying the system to make errors less likely, rather than just changing prompts

## What does OpenBB believe about the future of AI integration?

OpenBB believes that human plus AI will be better than either human or AI alone. Their vision focuses on collaboration rather than replacement, with AI making humans better or offloading certain tasks. They maintain that anything the human can do, the AI must be able to do, and vice versa, creating a unified interface for both. Looking further ahead, they predict that locally-running language models will eventually be integrated directly into browsers as a web standard, particularly on mobile devices.

---

--8<--
"snippets/enrollment-button.md"
--8<--

---

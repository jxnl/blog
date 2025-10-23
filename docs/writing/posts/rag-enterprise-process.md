---
title: How to invest in AI w/ MCPS and Data Analytics
date: 2025-06-09
comments: true
---

> tl;dr: You should build a system that lets you discover value before you commit resources.

!! **Key Takeaways**

Before asking what to build, start with a simple chatbot to discover what users are interested in. There's no need to reach for a complex agent or workflow before we see real user demand.

Leverage tools like Kura to understand broad user behavior patterns. The sooner we start collecting real user data, the better.

This week, I had conversations with several VPs of AI at large enterprises, and I kept hearing the same story: XX teams experimenting with AI, a CEO demanding results for the next board meeting, sales conference, quarterly review, and no clear path from pilot to production.

These conversations happen because I built [improvingrag.com](https://improvingrag.com)—a resource that helps teams build better RAG systems, which has lead me into many conversations from researchers, engineers, and executives. But the questions aren't about RAG techniques. They're about strategy: "How do we go from experiments to production?" "How do we know what to invest in?" "How do we show ROI?"

<!-- more -->

One VP said: "We have teams building everything from internal tools to customer-facing simulations. Some are trying to use AI for supply chain planning, others for compliance checks. The CEO wants something big to announce at our conference in six months, but I don't know which bets will pay off."
The best AI projects start with discovery, not deployment. They build systems that find value before committing resources to production. This means treating AI capabilities as levels of investment, not just "experiment" vs "production."
The solution comes from data engineering's lessons on scalable systems, which mirrors what we saw in 2019 with microservices architecture:

- **Modular services with unified interfaces**: Model Context Protocol (MCP) does for AI what API gateways did for services in distributed systems
- **Shared intelligence layers**: Like data organizations' shared data layers, AI needs layers that learn from every interaction, similar to how microservices shared data through centralized stores
- **Usage-driven architecture**: Let real usage patterns, not assumptions, guide your design, just as we learned to build services based on actual traffic patterns

I'm going to learn on the abstraction of MCP and how it can be used to build a system that lets you discover value before you commit resources.

MCP's "build once, use everywhere" approach enables a single service to power three levels of AI implementation—chatbots, agentic workflows, and custom end-to-end applications—while teams maintain their own MCP servers, similar to how microservices were deployed behind API gateways. This systematic approach to [improving RAG systems](./rag-improving-rag.md) scales across your organization. However, this architecture introduces complexity as services operate across different contexts and teams, requiring unified logging and evaluation systems to track performance everywhere; many teams fail here by fragmenting their observability layer, repeating the same patterns seen in distributed microservices.

Once all this is in place, you can start to build a system that lets you discover value before you commit resources by investing in products (workflows all the way to more niche capabilities) by simply looking at the data.

## The Fragmentation Problem

Here's what I see:

- **Domain experts working alone**: The -insert verticliazed company here- team builds their own chatbot. The compliance team builds another. Customer service builds a third. None of them talk to each other.
- **Too much optimization too early**: Teams jump straight to "Can we fine-tune an LLM for our use case?" before they've even validated the use case exists.
- **No shared infrastructure**: Every team rebuilds logging, evaluation, and deployment.
- **No clear success metrics**: "Make it more AI" isn't a strategy, 'make the ai better' isn't either.

The result? Lots of motion, very little progress.

## Part 1: MCP + Client Form Factors

Instead of treating each AI project as a separate initiative, think of them as points along an investment gradient. The key insight is this: **the same capability should be able to serve test chatbots and production workflows**.

This approach requires two key architectural decisions:

1. Distribute MCP servers across your organization, accessible through unified clients (chatbots, workflows, and custom applications)
2. Build agents that leverage these same underlying services, adding programmatic logic for more deterministic behavior as you identify valuable workflows

The core principle is to invest in capabilities as reusable tools rather than standalone applications. These tools can be deployed in various form factors depending on your needs:

- Simple chatbot interfaces (like Claude desktop) with MCP integrations
- Workflow automation using frameworks like Pydantic AI
- Fully agentic custom applications

The specific form factor should be determined by:

- Success rates of the capability
- Required guardrails and steering mechanisms
- User interaction patterns

Remember: The capabilities themselves are your business's core value. The form factor is just a delivery mechanism that adapts based on the level of control and safety measures needed.

Here's how it works:

### Level 1: Discovery Through Chat

Start by building capabilities as modular services (I recommend using something like Model Context Protocol servers). These can be plugged into a simple chatbot interface.

Why? Because you don't know what you don't know. A chatbot lets users naturally surface use cases you haven't thought of.

But here's the key part: you need to understand what patterns emerge from all those conversations. This is where tools like [Kura](https://usekura.xyz/) become useful. Inspired by Anthropic's [Clio](https://www.anthropic.com/research/clio), Kura analyzes your chat data to automatically discover:

- What users are actually trying to accomplish
- Common request patterns across hundreds of conversations
- Edge cases and failures you didn't anticipate
- Clusters of similar use cases that might warrant dedicated tooling

Instead of manually reviewing thousands of chat logs, Kura uses hierarchical clustering to surface insights like "38% of conversations are about compliance checks" or "users keep asking for real-time schedule updates." This data-driven discovery is what separates random experimentation from strategic investment.

### Level 2: Identified Patterns Become Agents

Once you identify patterns in chatbot usage through conversation analysis, you can determine the best way to automate those workflows. For example, if 10% of all conversations are about checking compliance status, that's a clear signal to build an agent that glues everything together. The implementation details—whether it's a code-based agent, an MCP server, or a Temporal workflow—can be decided based on your specific needs.

The key insight is that your discovery phase MCP servers become the foundation for these automated solutions. You're not starting from scratch or migrating data—you're simply adding programmatic logic to proven, high-value workflows. This is the power of MCP.

### Level 3: High-Value Workflows Get Custom UI

When workflows demonstrate clear value and consistent usage patterns, it's time to invest in purpose-built interfaces. This isn't just about building custom UIs—it's about creating specialized tools that make these proven workflows more efficient and accessible.

The key advantage is that you're building on top of your existing MCP infrastructure. You're not starting from scratch or creating new services—you're enhancing what already works with more sophisticated interfaces and controls. This approach ensures that your investment is backed by real usage data and proven value, rather than speculative features.

### Example: The Compliance Workflow

Let me walk you through how this played out at one company.

**Day 1**: They add schedule data to their chatbot. Users start asking: "Who's working today?"

**Week 2**: A manager asks: "Can you check which contractors haven't completed their compliance paperwork?" The team realizes they need to connect a rag tool to find unsigned contracts. They build an MCP server for it with 1-2 search functions

**Week 4**: Same manager: "Great, now can you send them a reminder or contact them?" The team adds a contact search service and messaging capability—again, augmenting our portfolio of tools (in the form of MCP servers)

Once we know this is very valuable and people are adopting this tool, then maybe we can write a piece of Python code that uses PyTantic AI, set this as a cron job, and then sends a reminders

**Month 2**: This workflow is running daily. They build an agent that:

- Checks the schedule every morning
- Identifies compliance gaps
- Automatically sends reminders
- Escalates if paperwork isn't completed by some predefined deadline

But here's what made this possible: After the first month, they ran their chat logs through Kura and discovered that compliance-related queries made up 40% of all manager interactions.

**Month 4**: This becomes so valuable they build a compliance dashboard with the agent running in the background. Maybe it's a single UI the general contractor can view to make sure everything's on track, and they can one-click call anybody who is missing information.

Notice what happened? They didn't start by saying "Let's build an AI-powered compliance system." They discovered the need through usage, validated it through repetition, and invested based on the value delivered.

## Part 2: Evals and Logs (and the Data Engineering Parallel)

Now we have a bunch of tools, and at some point, someone's going to share a blog post called evals or whatever. We're going to be asked to start thinking about such things.

Here's something VPs with data backgrounds understand: You wouldn't let every analyst compute revenue differently. So why let every AI team define success differently? The [common pitfalls in AI experimentation](./few-shot-foot-guns.md) that teams face can be avoided with proper evaluation frameworks.

Just like data organizations have:

- Standardized data models
- Certified datasets
- Unified logging infrastructure

AI organizations need:

- Standardized evaluation datasets
- Unified logging for all AI clients (chatbot, workflow, or custom app)
- Feedback loops that turn production usage into better evals

This isn't exciting work, but it's the difference between "we have 30 AI experiments" and "we have an AI platform that gets smarter every day."

The most important thing here is that as these AI applications are being used, the data goes somewhere. Without saving that data, having a systematic way of reviewing it and bringing it back into our eval suite (while there's offline test or statistical tests) is crucial. We are not closing the [data flywheel](./data-flywheel.md)

## The Strategic Insight

This isn't just a technical description; it's a strategic one that allows you to lay two separate foundations:

1. **You build a portfolio of tools**: Invest in a diverse set of reusable capabilities that can be combined in different ways.
2. **You create flexible interfaces**: Support multiple ways to access capabilities, from chatbots to custom clients.
3. **You establish [data literacy](./data-literacy.md)**: Train teams to be thoughtful about evaluations and logging, creating a unified approach to data collection and validation.

This aligns with proven [AI engineering leadership principles](./ai-engineering-leaders.md) that focus on business alignment and metric-driven decision making.

## What This Means for Your AI Strategy

If you're a VP of AI staring down a board presentation in six months, here's my advice:

**Month 1-2**: Build the shared infrastructure layer. Get teams building modular services, not single applications. Deploy a simple chatbot interface to start collecting usage data.

**Month 3-4**: Run your chat logs through [Kura](https://usekura.xyz/) to identify usage patterns. Let the clustering analysis show you what people actually do, not what they say they want. The patterns that emerge will be your roadmap. If you need a lot of help check out [improvingrag.com](https://improvingrag.com) or even reach out to me on [email](mailto:work@jxnl.co)

**Month 5-6**: Double down on the top 3-5 workflows measured by `volumn * success_rate * value_per_interaction` . Build agents or custom apps for these. Show ROI.

aside: Don't rush into fine-tuning models or building custom LLMs before establishing your foundation. It's like optimizing database queries before understanding your application's needs. Advanced AI techniques won't deliver value without a system to discover, validate, and scale use cases.

Follow this proven path:

1. Deploy a chatbot
2. Gather usage data
3. Analyze patterns with Kura
4. Build modular services
5. Let value emerge naturally
6. Invest based on results

When your CEO asks for a big announcement, showcase your platform that transforms employee insights into AI capabilities. That's a compelling story that demonstrates real business value.

Last night, if you do know what the economic value is, just build the automation. Skip the chatbots and agents and focus on the work. It might not be where you want to hear, but this is where you make your company more money. But if your goal is just to raise on a higher multiple with AI hype, I totally understand.

---

_Want to dive deeper into implementation details? I'm working on a guide covering MCP patterns, evaluation frameworks, and case studies from the teams who've reached out through improvingrag.com. [Subscribe to improvingrag.com](https://improvingrag.com) for early access and updates._

## Want to learn more?

I also wrote a 6 week email course on RAG, where I cover everything in my consulting work. It's free and you can:

[Check out the free email course here](https://dub.link/6wk-rag-email){ .md-button .md-button--primary }

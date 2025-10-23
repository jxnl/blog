---
title: "Domain Experts: The Lever for Vertical AI"
speaker: "Chris Lovejoy (Anterior)"
cohort: 3
description: "How to successfully apply LLMs in specialized industries by building domain‑expert review loops, augmenting prompts with expert knowledge, and earning customer trust."
tags: [vertical AI, domain experts, evaluation, prompting, trust, security]
date: 2025-09-11
categories: [Speaker Series, RAG]
---

# Domain Experts: The Lever for Vertical AI — Chris Lovejoy (Anterior)

I hosted a session featuring Chris Lovejoy, Head of Clinical AI at Anterior, who shared valuable insights from his experience building AI agents for specialized industries. Chris brings a unique perspective as a former medical doctor who transitioned to AI, working across healthcare, education, recruiting, and retail sectors.

<!-- more -->

[▶️ Lessons from building verticalized AI agents](https://maven.com/p/504453/lessons-from-building-verticalized-ai-agents?utm_medium=ll_share_link&utm_source=instructor){.md-button .md-button--primary}

## Why is it so hard to successfully apply LLMs to specialized industries?

Chris identified two fundamental challenges when implementing AI in vertical industries:

- The "last mile problem" — taking powerful models and making them work in specific customer contexts. The challenge isn't reasoning quality anymore; today's models fail because they lack context on how workflows are performed in specific industries.
- Difficulty defining "good" and "correct" — in specialized fields, determining what constitutes a good output requires domain expertise that most AI engineers don't possess.

As Chris explained, "If your data looks like a legal document and you're not a lawyer, you wouldn't know whether it's right or wrong." This highlights why domain experts are essential for vertical AI applications.

## How can domain experts supercharge AI development?

Chris recommends implementing a systematic review process with domain experts that creates a powerful feedback loop:

1. Your production application generates AI outputs
2. Domain experts review these outputs to provide:
   - Performance metrics (accuracy scores)
   - Categorized failure modes
   - Suggested improvements
   - Input–output pairs for training
3. This expert‑generated data enables you to prioritize work based on which failure modes most impact your key metrics. You can create ready‑made failure mode datasets grouped by error type, allowing engineers to test improvements against specific problems.

The most effective process is a continuous loop where:

1. Production generates outputs
2. Domain experts review and categorize issues
3. A domain expert PM prioritizes which failure modes to fix
4. Engineers test changes against failure mode datasets
5. The PM approves changes to go live

**Key Takeaway:** Domain experts aren't just helpful — they're essential for vertical AI applications. Building systems to capture their insights creates a data‑driven improvement cycle that addresses the specific needs of specialized industries.

## What's the best way to implement domain expert reviews?

While many companies start with simple tools like Google Sheets or raw traces in monitoring tools, Chris strongly recommends building a custom review dashboard. This approach gives you maximum freedom over how you present information and makes it easier to integrate review data into your production systems.

A well‑designed review UI should optimize for:

- High‑quality reviews (prioritize quality over quantity)
- Minimizing time spent by reviewers
- Generating actionable data

When building a custom UI, follow these principles:

- Clearly surface all required context (separate wider context from specific details)
- Optimize the review flow sequence (bake your ideal review process into the UI)
- Minimize friction (reduce scrolling, clicking, and manual work)

Chris has found that spending time shadowing domain experts as they review outputs helps you understand their natural workflows, which you can then incorporate into your UI design.

## Should I use prompting or fine‑tuning for vertical AI applications?

Chris believes better prompting beats fine‑tuning for improving performance in most vertical applications. This might seem counterintuitive, but he offers several reasons:

- Today's out‑of‑the‑box models already have strong domain‑specific reasoning capabilities
- Fine‑tuning adds complexity (managing multiple models for different tasks and customers)
- Fine‑tuned models can degrade as workflows evolve over time

While fine‑tuning has benefits for speed, cost, and scalability, Chris recommends starting with prompting for performance improvements.

However, he doesn't mean just tweaking prompt text — that approach can be brittle and model‑dependent. Instead, he focuses on two more powerful techniques:

1. Use context augmentation — inject domain expert‑generated knowledge into your prompts at inference time. For example, in finance, you might include the specific definition of "high net worth individual" used by a particular bank.
2. Leverage input–output pair examples for in‑context learning — include examples where the model initially made mistakes, along with the corrections from domain experts.

The most powerful approach is to go beyond static prompting by implementing dynamic retrieval of this knowledge. Your domain expert UI generates knowledge that lives in a domain knowledge base, which you can then retrieve in real‑time during inference using techniques like:

- Keyword matching
- Semantic similarity
- Recency weighting
- Diversity optimization

**Key Takeaway:** Rather than fine‑tuning models, focus on dynamically augmenting prompts with domain‑specific knowledge and examples. This approach is more adaptable to changing workflows and customer needs.

## How do I build and maintain customer trust?

For verticalized AI agents, Chris identifies three key factors for customer trust:

- Confidence in the AI's performance
- Confidence in secure data handling
- Protection against LLM‑specific attack vectors

To build confidence in AI performance, implement these practices:

- Review production outputs and generate performance metrics
- Report these metrics to customers regularly (biweekly or monthly)
- Define a sampling strategy as you scale (based on uncertainty, outliers, or stratified sampling)
- Establish an internal response protocol for performance issues
- Consider using LLMs as judges to help scale monitoring

Chris shared a case study from a healthcare application where they couldn't manually review all AI outputs — they could only review about 5%. They implemented an LLM judge system that:

- Scored the confidence of each AI output in real‑time
- Prioritized which cases humans should review
- Provided performance metrics for all outputs
- Created a feedback loop where human reviews improved the judge system

For data handling, Chris recommends:

- Mapping out your data usage strategy early (during contract negotiations)
- Being ready to offer isolated, single‑tenant environments
- Investing in synthetic data generation for testing and training

For LLM‑specific security, stay vigilant about:

- Prompt injections (using input filtering and validation)
- Sensitive information disclosure (through data sanitization)
- Data and model poisoning (tracking data origins and using version control)

**Key Takeaway:** Building trust requires transparent performance monitoring, secure data handling, and proactive security measures. Implement systems that give customers visibility into AI performance while protecting their sensitive information.

## Which domain experts should you hire and how should you use them?

Chris strongly recommends hiring a principal domain expert who has ultimate responsibility for your AI's performance. This approach has several advantages:

- Organizational clarity (having a DRI helps you move faster)
- Avoiding consensus by committee
- Building deep intuition about your AI system's performance

This person should be hired early and given ownership to shape your product. Beyond reviewing outputs, they can:

- Help hire and manage additional reviewers
- Define sampling strategies
- Analyze review data
- Monitor reviewer performance
- Steer product development
- Talk to customers
- Improve AI performance

When hiring this principal domain expert, look for someone who meets a critical domain expertise threshold but also has additional skills like:

- Management/leadership experience
- Statistical knowledge
- Product development experience
- Technical understanding

At Anterior, Chris played this role with his medical background, which allowed him to review outputs, hire additional reviewers from his healthcare network, define sampling strategies using his data science background, and contribute to AI implementations with his software engineering skills.

**Key Takeaway:** A principal domain expert who combines industry knowledge with leadership and technical skills can dramatically accelerate your ability to build effective vertical AI applications. This person becomes the bridge between domain expertise and technical implementation.

## How do you handle citations and references in AI‑generated content?

For citation handling, Chris mentioned they've used both custom approaches and vendor solutions like Anthropic's citation API. One effective technique they've implemented is:

1. Chunk content with semantic similarity‑based methods
2. Assign unique IDs to each chunk
3. Prompt the model to first identify relevant evidence chunks by their UIDs
4. Have the model reason using those specific chunks
5. Make the final decision with clear references to the source material

This sequential approach ensures the model explicitly references the information it used, making the reasoning process more transparent and traceable.

## What question are teams not asking themselves when building these systems?

When I asked Chris what question teams aren't asking themselves, he identified: "What does your system look like for incorporating domain expertise?"

He noted many teams focus on using the latest, most sophisticated models while neglecting the process for systematically incorporating domain knowledge. The real challenge isn't just implementing the model — it's creating a flywheel that continuously improves your system based on expert feedback.

Unlike traditional software where you build features and move on, AI systems require ongoing optimization to push the probability distribution in the right direction. Building this improvement flywheel is essential for successful vertical AI applications.

**Key Takeaway:** Don't treat AI applications like traditional software that you build once and maintain. Instead, design systems that continuously incorporate domain expertise to systematically improve performance over time.

---

## FAQs

## What makes applying LLMs to specialized industries so challenging?

The primary challenge lies in the "last mile problem" — taking powerful models and making them work effectively in specific industry contexts. While today's models have strong reasoning capabilities, they often lack the contextual understanding of how specific workflows operate in specialized industries. Additionally, defining what constitutes "good" or "correct" output in these domains requires domain expertise that general AI practitioners may not possess.

## How can domain experts improve AI development in vertical industries?

Domain experts are invaluable when your AI is processing specialized data that general practitioners can't properly evaluate. By implementing a structured review process with domain experts, you can gather four critical types of information:

- Performance metrics that show how well your AI is performing
- Specific failure modes that categorize where and how your AI makes mistakes
- Suggested improvements based on domain knowledge
- High‑quality input–output pairs for training and evaluation

This information enables you to prioritize improvements, create targeted datasets for testing, and implement a continuous improvement cycle that addresses real‑world usage patterns.

## What's the most effective way to support domain experts in reviewing AI outputs?

While you can start with basic tools like spreadsheets or third‑party evaluation platforms, building a custom review dashboard is the highest‑leverage investment you can make. A well‑designed custom UI should:

- Clearly surface all required context without overwhelming reviewers
- Optimize the review flow sequence to match how experts naturally evaluate information
- Minimize friction by reducing unnecessary scrolling and clicking
- Generate actionable data that can be directly integrated into your production system

The goal is to balance high‑quality reviews with reviewer efficiency while generating data that can immediately improve your system.

## Is fine‑tuning or prompting better for verticalized AI agents?

For most vertical applications, advanced prompting techniques are more effective than fine‑tuning. Today's out‑of‑the‑box models already have strong domain‑specific reasoning capabilities, and the typical issues in vertical applications relate more to context than reasoning ability. Fine‑tuning adds complexity through model management and can become outdated as workflows evolve.

That said, fine‑tuning may still be valuable for optimizing speed, reducing costs, or improving scalability in certain scenarios.

## What prompting techniques work best for vertical applications?

Rather than just tweaking prompt wording (which can be brittle and model‑dependent), two more robust techniques are particularly effective:

- Context augmentation: Injecting domain‑specific knowledge into the prompt context at inference time, such as customer‑specific definitions or guidelines
- Input–output pair examples: Using few‑shot prompting with real examples to demonstrate the desired behavior

These approaches can be implemented dynamically, retrieving the most relevant context based on the specific query and customer needs.

## How can you build and maintain customer trust in vertical AI applications?

Building trust requires addressing three key areas:

- Performance confidence: Conduct regular reviews of production outputs, report metrics to customers, implement strategic sampling as you scale, and establish clear response protocols for performance issues
- Data security: Map out your data usage strategy early (ideally during contracting), be prepared to offer isolated environments for security‑conscious customers, and consider investing in synthetic data generation
- Security against LLM‑specific threats: Implement protections against prompt injection, prevent sensitive information disclosure, and stay current with evolving best practices in LLM security

Transparent communication about these measures helps customers understand your commitment to reliability and security.

## What role should domain experts play in your organization?

Consider hiring a principal domain expert who serves as the direct responsible individual (DRI) for AI performance. This person should:

- Define what constitutes "good" or "correct" output
- Build intuition about how your AI system performs and how it can be improved
- Help hire and manage additional reviewers as you scale
- Define sampling strategies for efficient review
- Analyze review data and monitor reviewer performance
- Steer product development and prioritize engineering work
- Communicate with customers about performance and improvements

The ideal candidate combines domain expertise with additional skills like management experience, statistical knowledge, and product development capabilities.

## How can you create an effective continuous improvement cycle?

Implement a structured loop where:

1. Your production application generates AI outputs
2. Domain experts review a strategic sample of those outputs
3. Reviews produce performance metrics and categorized failure modes
4. Product managers prioritize which failure modes to address
5. Engineers make changes and test against failure mode datasets
6. Changes are validated and deployed to production

This cycle allows you to systematically improve performance based on real‑world usage patterns and domain‑specific requirements.

## How can you scale performance monitoring as your application grows?

As you scale and can no longer review all outputs, implement a strategic sampling approach based on:

- Uncertainty levels in the AI's responses
- Outlier detection to identify unusual cases
- Stratified sampling across different characteristics

You can also implement an LLM‑as‑judge system that evaluates outputs in real‑time, providing confidence scores that help prioritize which cases need human review and potentially taking automated actions for low‑confidence outputs.

---

## Connect with Chris Lovejoy

- **[Book time here](https://forms.fillout.com/t/uYXsRp2K8Pus)** - Schedule a consultation with Chris
- **[Sign up to mailing list here](https://chrislovejoy.me/email)** - Get updates on vertical AI insights

## Additional Resources

**Chris Lovejoy's Talks & Content:**

- **[How to build an LLM-Native Expert System](https://www.youtube.com/watch?v=MRM7oA3JsFs)** - Dr Chris Lovejoy, AI Engineer World's Fair (SF, June 2025)
- **[Why custom AI review dashboards transform AI products - and how to build one](https://chrislovejoy.me/review-dashboard)** - Dr Chris Lovejoy
- **[Mission-Critical Evals at Scale](https://www.youtube.com/watch?v=cZ5ZJy19KMo)** - Dr Chris Lovejoy, AI Engineer Summit (NY, Feb 2025)
- **[Why you need a principal domain expert for building vertical AI - and how to find them](https://chrislovejoy.me/domain-expert-vertical-ai)** - Dr Chris Lovejoy

**Industry Resources:**

- **[2025 Top 10 Risks and Mitigations for LLM Applications & Generative AI](https://genai.owasp.org/llm-top-10/)** - OWASP

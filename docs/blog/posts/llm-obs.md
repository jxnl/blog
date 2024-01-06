---
draft: False
date: 2023-04-04
slug: stitchfix-framework
tags:
  - stitchfix
  - python
  - data science
  - data engineering
  - data pipelines
  - data architecture
authors:
  - jxnl
---

# LLM Observability is just plain observability

## Plain old telemetry

Many current AI agents lack proper observability, which makes it hard to evaluate and fine-tune their performance in production. To solve this problem, we can instrument our agents with Open Telemetry and use powerful tools such as Prometheus, Grafana, and Datadog to bring transparency to their actions, but that's not all. We need to integrate them back into AI agents in a meaningful way.

We need something to provide the missing link by exporting telemetry data that can be used to observe not just the single POST request to **`openai.Completion.create`**, but the entire task. With proper logging of the prompts and completions, we can generate end-to-end telemetry for complex agent actions, whether it's question answering, synthesis, or taking autonomous actions.

Imagine a conversational agent that answers questions using SQL in natural language. It accesses different datasources via a Router Agent and generates SQL queries, calls the DB to return a list of tuples that it then uses to generate a natural language response. If the database errors or the latency increases, we need to know whether it's the LLM, the generated SQL, or the DB that's causing the issue.

Open Telemetry can help us answer these questions and provide insight into the agent's complete actions and relate each component to each other. Once we have this information, we can improve our system engineering to make it more performant, robust, and alert on and detect incidents.

## **But what's next?**

Well, what if this same telemetry data can be used for model-guided self-evaluation, making it the key to scalable model evaluation?

With the export of traces, it's could be possible to generate evaluations based on the complete call graph of the task. For example, given the entire span of the user journey, give me all events that resulted in p95 calls to the DB or the ones that threw errors. We can pass this data back into the LLM and say: “Given this entire tree of calls, return to me the set of data I need to finetune the components of this agent now that you know how the entire sequence of actions happened and their outcomes, give it to me in whatever format makes sense, give it to me.” It could, for example, rank retrieved documents for relevance versus misleading and improve the retrieval model specific for question answer tasks that matched some criteria. It could look at an error-correcting cycle of calls and generate the correct data to.

## **Telemetry… Is Just End-to-End Self-Evaluation?**

Maybe telemetry for AGI is just the detailed diary one uses for reflection and improvement? With the help of something as simple as good telemetry, we can gain true observability into agents' actions and build applications that generate end-to-end evaluations of complex agent actions, something that benefits both humans and computers.

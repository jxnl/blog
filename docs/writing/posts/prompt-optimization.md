---
authors:
  - jxnl
categories:
  - Software Engineering
comments: true
date: 2024-05-22
description: Explore prompt optimization techniques to enhance content generation
  quality using few-shot examples and effective evaluation methods.
draft: false
tags:
  - prompt optimization
  - machine learning
  - few-shot learning
  - content generation
  - AI techniques
---

# What is prompt optimization?

Prompt optimization is the process of improving the quality of prompts used to generate content. Often by using few shots of context to generate a few examples of the desired output, then refining the prompt to generate more examples of the desired output.

<!-- more -->

## Understanding Hyperparameters

Hyperparameters are settings that control a machine learning model's behavior, like learning rate, batch size, and epochs.

In prompt optimization, few-shot examples act as hyperparameters. Few-shot learning uses a small number of examples to guide the model's responses.

By treating few-shot examples as hyperparameters, we can find the best set by experimenting with different combinations, evaluating outputs, and refining the selection.

## The number one assumption

The big assumption you can make here is that there actually exists a function to score the quality of outputs. This might be possible in simple benchmark tests, but in production, this is often impossible. It is not just that I want a summary, but I might want summaries with certain formatting or certain rules of a certain length, and these are all very hard to quantify into a scoring system. You might need to use an llm as a judge, which just further complicates the whole process.

1. How do you score the effectiveness of a motivational speech?
2. What is the score for a persuasive product description?
3. How do you evaluate the quality of a heartfelt apology letter?
4. What is the score for an engaging social media post?
5. How do you rate the impact of a compelling storytelling narrative?

```python
def score(expected, output):
    # This is a placeholder for the actual scoring function
    return ...
```

## Generating Examples

The second thing to focus on is whether or not you already have existing examples or a few shot examples to use in your prompting. Let's assume for now we have some list of examples that we either AI generate or pull from production.

```python
examples = from_prod_db(n=100)
# or
examples = generate_examples(n=100)
```

## Searching for the best examples

Now that we have our examples, we can begin the process of identifying the most effective examples. This involves generating few-shot examples, scoring them, and iteratively refining our selection. By systematically evaluating different combinations of examples, we aim to find the optimal set that yields the highest quality outputs.

```python
from ai_library import llm, score_fn

N_FEW_SHOTS = 10

examples = generate_examples(n=100)
tests = generate_tests(n=100)

prompt = """
You task is to do X

<examples>
{% for example in examples %}
{{ example }}
{% endfor %}
</examples>

Compture the answer for the following input:

{{ input }}
"""

best_examples = None
best_score = float('-inf')

while True:

    # Randomly sample few-shot examples
    few_shot_examples = random.sample(examples, n=N_FEW_SHOTS)

    scores = []

    for inputs, expected in tests:

        # Format the prompt with examples and inputs
        prompt_with_examples_and_inputs = prompt.format(
            examples=few_shot_examples, input=inputs
        )

        # Generate output using the language model
        output = llm.generate(prompt_with_examples_and_inputs)

        # Score the generated output
        scores.append(score_fn(expected, output))

    # Update the best score and examples if current score is better
    if mean(scores) > best_score:
        best_score = mean(scores)
        best_examples = few_shot_examples
```

### Optimizations

We can improve our approach by being more strategic in how we subsample the examples and generate the few-shot examples. Additionally, we can replace the `while` loop with a `for` loop that iterates over a grid of hyperparameters.

However, this entire process relies on having a reliable function to score the quality of outputs. While this might be feasible in controlled benchmark tests, it becomes significantly more challenging in a production environment. In practice, 90% of your effort will be spent on producing data, with only 10% dedicated to tuning hyperparameters.

## Conclusion

In conclusion, optimizing prompts and selecting few-shot examples seems straightforward but relies on assumptions about data quality and output scoring. The approach appears simple but ensuring representative data and accurate scoring is still where most of the complexity lies.

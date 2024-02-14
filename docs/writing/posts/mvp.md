---
draft: False
date: 2024-02-13
slug: mvp
categories:
  - Personal
authors:
  - jxnl
---

# How to ship an MVP for AI applications

What is an MVP?

> A minimum viable product (MVP) is a version of a product with just enough features to be usable by early customers who can then provide feedback for future product development.

The analogy I often use is one where I need something to help me get from point A to point B. Maybe the vision is to have a car. But the MVP is not a chassis without wheels or an engine. Instead it might look like a skateboard. Maybe you'll ship and realised You need brakes or the ability to steer. So instead you ship a scooter. Afterwards you find that you need a little more leverage by having larger wheels and stumble upon a bicycle. Afterwards you find yourself limited by the force that you can apply as a human being. And I started thinking about motors. You can build a moped, an e-bike, a motorcycle. And one day, we'll ship the car.

But today I want to focus on what that looks like when we ship AI applications.

I propose that we just need to understand:

1. What does 80% mean?
2. What are the segments of your users that we can serve well?
3. Can we double down on the segments that we serve well and educate the users about the segments that we don't serve well?

<!-- more -->

## Consider the 80/20 rule: What does 80% mean?

When we talk about something being 80% done or 80% ready, we usually refer to the classical machine learning sense. In this context, each component is deterministic, so 80% likely means that 8 out of 10 features are complete. Once we have the remaining 2 features, we can ship the product. IF we want to follow the 80/20 rule, we might be able to ship the product with 80% of the features and then add the remaining 20% later, like a car without a radio or air conditioning.

However, this definition may not apply to an AI-powered application. The meaning of 80% can vary significantly in this case.

### The issue with Summary Statistics

![](https://upload.wikimedia.org/wikipedia/commons/e/ec/Anscombe%27s_quartet_3.svg)

> The above image is a classic example of Anscombe's quartet. It's a set of four datasets that have nearly identical simple descriptive statistics, yet have very different distributions and appearances. This is a classic example of why summary statistics can be misleading.

Consider the following example:

| Query_id | score |
| -------- | ----- |
| 1        | 0.9   |
| 2        | 0.8   |
| 3        | 0.9   |
| 4        | 0.9   |
| 5        | 0.0   |
| 6        | 0.0   |

**The average score is 0.58**. However, if we analyze the queries within segments, we might discover that we are serving the majority of queries exceptionally well!

!!! note "Admitting what you're bad at"

    If you can accurately identify when something will perform poorly and confidently reject it, then you might be ready to ship a great product while educating your users about the limitations of your application. Saying what you're bad at is a great way to build trust with your users.

The behavior of a probabilistic system could also be very different, consider the following example:

| Query_id | score |
| -------- | ----- |
| 1        | .59   |
| 2        | .58   |
| 3        | .59   |
| 4        | .57   |

In contrast, a system like this also has the same average score of 0.58, but it's not as easy to reject any subset of requests...

It is very important to understand the limitations of your system and to be able to confidently understand the charactersitics in your system beyond summary statistics.

### Learning to say no

Consider an RAG application, where a large proportion of the queries are regarding timeline queries. If our search engines do not support this time constraint, we will likely not be able to perform well.

| Query_id | score   | query_type   |
| -------- | ------- | ------------ |
| 1        | 0.9     | text search  |
| 2        | 0.8     | text search  |
| 3        | 0.9     | news search  |
| 4        | 0.9     | news search  |
| 5        | **0.0** | **timeline** |
| 6        | **0.0** | **timeline** |

If we're in a pinch to ship, we could simply build a classification model that detects whether or not these questions are timeline questions and throw a warning. Instead of constantly trying to push the algorithm to do better, we can simply educate the user and educate them by changing the way that we might design the product.

!!! note "Detecting segments"

    Detecting these segments could be accomplished in various ways. We could construct a classifier or employ a language model to categorize them. Additionally, we can utilize clustering algorithms with the embeddings to identify common groups and potentially analyze the mean scores within each group. The sole objective is to identify segments that can enhance our understanding of the activities within specific subgroups.

By changing the design of our application and understanding the limitations, we can have conditionally better performance if we know what kind of work we can turn down. If you are able can put this segment data into some kind of In-System Observability, you'll be able to safely monitor what proportion of questions you're turning down, and prioritize your work to maximize coverage.

One of the worst things you can do is to spend months building out a feature that only increases your productivity by a little while ignoring some more important segment of your user base.

### Importance of Niching Down

One of the dangerous things I've really noticed working with startups is that we often think that the AI works at all...
As a result we want to be able to serve a large general application without much thought into what exactly we want to accomplish.

In my opinion, most of these companies should really try to focus on one or two significant areas and identify a good niche to target. If your app is good at one or two tasks, there's no way you could not find a hundred or two hundred users to test out your application and get feedback quickly. Whereas, if your application is good at nothing, it's going to be hard to be memorable and provide something that has repeated use. You might get some virality, but very quickly you're going to lose the trust of your users and find yourself in a position where you're trying to reduce churn.

When we're front loaded the ability to use GPT-4 to make predictions, time to feedback is very important. If we can get feedback quickly, we can iterate quickly. If we can iterate quickly, we can build a better product.

## Conclusion

In conclusion, the MVP for an AI application is not as simple as shipping a product with 80% of the features. Instead, it requires a deep understanding of the segments of your users that you can serve well and the ability to educate your users about the segments that you don't serve well. By understanding the limitations of your system and niching down, you can build a product that is memorable and provides something that has repeated use. This will allow you to get feedback quickly and iterate quickly, ultimately leading to a better product.

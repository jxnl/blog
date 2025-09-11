---
draft: true
date: 2025-01-02
authors:
  - jxnl
categories:
  - Strategy
  - Philosophy
  - Software Engineering
---

# Code as Craft: What Musashi's Carpenter Can Teach Us About Software

<!-- more -->

!!! quote "Book of Five Rings"

    The comparison with carpentry is through the connection with houses. Houses of the nobility, houses of warriors, the Four houses, ruin of houses, thriving of houses, the style of the house, the tradition of the house, and the name of the house. The carpenter uses a master plan of the building, and the Way of Strategy is similar in that there is a plan of campaign. If you want to learn the craft of war, ponder over this book. The teacher is as a needle, the disciple is as thread. You must practice constantly.

    Like the foreman carpenter, the commander must know natural rules, and the rules of the country, and the rules of houses. This is the Way of the foreman.

    The foreman carpenter must know the architectural theory of towers and temples, and the plans of palaces, and must employ men to raise up houses. The Way of the foreman carpenter is the same as the Way of the commander of a warrior house. In the construction of houses, choice of woods is made.

    Straight un-knotted timber of good appearance is used for the revealed pillars, straight timber with small defects is used for the inner pillars. Timbers of the finest appearance, even if a little weak, is used for the thresholds, lintels, doors, and sliding doors, and so on. Good strong timber, though it be gnarled and knotted, can always be used discreetly in construction. Timber which is weak or knotted throughout should be used as scaffolding, and later for firewood.

    The foreman carpenter allots his men work according to their ability. Floor layers, makers of sliding doors, thresholds and lintels, ceilings and so on. Those of poor ability lay the floor joists, and those of lesser ability carve wedges and do such miscellaneous work. If the foreman knows and deploys his men well the finished work will be good. The foreman should take into account the abilities and limitations of his men, circulating among them and asking nothing unreasonable. He should know their morale and spirit, and encourage them when necessary. This is the same as the principle of strategy.

## The Architecture of Code

When I first read this passage, I couldn't help but see the parallels to how we build software. The foreman carpenter choosing timber based on its qualities and purpose - isn't this exactly what we do when we architect systems?

### The Visible and the Hidden

Consider the "revealed pillars" versus the "inner pillars." In software, our public APIs and user interfaces are like those revealed pillars - they need to be straight, unknotted, of good appearance. These are what users see and interact with. Meanwhile, our internal services and private methods are the inner pillars. They might have "small defects," but they're structurally sound and do their job.

This aligns with what Clean Code teaches us about layers of abstraction - each layer should look and feel different because it serves a different purpose. The high-level policy code reads like prose. The mid-level orchestration has a different texture. The low-level implementation details are dense and mechanical. Just as a visitor to a temple experiences different materials at different points - polished wood at the entrance, rough stone in the foundations - our code deliberately varies its appearance based on its role.

The beauty of this approach is that the quality becomes self-documenting. When you see meticulously crafted, thoroughly tested code with careful naming, you immediately know you're looking at a load-bearing pillar. When you encounter a quick-and-dirty script with inline configurations and hardcoded values, you recognize scaffolding. Just by looking at the quality of the wood, the carpenter knows its purpose. Just by looking at the quality of the code, we know what we're working on.

Users visiting our applications are like visitors to a temple. They see the beautiful entrance, the polished interfaces, but they don't need to know about the complex plumbing underneath - the message queues, the caching layers, the database optimizations.

### Nothing Goes to Waste

What strikes me most is Musashi's insistence that even weak, knotted wood has its place - first as scaffolding, then as firewood. In our world, this is profoundly relevant as AI begins to generate more of our code.

That boilerplate code that ChatGPT or Copilot generates? It might be our scaffolding - good enough to get us building, knowing full well it'll be refactored or replaced later. It serves its purpose in the moment, getting us to a working prototype quickly. But we don't confuse it with the load-bearing pillars of our architecture.

### Scaffolding to Firewood

But there's another category Musashi mentions - timber that becomes scaffolding, then later firewood. This perfectly describes so much of our code. The scaffolding isn't part of the final structure, but you can't build without it.

Think about all the scaffolding we erect in software: the logging decorators we wrap around functions to debug issues, the temporary migration scripts that help us move between database schemas, the hooks we implement for observability. These aren't beautiful. They're often gnarly, pragmatic solutions - Python decorators hastily written to trace execution, monitoring scripts that barely hold together.

And that's exactly right.

This scaffolding code helps us build and maintain the real structure. Once it's served its purpose - once we've debugged the issue, completed the migration, understood the performance bottleneck - we tear it down. Some of it becomes "firewood," repurposed for the next debugging session. Some of it just gets deleted.

The principle here is profound: write code so that the easy code is easy to delete, and the hard-to-delete code is actually important. Your scaffolding should come down with a few quick commands. Your debugging hooks should vanish without a trace. But those core abstractions? Those should be so intertwined with the system that removing them would mean rebuilding everything.

The mistake would be confusing this scaffolding with our pillars. The core APIs, the domain models, the fundamental abstractions - these are our carefully selected timber. The nouns and verbs we define in our SDKs become the vocabulary of our system. They need to be straight-grained and unknotted because changing them later means reconstructing the entire building.

### Deploying According to Ability

The foreman carpenter's approach to team allocation feels especially prescient. "Those of poor ability lay the floor joists, and those of lesser ability carve wedges." This isn't about devaluing anyone's contribution - it's about recognizing that different tasks require different levels of expertise.

In software teams, junior developers might handle the "floor joists" - the CRUD operations, the basic implementations. Senior engineers focus on the "architectural theory of towers and temples" - the system design, the critical abstractions that will determine whether our house stands or falls.

And now, with AI as part of our toolkit, we have a new kind of team member. AI can carve those wedges, lay those joists, generate that scaffolding code. But choosing which timber becomes a pillar? Knowing the natural rules and the rules of the country? That still requires human judgment.

### The Master Plan

"The carpenter uses a master plan of the building, and the Way of Strategy is similar in that there is a plan of campaign."

Our system architecture is that master plan. It's not just about the code we write today, but understanding how the pieces fit together, how the system will evolve, what loads it needs to bear. The best architects, like the best carpenters, can see the finished structure before the first line of code is written.

## A Craft Worth Practicing

Musashi writes, "The teacher is as a needle, the disciple is as thread. You must practice constantly." In an age where AI can generate code in seconds, this reminder about constant practice might seem outdated. But I think it's more relevant than ever.

The craft isn't just in writing code - it's in knowing which code matters, where to place it, how to organize our teams, when to use the strong timber and when the scaffolding will do. It's in understanding that even as our tools evolve, the fundamental challenges of building things that last remain remarkably constant.

Whether we're building temples or software, the Way remains the same: know your materials, deploy your resources wisely, and remember that every piece - from the finest pillar to the humblest wedge - has its role to play.

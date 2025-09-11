# Chapter 3 Slides

## jxnl.co

@jxnlco

## Systematically Improving RAG Applications

**Session 3:** The Art of RAG UX: Turning Design into Data

Jason Liu

---

## Today's Goals

**From Synthetic Data to Real User Feedback**

- Design systems that collect high-quality user feedback
- Master streaming techniques for better user experience
- Learn prompting and Chain of Thought best practices
- Turn every user interaction into training data
- Bridge the gap between synthetic and real-world data

**Focus: Small UX changes = 5-10x more feedback**

<!-- 
Speaker Notes:

Welcome to session three of systematically improving RAG applications. In this session, we're going to talk about the art of RAG UX, and in particular, how we can turn design into data.

The three goals for today are to make sure we're taking actions to collect feedback, expand on what is possible with streaming, and give a small set of prompts and UX tips to improve satisfaction and quality of answers.

You'll really be surprised at how some minor changes can have 2x to 5x to even 10x more impact on our ability to collect high-quality feedback. The first two sessions have been around creating synthetic data, and now we want to figure out how we can collect that user data and give users a good experience.
-->

---

## Course Context: Building the Data Flywheel

### Sessions 1-2: Foundation
- **Session 1:** Synthetic data and evaluations (faking it)
- **Session 2:** Fine-tuning on synthetic data (making it)

### Session 3: The Bridge ← Today
- **Goal:** Collect real user data to supplement synthetic work
- **Challenge:** How to get users to give us quality feedback
- **Opportunity:** Design choices that 5-10x feedback volume

### Sessions 4-6: Data-Driven Optimization
- Use real feedback for segmentation and improvement

<!-- 
Speaker Notes:

In the first two sessions, we talked about the importance of looking at your data, and in this session, we're going to talk about how we collect feedback. User feedback is the second most important thing after looking at your input data. We need to think about how we can drive users to give us that feedback.
-->

---

## The Feedback Collection Hierarchy

**Most Important:** Looking at your input data  
**Second Most Important:** Getting user feedback

**The Problem:** Most systems collect terrible feedback
- Vague thumbs up/down with no context
- Hidden or hard-to-find feedback buttons
- No follow-up questions to understand failures
- Feedback that doesn't correlate with actual problems

**The Opportunity:** Small design changes → massive data improvements

<!-- 
Speaker Notes:

Let me give you a simple example. Look at these two designs - what kind of behavior do you think each is encouraging? Does this behavior help my team collect data? 

In the first example, we have very small buttons that are hard to find. In the second example, not only are the buttons massive, but we also think about the copy that we collect. This is really important - sometimes when we have negative feedback, it's not clear what's going wrong. It could take too long, be too wordy, or be very unclear.

But if we change the copy to something more specific like "Did we answer your question today?" or "Did we successfully complete the task?", this copy allows us to align the outcomes of what we're trying to measure. These labels will be very useful once we start doing data analysis in sessions four and five.
-->

---

## Bad vs Good Feedback Design

### Bad Design: Subtle and Generic
```
[Answer displayed]

                    👍  👎
                 (tiny buttons, bottom right)
```

### Good Design: Prominent and Specific
```
[Answer displayed]

Did we answer your question today?
┌─────────────────┬─────────────────┐
│     👍 YES      │      👎 NO      │
│   (large btn)   │   (large btn)   │
└─────────────────┴─────────────────┘
```

**Result:** 5x more feedback with better design

<!-- 
Speaker Notes:

Simple changes like making buttons bigger and changing the copy can result in 5x more feedback. The positioning matters - where can users give feedback? Is it hidden? How long does it take to find the feedback buttons? These are all super important considerations.
-->

---

## The Power of Specific Copy

### Generic (Useless)
```
👍 Good    👎 Bad
```
**Problem:** "Bad" could mean slow, wrong, too long, confusing, etc.

### Specific (Actionable)  
```
Did we successfully complete your task?
┌─────────────────────────────────────┐
│            👍 YES, DONE             │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│         👎 NO, DIDN'T HELP          │
└─────────────────────────────────────┘
```

**Benefits:** 
- Clear success criteria alignment
- Actionable labels for data analysis
- Better correlation with business outcomes

<!-- 
Speaker Notes:

When you have generic feedback like "Good" or "Bad", the problem is that "Bad" could mean slow, wrong, too long, confusing, etc. But with specific copy that asks "Did we successfully complete your task?", we get much more actionable feedback that aligns with our success criteria and correlates better with business outcomes.
-->

---

## Follow-Up Questions for Rich Data

### When User Says "No"
```
Why wasn't your question answered?

□ Too slow
□ Called wrong functions  
□ Bad response format
□ Misinterpreted my request
□ Missing information
□ Other: ___________
```

**Impact:**
- Segment failure modes
- Identify specific improvement areas
- Create targeted evaluation datasets
- Debug system bottlenecks systematically

<!-- 
Speaker Notes:

When users select negative feedback, we can start asking follow-ups: "Why wasn't your question answered? Was it too slow? Did it call too many functions? Is the response format bad? Is it misinterpreting results?"

I've had so many clients not really understand what went wrong in their system and collect feedback that's very uncorrelated with any outcomes. Sometimes people think it's bad because it's slow, others because it's too long or too short. These are all different things we care about, and by having sub-questions, we can segment and understand failure modes much better.
-->

---

## Enterprise Feedback: The Slack Integration

### Consumer Pattern
- Small feedback buttons
- Passive collection
- Volume-based insights

### Enterprise Pattern
- **Direct Slack integration:** Negative feedback → Customer success channel
- **Human review:** Manual assessment of each failure
- **Eval integration:** Add examples to test suites
- **Customer loop:** Report back on improvements in meetings
- **Critical:** Let customers know their feedback will improve the product
- **Behavior:** Customers need to see feedback leads to action

**Result:** 5x more feedback + stronger customer relationships
- **Speed:** Fine-tune 5x faster with more data
- **Trust:** Build trust while collecting data and building evals

<!-- 
Speaker Notes:

What I mentioned works for a consumer setting with low-touch feedback buttons, but this also works in enterprise sales settings, especially with large customers and customer success teams.

A lot of this is behavioral - you really have to let the customer know that the negative feedback they give will improve the product. We think about Slack bot integrations and webhooks where negative feedback is posted directly into Slack for customer success review.

We take those examples, review them by hand, add them to our eval suite, then bring it up in bi-weekly or monthly meetings. We tell customers we've added their feedback to our evals and report back on improvements over time. This has been the biggest factor in collecting feedback while building trust, collecting data, and building evals.

In both cases - changing consumer copy and creating shared Slack groups - we saw about 5x more feedback for the same applications. This means we can fine-tune 5x faster and deploy knowing our models work 5x faster.
-->

---

## Mining Hard Negatives Through UX

**The Challenge:** Finding good negative examples for fine-tuning

### Traditional Approach
```
Anchor: "How to deploy?"
Positive: deployment_guide.md
Negative: ??? (random documents)
```

### UX-Driven Approach: Citation Deletion
```
[Generated Answer with Citations]
📄 deployment_guide.md    [×] Delete
📄 security_setup.md     [×] Delete  
📄 api_reference.md      [×] Delete

When user deletes → Hard negative example!
```

**Benefit:** User-validated irrelevant content = perfect training data

<!-- 
Speaker Notes:

This same feedback can be used to improve our re-rankers or embedding models. When people say we didn't answer the question and the data was irrelevant, we can go back and use a language model to relabel text chunks for relevance to find hard negatives.

The hardest part of fine-tuning triplets is finding hard negative examples. If you think about Facebook's "People You May Know" feature, every time you add somebody, that tells us they should have showed up higher. When you delete someone, that's collecting negative feedback.

You can imagine a UI where we answer questions and show referenced documents. If a user can delete one of these documents and regenerate an answer, that's another opportunity for hard negatives. This is the general secret of collecting high-quality data: positive examples, negative examples, and simple objectives - just like dating apps like Tinder and Hinge.
-->

---

## Facebook-Style Feedback Collection

### Infinite Scroll Pattern
```
People You May Know:
┌─────────────────┬─────────────────┐
│  User 1  [Add]  │  User 2  [Add]  │
└─────────────────┴─────────────────┘
┌─────────────────┬─────────────────┐
│  User 3  [Add]  │  User 4  [Add]  │  
└─────────────────┴─────────────────┘
                  ...
```

### Limited Options Pattern  
```
Top 5 Suggestions:
┌─────────────────────────────────────┐
│  User A  [Add]              [Skip]  │
│  User B  [Add]              [Skip]  │
│  User C  [Add]              [Skip]  │
└─────────────────────────────────────┘
```

**RAG Application:** Show top documents, let users add/remove = training data

<!-- 
Speaker Notes:

If you think about the Hinge or Tinders of the world, they train embedding models because they have tons of volume in interactions. The swiping mechanics give them positive examples (likes) and negative examples (dislikes), plus they have very simple objectives like whether something matches. That's the general secret of high-quality data collection.
-->

---

## The Dating App Secret

**Why Tinder/Hinge Have Great Models:**

1. **High Volume:** Millions of interactions daily
2. **Clear Positive/Negative:** Swipe right/left  
3. **Simple Objective:** Match prediction
4. **Continuous Feedback:** Every interaction is a label

**RAG Lesson:** Design interactions that naturally generate training labels

**Examples:**
- Citation deletion = negative examples
- Follow-up clicks = positive examples  
- Query refinement = preference learning

<!-- 
Speaker Notes:

There are numerous ways to collect positive and negative examples through natural user interactions. The key is designing your interface so that every user action provides valuable training data while improving their experience.
-->

---

## Citations: Trust + Training Data

### Why Citations Matter
- **User Trust:** "Where did this come from?"
- **Verification:** Users can check sources
- **Training Data:** Click patterns = relevance signals
- **Customer Questions:** "How does AI get this info?" "How do I know it's accurate?"
- **Beat them to the punch:** Include citations proactively
- **Preview functionality:** Show what data is being used

### Simple Citation Implementation
```python
class Response(BaseModel):
    content: str
    citations: List[Citation]

class Citation(BaseModel):
    text: str
    source_id: str
    title: str
```

### Advanced: Bounding Box Citations
```python
class BoundingBoxCitation(BaseModel):
    text: str
    pdf_path: str
    page_number: int
    bbox: List[float]  # [x1, y1, x2, y2]
```

**Recent Innovation:** Cite bounding boxes of parsed data
- **Beyond text chunks:** Cite actual PDF locations
- **Visual citations:** Show boxes over original document
- **High fidelity:** Reference specific tables, titles, sections
- **Better trust:** Users see exact source location

<!-- 
Speaker Notes:

Citations can go a long way, especially if your end users aren't familiar with AI. They're going to ask questions like: "Where do we get these answers from? How is the AI able to get this information? How do I know it's accurate?"

Most of these questions are about building trust and understanding what's happening behind the scenes. You can beat them to the punch by including citations they can interact with. Citations allow preview of what data is being used, and features like deleting citations and regenerating answers let us collect negative feedback.

What's been interesting in recent months is that we can now cite not just text chunks, but bounding boxes of parsed data. If we have answers about titles or tables, we can cite the actual box and visualize citations over the actual PDF, rather than just processed text. This allows high-fidelity answers with visual citations showing exact source locations.
-->

---

## Streaming: The Table Stakes Feature

**Reality Check:** Only 20% of companies implement streaming well

### Why Streaming Matters
- **User Expectation:** Instant response feeling
- **Perceived Performance:** 11% faster with animated progress (same wait time!)
- **Retention:** Users tolerate 8 seconds with visual feedback vs instant abandonment
- **Abandonment:** Reduces dropout rates significantly
- **Trust:** Applications with engaging loading screens report higher satisfaction
- **Real Examples:** Facebook's skeleton screens reduced perceived load times

### What to Stream
1. **Response Text:** Token by token
2. **Tool Calls:** Show function execution  
3. **Interstitials:** "Searching documents...", "Analyzing results..."
4. **UI Components:** Citations, follow-ups as they're ready

<!-- 
Speaker Notes:

Only about 20% of companies I work with have a good understanding of how to implement streaming to make the user experience better. My recommendation is to stream everything when possible.

You can stream interstitials to explain latency and help customers understand what's going on. You can stream different results and UI components so customers don't have to wait for the last token to complete. You can stream tool calls to show intermediate states.

Once you see skeleton screens - whether on Slack, Facebook, or LinkedIn - it's really hard to unsee them. They really help users improve their perception of latency. Streaming has become table stakes in LLM applications - users expect responses instantly, and streaming improves both performance and perceived performance.

For example, users perceive animated progress bars as 11% faster, even when wait times are the same. For most applications, users will only tolerate up to about 8 seconds of waiting given visual feedback, which reduces abandonment. Applications with engaging loading screens often report higher satisfaction scores.
-->

---

## Streaming Implementation Strategy

### The Migration Problem
> "Migrating from non-streaming to streaming is a pain in the ass"

**Recommendation:** Build streaming from day one
- **Reality:** Will take weeks out of your dev cycle to upgrade later
- **Streaming is table stakes:** Users expect it in LLM applications
- **Build it now:** Much easier than retrofitting later

<!-- 
Speaker Notes:

If you're on the fence about implementing streaming in products you're building today, I want to let you know that migrating from non-streaming to streaming application is a pain in the ass. I really recommend building it from the start - it's likely going to take weeks out of your dev cycle just to upgrade to streaming in the long run.
-->

### Technical Approach
```python
@app.route('/chat', methods=['POST'])
def chat_stream():
    def generate():
        # Stream interstitials
        yield f"data: {json.dumps({'type': 'status', 'message': 'Searching...'})}\n\n"
        
        # Stream tool calls
        for tool_result in execute_tools():
            yield f"data: {json.dumps({'type': 'tool', 'data': tool_result})}\n\n"
        
        # Stream response
        for token in llm_stream():
            yield f"data: {json.dumps({'type': 'token', 'data': token})}\n\n"
    
    return Response(generate(), mimetype='text/plain')
```

---

## Structured Streaming with Citations

### Traditional Response
```json
{
  "answer": "The deployment process involves three steps...",
  "done": true
}
```

### Structured Streaming Response
```python
class StreamingResponse(BaseModel):
    content: str = ""
    citations: List[Citation] = []
    follow_ups: List[str] = []
    status: str = "generating"

# Stream updates to each field
for update in llm_stream():
    response.content += update.token
    if update.citation:
        response.citations.append(update.citation)
    yield response.model_dump()
```

**Advanced Pattern:** Stream different UI components separately
- **Content:** Streams token by token
- **Citations:** Added as they're identified
- **Follow-ups:** Generated and streamed at the end
- **Status:** Updates throughout the process

**Result:** Users see progress on multiple fronts, better perceived performance

<!-- 
Speaker Notes:

With structured streaming, you can stream different UI components separately. Content streams token by token, citations are added as they're identified, follow-ups are generated and streamed at the end, and status updates throughout the process. Users see progress on multiple fronts, creating much better perceived performance.

If you use a library like Instructor, you can also stream out structured data. This allows us to have citations with IDs and titles, and responses that contain content, follow-up actions, and sources. Then you just build a React component that renders all of this as it streams in.
-->

---

## Slack Bot Feedback Patterns

### Basic Acknowledgment
```
User: "How do I deploy the app?"
Bot: 👀 (eyes reaction - received)
     
     [Processing...]
     
     ✅ (checkmark - completed)
     Response: "To deploy the app..."
```

### Pre-seeded Feedback
```
Bot Response: "To deploy the app, run..."

👍 👎 ⭐ (auto-added reactions)
```

**Impact:** Pre-seeded reactions dramatically increase feedback rates

**Key Insight:** If reactions aren't there, users won't think to give feedback
- **Behavioral psychology:** Prompt the action you want
- **"How did I do?"** + pre-seeded reactions = 5-10x more feedback
- **Simple implementation:** Auto-add emoji reactions to responses

**Data Collection:** Track reaction patterns for continuous improvement
- **Cache:** Save question-answer pairs as few-shot examples
- **Analytics:** Monitor which responses get what reactions

<!-- 
Speaker Notes:

For Slack bot integrations, you can react with eyes emoji to communicate that the user message has been received. It doesn't have to be complicated - just let the user know it's been received. Then mark with a checkmark emoji to label it as responded to.

But here's the key insight: you can prefill emojis with thumbs up, thumbs down, and star reactions to prompt users to give feedback. If these reactions weren't there, we might not think about giving feedback. But because we ask "How did I do?" and provide the reactions, we're giving users an opportunity to give feedback.

This dramatically improves the amount of feedback we get compared to having no react emojis at all. You can save these question-answer pairs as few-shot examples or cache them for the future.
-->

---

## Prompting the User, Not Just the AI

**Insight:** People are lazy and don't know what they want

### Bad Approach
```
[Empty text box]
"What would you like to know?"
```

### Good Approach  
```
Try asking:
• "How do I deploy to production?"
• "What are the security requirements?"
• "Show me the API documentation"
• "Help me troubleshoot connection issues"
```

**Benefits:**
- Shows capabilities users didn't know existed
- Reduces empty/vague queries
- Generates higher-quality training data
- **Key insight:** People are lazy and don't know what they want
- **Discovery:** Show features users wouldn't have thought about
- **Session 4 preview:** Discover these through conversation data analysis

<!-- 
Speaker Notes:

Not all prompting should be for the AI - we should also prompt the customer and prompt the user. Generally, people are pretty lazy and most people don't know what they want. By giving a couple of examples early on, we make life as easy as possible.

This is also a good way of using suggestions to show off capabilities your users wouldn't have thought about or didn't know was possible. For example, when Perplexity had social features, I didn't even know that was a thing.

In session four, we'll talk about how we can discover these through data analysis of existing conversations. Once you start looking for these interactions to help collect data, you'll see them everywhere.
-->

---

## Chain of Thought: The Hidden Performance Booster

**Reality:** Massively underutilized by most teams

### Performance Impact
- **10% improvement** in most tasks
- **Make or break** difference for production deployment
- **Loading interstitial** opportunity with streaming
- **Game changer:** With O1/R1 models, reasoning becomes visible
- **Multiple purposes:** Better reasoning + loading indicator

<!-- 
Speaker Notes:

Chain of thought is a massively missed opportunity for a lot of teams. With the advent of things like O1 and R1, we know this is a game changer for improving performance. Even without R1 or O1, implementing chain of thought has been one of the highest impact things we can do.

In many tasks we've seen, chain of thought produces a 10% bump in performance, and that bump can make the difference between something usable and something impossible to deploy in production.

By wrapping chain of thought in XML or streaming it with O1/R1, we can build dynamic UI that renders the chain of thought as separate data. Chain of thought can now also become a loading interstitial, serving multiple purposes.
-->

### Modern Implementation
```python
# With O1/R1 models
response = client.chat.completions.create(
    model="o1-preview",
    messages=[{"role": "user", "content": prompt}]
)

# Stream the reasoning
for chunk in response:
    if chunk.type == "reasoning":
        yield {"type": "thinking", "content": chunk.content}
    elif chunk.type == "response":  
        yield {"type": "answer", "content": chunk.content}
```

---

## Chain of Thought for Complex Tasks

### Use Case: SaaS Pricing Quotes
```
Context: 15-page pricing document + 1-hour transcript
Goal: Generate pricing proposal email

Chain of Thought Prompt:
1. "First, reiterate the key pricing variables from our document"
2. "Next, identify parts of transcript that mention pricing"  
3. "Then, find relevant sections of pricing document"
4. "Finally, reason through the appropriate pricing options"
```

### Results
- **90% acceptance rate** for generated quotes
- **Single prompt** replaces complex multi-agent system
- **Easy verification** with structured reasoning
- **Rich training data** from sales rep feedback

<!-- 
Speaker Notes:

Let me give a specific example of using monologues for SaaS pricing quotes. Imagine we have a 15-page pricing document on how salespeople should dictate prices, plus a one-hour transcript. The task is to prepare an email proposing the pricing model.

Before long context, we might have needed RAG. But what we found more effective is to cache-prompt the pricing data and inject the transcript. Instead of using agents, we specifically prompt the chain of thought to:

1. First, reiterate the variables that define quotes
2. Then, reiterate parts of the transcript mentioning quotes  
3. Finally, reiterate relevant parts of the pricing document

With a single prompt, we get pricing questions answered without complex multi-stage agents. This produces citations that are easy to verify, and we were able to get 90% of follow-up emails accepted without edits.
-->

---

## The Long Context + Chain of Thought Pattern

### Traditional RAG Approach
```
Query → Retrieve chunks → Stuff context → Generate
```

### Long Context + CoT Approach  
```python
system_prompt = f"""
Context: {full_pricing_document}

For each query:
1. Reiterate relevant pricing variables
2. Extract pricing mentions from transcript  
3. Reference applicable document sections
4. Reason through recommendation
"""

user_prompt = f"""
Transcript: {full_transcript}
Generate pricing proposal email.
"""
```

**Benefits:** Better reasoning, verifiable citations, simpler architecture

<!-- 
Speaker Notes:

For complex tasks, when dealing with very long contexts, the language model may struggle with recall or fully processing instructions. Having chain of thought reiterate those instructions and recall relevant examples before answering allows the LM to re-read the prompt, improve reasoning, and get much better results.

Generating monologues can also dramatically improve tonality and quality, which can be fine-tuned later to be done without monologues. We can use chain of thought to create better answers and then distill that into a smaller model.
-->

---

## Validation: The Hidden Quality Multiplier

**The Problem:** Single-step generation isn't enough for high-quality answers

### Validation Pattern
```python
class EmailResponse(BaseModel):
    subject: str
    body: str
    
    @validator('body')
    def validate_urls(cls, v):
        urls = extract_urls(v)
        for url in urls:
            if not is_allowed_domain(url):
                raise ValueError(f"Invalid URL domain: {url}")
            if not url_exists(url):  # GET request check
                raise ValueError(f"URL not found: {url}")
        return v
```

### Real Results
- **Before validation:** 4% failure rate (invalid URLs)
- **After validation:** 0% failure rate with retry loop
- **After fine-tuning:** Validators never triggered again
- **Implementation time:** 3 days to build

**Key Insight:** Validators become evals in production, improving both user experience and model training

<!-- 
Speaker Notes:

Often a single step isn't enough for high-quality answers. I like having a validation pattern before going into multi-stage agent behavior. As language models get more complex, we'll be able to do more within a single prompt.

In latency-insensitive applications, having validators on your prompt outputs can really increase user trust and satisfaction. These effectively become evals and tests within production workflows.

Here's a specific example that mattered for our use case: we wanted our language model to draft emails with references to case studies and marketing material, but we had to ensure no hallucinated URLs. We built a simple validator using regex to verify URLs existed in allowed domains.

For critical applications, we even made small GET requests to verify 200 status. Initially we had a 4% failure rate - 4% of emails had invalid URLs. After one retry, it got to 0%. After fine-tuning the 4.0 model into 4.0 mini, validators never triggered again - we got zero hallucination rate in a single pass. This took about 3 days to build and gave us a much faster application without retry loops.
-->

---

## UI Components That Collect Data

### Follow-Up Questions
```
[Generated Response]

Continue with:
• "Tell me more about deployment"
• "What about security considerations?"  
• "Show me code examples"
```
**Data:** Track click patterns → improve suggestions

### Source Interaction
```
[Response with hoverable citations]
📄 deployment.md ← Click to preview
📄 security.md   ← Click to preview
```
**Data:** Preview clicks = relevance signals

### Share/Save Buttons
```
[Response] 
├── 📋 Copy   ← Usage signal
├── ⭐ Save   ← High quality signal  
└── 🔗 Share  ← Validation signal
```

---

## Data Collection Everywhere

**Once you start looking, you'll see feedback opportunities everywhere:**

### Perplexity Patterns
- Related questions
- Source hover interactions
- Follow-up suggestions
- Share/copy behaviors

### ChatGPT Patterns  
- Regeneration requests
- Edit suggestions
- Conversation ratings
- Feature usage tracking

**Exercise:** Audit your favorite AI tools for data collection patterns

### The Universal Truth
**Once you start looking for feedback collection, you'll see it everywhere:**
- Perplexity: Related questions, source hovers, follow-up suggestions
- ChatGPT: Regeneration, edit suggestions, conversation ratings
- Every tool: Multiple touchpoints for data collection

**Your mission:** Identify 5 feedback opportunities in your current application

<!-- 
Speaker Notes:

Once you start looking for feedback collection, you'll see it everywhere. Perplexity has related questions, source hover interactions, follow-up suggestions, and share/copy behaviors. ChatGPT has regeneration requests, edit suggestions, conversation ratings, and feature usage tracking.

Every AI tool has multiple touchpoints for data collection. Your mission is to identify 5 feedback opportunities in your current application. As you try different AI tools, pay attention to how they collect feedback, render citations, and continue the user experience with follow-up actions.
-->

---

## This Week's Implementation Checklist

### Immediate (Day 1)
1. **Redesign feedback buttons:** Make them large and specific
2. **Add follow-up questions:** When users give negative feedback  
3. **Implement basic streaming:** At minimum, token-by-token response

### Short-term (This Week)
1. **Add citations:** Basic markdown links to sources
2. **Create suggestion prompts:** Show example queries
3. **Set up feedback logging:** Store all user interactions

<!-- 
Speaker Notes:

This concludes the first half of the systematically improving RAG course. We've covered how synthetic data can be supplemented with user data, and in this session, we've focused on using different UX to make the user experience better while building systems that collect feedback over time.

Whether it's deleting citations to regenerate answers, changing copy so customers understand what they're labeling, or adding validators that check if answers are correct - all of these approaches help us collect better data while improving user experience.
-->

### Medium-term (Next Month)
1. **Slack/webhook integration:** Route feedback to team channels
2. **Citation deletion UI:** Let users remove irrelevant sources  
3. **Chain of Thought streaming:** Show reasoning process

---

## Next Week Preview: Data Analysis

**Session 4 Focus:**
- Analyze all the feedback you've collected
- Segment users and queries to find patterns
- Identify high-impact improvement opportunities  
- Build data-driven product roadmaps

**Connection:** This week's UX improvements become next week's analysis dataset

<!-- 
Speaker Notes:

Next week in Session 4, we'll focus on analyzing all the feedback you've collected, segmenting users and queries to find patterns, identifying high-impact improvement opportunities, and building data-driven product roadmaps. This week's UX improvements become next week's analysis dataset.
-->

---

## Key Takeaways

### Design Insights
1. **Small changes, big impact** - 5-10x feedback improvement possible
2. **Specific > Generic** - "Did we complete your task?" vs "Good/Bad"
3. **Streaming is table stakes** - Build it from day one
4. **Every interaction is data** - Design for continuous learning

### Technical Insights  
1. **Chain of Thought works** - 10% performance improvement
2. **Citations build trust** - And provide training signals
3. **Structured streaming** - Better UX + richer data collection
4. **Long context + CoT** - Often beats complex RAG systems

### Strategic Insights
1. **Feedback design = competitive advantage** - Most teams do this poorly
2. **User prompting matters** - Show capabilities proactively  
3. **Enterprise needs human touch** - Slack integrations build relationships
4. **Data compounds** - Today's UX decisions become tomorrow's models

---

## Remember: Every User Interaction is an Opportunity

**The Flywheel:**
- Better UX → More feedback → Better training data → Better models → Better UX

**Your Goal:** Turn every user session into multiple training examples

**Success Metric:** 5-10x increase in useful feedback volume within 2 weeks

**Reality Check:** Most teams collect terrible feedback because:
- Buttons are too small and hidden
- Copy is vague ("good/bad" tells you nothing)
- No follow-up questions to understand failures
- Users don't know their feedback matters

**The Fix:** Small design changes = massive data improvements

<!-- 
Speaker Notes:

The questions I want you to ask yourself in this session are:

1. Are you being too subtle with feedback collection? Should we change the copy? Make buttons bigger? How can we communicate that customer feedback is very important?

2. Am I building citations in a way that gains user trust and improves satisfaction? Can I use citations UX to collect more relevant data?

3. Could I implement streaming better with loading interstitials and follow-up actions to make applications feel faster? Can I better promote capabilities and reject work my language model can't do?

4. Can I iterate on producing monologues and chain of thought to reiterate parts of my data and context to improve reasoning in my system?

Remember: The flywheel is Better UX → More feedback → Better training data → Better models → Better UX. Your goal is to turn every user session into multiple training examples, with a success metric of 5-10x increase in useful feedback volume within 2 weeks.
-->

---

## Thank You

**Questions for office hours:**
- How to implement streaming in your tech stack?
- Best feedback patterns for your specific use case?
- Chain of Thought prompting strategies?
- Citation implementation approaches?

**Next week:** Analyzing all that beautiful data you'll collect

*maven.com/applied-llms/rag-playbook*
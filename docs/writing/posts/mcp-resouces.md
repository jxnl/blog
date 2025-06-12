---
draft: false
date: 2025-01-01
authors:
  - jxnl
categories:
  - AI
  - Engineering
  - MCP
comments: true
---

# Prompt Template Resource System Specification

## Overview

A token-efficient system for referencing external resources in LLM prompts without including their full content, designed to optimize token usage when LLMs generate template calls.

<!-- more -->

## Template Definition Syntax

```python
@template
def template_name(param1, param2, ...):
    # I recognize that these should really be chat messages
    return Template("""
    Template content with placeholders:

    <param1>
    {{param1}}
    </param1>

    <param2>
    {{param2}}
    </param2>
    """)
```

## Resource Reference Types

| Type          | Syntax                        | Description                                            |
| ------------- | ----------------------------- | ------------------------------------------------------ |
| File          | `file://path/to/resource.txt` | Load content from file system                          |
| String        | `"Direct content"`            | Use literal string value                               |
| Tagged Output | `context://<tag_type>#<id>`   | Reference session-based generated content with any tag |
| Image         | `image://path/to/image.jpg`   | Reference image resource                               |
| Audio         | `audio://path/to/audio.mp3`   | Reference audio resource                               |
| Video         | `video://path/to/video.mp4`   | Reference video resource                               |

## Template Usage

```python
# Basic usage with mixed resource types
response = template_name(
    param1="file://path/to/resource.txt",
    param2="This is direct string content"
)

# Using various tagged output references
response = template_name(
    param1="context://artifact#summary-12345",
    param2="context://thought#reasoning-67890",
    param3="context://candidate-profile"
)
```

## Tagged Outputs & Memory Management

### XML Tag Creation and Reference

Any XML tag can be used to create referenceable content. Examples:

```xml
<artifact id="summary-123">
Professional developer with 10 years experience...
</artifact>

<thought id="reasoning-456">
This candidate has strong technical skills but limited management experience.
</thought>

<response id="feedback-789">
Your solution correctly implements the algorithm but could be optimized further.
</response>
```

Reference in subsequent calls:

```python
create_notion_page(title=str, body="context://artifact#summary-123")
follow_up_question(reasoning="context://thought#reasoning-456")
email_template(feedback="context://response#feedback-789")
```

### Error Handling

| Error               | Behavior                           |
| ------------------- | ---------------------------------- |
| Missing file        | Return error with path information |
| Invalid resource ID | Return error with invalid ID       |
| Permission issues   | Return security constraint error   |
| Malformed template  | Return syntax error with details   |

## Comments

Generally, I think here that if we can just save XML tagged data as resources and get names back out, that we can pass them around as context in a way that's more productive.

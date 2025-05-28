---
authors:
  - jxnl
categories:
  - Software Engineering
comments: true
date: 2022-08-01
description: Discover how the Flight framework enhances recommendation systems at
  Stitch Fix, streamlining data pipelines and improving performance.
draft: false
slug: stitchfix-framework
tags:
  - recommendation system
  - data pipelines
  - Stitch Fix
  - Flight framework
  - real-time systems
---

# Recommendations with Flight at Stitch Fix

As a data scientist at Stitch Fix, I faced the challenge of adapting recommendation code for real-time systems. With the absence of standardization and proper performance testing, tracing, and logging, building reliable systems was a struggle.

To tackle these problems, I created Flight – a framework that acts as a semantic bridge and integrates multiple systems within Stitch Fix. It provides modular operator classes for data scientists to develop, and offers three levels of user experience.

<!-- more -->

- The **pipeline layer** allows business-knowledge users to define pipelines in plain English.
- The **operator layer** enables data scientists to add and share many filters and transformations with ease.
- The **meta layer** provides platform engineers the ability to introduce new features without affecting the development experience of data scientists.

Flight improves the "bus factor" and reduces cognitive load for new developers, standardizes logging and debugging tools, and includes advanced distributed tracing for performance measurement and metrics monitoring.

## Pipeline Layer

The `Pipeline` class is the foundation of the Flight framework, enabling users with business domain knowledge to craft pipelines composed of a variety of modular operators. The resulting code is readable and almost resembles plain English. The code sample below showcases how the `Pipeline` class can be used to set inclusion and exclusion criteria and scoring functions for a given item type.

```python
from flight.pipelines import Pipeline
import flight.sourcing as so
import flight.scoring as sc
import flight.operators as fo

@app.post("/recs/complimentary_items")
async def complimentary_items(client_id: int, product_id: int):
    pipeline = Pipeline("complimentary_items").initialize(
        includes=[so.AvailableInventory(), so.MatchClientSize()],
        excludes=[so.PreviouslyPurchased()],
        scores=[sc.ProbabilityOfSale("psale_score")],
        item_type="sku_id",
    )

    pipeline = (pipeline
                | fo.Hydrate(["department", "product_id"])
                | fo.MatchDepartment(product_id)
                | fo.DiverseSample(n=10, maximize="psale_score")
                | fo.Sort("score", desc=True))

    # Pipelines are lazy, so execution only happens upon calling execute()
    resp = await pipeline.execute(
        client_id, return_cols=["sku_id", "product_id", "score"], **kwargs
    )
    return resp
```

In the shopping example, we start by performing the set operation `Union(includes) - Union(excludes)` and then calculate scores for the results. It's worth taking a look at the code to get a better understanding of how it works on first glance. The pipeline class manages the whole process, allowing us to have control over how best to compute.

## Operator Layer

Operators in the framework are implemented as classes, with static variables defined using the **`dataclass`** style, and dynamic variables passed in during runtime. For example, **`SourceOperators`** such as the **`Inventory`** operator rely on external APIs to retrieve data, while **`IndexOperators`** like **`MatchDepartment`** merely return indices, providing an efficient way to manage pipelines without mutating dataframes.

```python
class AvailableInventory(fo.SourceOperator):
   async def __call__(self, **kwargs) -> fo.Source:
       data = await get_inventory(**kwargs)
       return fo.Source(data)

class MatchDepartment(fo.FilterOperator)
    product_id: int
    department: str

   def __call__(self, df, **kwargs) -> pd.Index:
      assert "department" in df.columns
      department = get_product(self.product_id, "department")
      self.department = department
      return df[df.department == department].index
```

## Meta Layer

In the pipeline layer, you only have to worry about the shape of the pipeline, not pandas code required. In the operator you only need to make sure your pandas or etc code fits the shape of the signature. Return a `fo.Source` or a `pd.Index` and all data merging, filter, augmentation happens behinds the scenes.

So what actually happens?

### **Error handling:**

Pipeline handles errors on `execute`, providing info on what went wrong. Since errors only occur in `__call__` method of operator, making it easy to write tests to catch errors and identify the operator causing the issue. This especially useful when we don't know why no recommendations were generated.

```python
# not an error, just due to the pipeline
resp = {
   product_id=[],
   error=False,
   reason="MatchDepartment(product_id=3) pipeline returned 0 items after filtering 53 items"
}
# actual error, since not having inventory is likely a systems issue and not an
resp = {
   product_id=[],
   error=True,
   reason="Inventory(warehouse_id=1) timed out after retres"
}
```

### **Logging**

Operators are logged at various levels of detail. When `initialize` is called, we log each class that was called, the number of results produced, and information on how data was intersected and combined. Each log is structured with the `dataclass`level information of each operato

```python
> Inventory(warehouse="any") returned 5002 products in 430ms
> MatchSize("S") returned 1231 products in 12ms
> After initalization, 500 products remain
> MatchDepartment(product_id=3) filtered 500 items to 51 items in 31ms
> Diversity(n=10) filtered 51 items to 10 items in 50ms
> Returning 10 items with mean(score)=0.8
```

By injesting this data into something like Datadog we can add monitors on our operators, the results, the distribution of results.

### **Distributed Tracing**

With integration of OpenTelemetry's tracing logic, Flight allows for comprehensive tracing of each operator, providing visibility into performance issues from end to end. This is particularly useful for source operators.

### **Dynamic Execution**

The entire pipeline object is around passing around classes with `dataclass`style initialization. This simple fact that all arguments tend to be primitives allows us to create pipelines dynamically, either through config or requests, you could imagine a situation where it might be useful to define pipelines by config like JSON or YAML and have an engine serve many many pipelines dynamically

```python
# config.yaml
pipeline:
  name: "MyPipeline"
  item_type: "sku_id"
  initialization:
    includes:
    - name: AvailableInventory
    scorer:
    - name: ClickRate

  operations:
  - name: Sort
    parameters:
      score: "click_rate"
      desc: True

# run.py
@app.post("/execute_config")
async def execute(config, kwargs):
   pipeline = Pipeline.from_config(config)
   return await pipeline.execute(**kwargs)

@app.post("/execute_name")
async def execute_from_config(name, kwargs)
   config = get_config(name)
   return await execute(config, kwargs)

```

### **Debugging**

Debugging data quality issues or identifying the reasons behind clients not being able to see inventory can be a challenge. Flight's verbose mode allows for detailed debugging by listing products and viewing the index at each step of the pipeline's iteration. This standardized debug output enables the creation of UI tools to explore results, compare operators, and analyze pipelines.

```python
# with verbose = debug = true
resp = {
   "product_id": [1, 2, 3],
   "debug": {
       "includes": [
           {"name": "Inventory", "kwargs": {}, "product_ids": [1, 2, 3, ...]}
       ],
       "excludes": [],
       "pipeline_operators": [
           {
               "name": "Match",
               "kwargs": {...},
               "input_ids": [1, 2, 3, ...],
               "n_input": 100,
               "output_ids": [1, 2, 3, ...],
               "n_output": 400
           }
       ]...
   }
}
```

The capabilities provided by the glue of the meta layer allowed us to systematically inspect pipelines and operators, identify bottlenecks in our micro services, and directly communicate with other teams to improve performance and latency.

## Conclusion

In summary, Flight has significantly improved data pipeline management at Stitch Fix. Its architecture, which utilizes the source and index operator pattern, has streamlined code development and enhanced performance issue detection. The integration of OpenTelemetry's monitoring capabilities has also been critical for efficient pipeline execution and debugging.

As the usage of pipelines and operators grows, exploring more scalable management solutions may become necessary. However, the current architecture has effectively met our business needs by focusing on the development of efficient solutions. The experience with Flight highlights our commitment to improving data pipeline management, setting a standard for operational efficiency.

---
draft: False
date: 2024-06-01
categories:
  - RAG
  - Synthethic Data
  - LLM
authors:
  - ivanleomk
  - jxnl
---

## Coldstarting Rag Evaluations

Without a method to evaluate the quality of your RAG application, we might as well be leaving its performance to pure chance. In this article, we'll walk you through a simple example to demonstrate how easy it is to get started.

We'll start by using Instructor to generate synthethic data. We'll then chunk and embed some Paul Graham Essays using `lancedb`. Next, we'll showcase two useful metrics that we can use to track the performance of our retrieval before concluding with some interesting improvements to iteratively generate harder evaluation datasets. 

Most importantly, the code used in this article is avaliable inside the `/code/synthethic-evals` folder. We've also included some Paul Graham essays in the same folder for easy use.


Let's start by first installing the necessary libraries

```bash
pip install instructor openai scikit-learn rich lancedb tqdm
```

## Generating Evaluation Data


??? note "Set your OPENAI_API_KEY"

    Before proceeding with the rest of this tutorial, make sure to set your `OPENAI_API_KEY` inside your shell. You can do so using the command

    ```bash
    >> export OPENAI_API_KEY=<api key>
    ```


Given a text-chunk, we can use Instructor to generate a corresponding question using the content of the question. This means that when we make a query using that question, our text chunk is ideally going to be the first source returned by our retrieval algorithm.

We can represent this desired result using a simple `pydantic` BaseModel.

### Defining a Data Model

```python
class QuestionAnswerPair(BaseModel):
    """
    This model represents a pair of a question generated from a text chunk, its corresponding answer,
    and the chain of thought leading to the answer. The chain of thought provides insight into how the answer
    was derived from the question.
    """

    chain_of_thought: str = Field(
        ..., description="The reasoning process leading to the answer.", exclude=True
    )
    question: str = Field(
        ..., description="The generated question from the text chunk."
    )
    answer: str = Field(..., description="The answer to the generated question.")
```

<!-- more -->

??? info "Excluding Fields"

    When defining a Pydantic Base model, we can specify specific fields to be excluded when we convert our model to a json object. 

    ```python
    >> data = QuestionAnswerPair(chain_of_thought="This is fake", question="Fake question", answer="Fake Answer")
    >> print(data.model_dump_json(indent=2))
        {
            "question": "Fake question",
            "answer": "Fake Answer"
        }
    ```

    This is useful when we have intermediate values/states that we might want to avoid including within the serialized json such as a chain of thought reasoning.

Now that we have a defined data model, we can use `Instructor` to take in a desired text chunk and return a question that is specifically tailored to that text chunk.

```python
from pydantic import BaseModel, Field
import instructor
from openai import AsyncOpenAI
from asyncio import run
from typing import List
from rich import table
from tqdm.asyncio import tqdm_asyncio as asyncio

client = instructor.from_openai(mode=instructor.Mode.TOOLS)


class QuestionAnswerPair(BaseModel):
    """
    This model represents a pair of a question generated from a text chunk, its corresponding answer,
    and the chain of thought leading to the answer. The chain of thought provides insight into how the answer
    was derived from the question.
    """

    chain_of_thought: str = Field(
        ..., description="The reasoning process leading to the answer.", exclude=True
    )
    question: str = Field(
        ..., description="The generated question from the text chunk."
    )
    answer: str = Field(..., description="The answer to the generated question.")


async def generate_question_answer_pair(chunk: str):
    return await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a world class algorithm that excels at generating great questions that can be only answered by a specific text that will soon be passed to you. ",
            },
            {
                "role": "assistant",
                "content": f"Generate a question and answer pair that uses information and content that is specific to the following text chunk, including a chain of thought:\n\n{chunk}",
            },
        ],
        response_model=QuestionAnswerPair,
    )
```

Note here that we're generating our questions using `async` functions. These allow our calls to OpenAI to be made in parallel so that we don't have to wait for them to be made sequentially and speeds up our execution time significantly. 

<!-- more -->

??? info "Using Async Functions"
    To learn more about using `asyncio` with Instructor, checkout our guide to Batch Processing [here](https://jxnl.github.io/instructor/blog/2023/11/13/learn-async/) where we show examples demonstrating when to use each method and more.

We can see the results of our function by running it using the code snippet below

```python
chunk = "The companies at the Google end of the continuum are called startups\
        when they're young. The reason I know about them is that my wife Jessica\
        and I started something called Y Combinator that is basically a startup\
        factory. Since 2005, Y Combinator has funded over 4000 startups.\
        So we know exactly what you need to start a startup, because we\
        've helped people do it for the last 19 years."

result = run(generate_question_answer_pair(chunk))
print(result.model_dump_json(indent=2))
```

which in turn produces the output of

```json
{
  "question": "What is the name of the startup factory founded by the speaker and their wife in 2005?",
  "answer": "Y Combinator"
}
```

### Running our Function

Now that we've defined a data model and function to extract questions from a chunk, we can use a simple wrapper function to generate multiple questions from each of our source chunks in parallel. We can do so using the snippet below.

```python
from typing import List
from tqdm.asyncio import tqdm_asyncio as asyncio

async def generate_questions(chunks: List[str]):
    coros = [generate_question_answer_pair(chunk) for chunk in chunks]
    return await asyncio.gather(*coros)
```

??? info "Why use Tqdm for async?"
    In this case, we've chosen to use `tqdm`'s asyncio module instead of the native `asyncio` module because of two main reasons 

    1. `tqdm` offers an easy way to monitor the result of our question generation with it's native progress bar
    2. By importing it in as `asyncio`, we can easily swap it out down the line for the original asyncio library if our needs change

    If you want to extend this to a larger batch, consider using the `tenacity` library. With a simple `@retry` decorator, it provides useful features such as exponential backoff, error handling and maximum retries. `

Let's see how our function scales out to more chunks. We'll be using the `rich` library to format the generated output.

```python
from asyncio import run

chunks = [
    "The companies at the Google end of the continuum are called startups when they're young. The reason I know about them is that my wife Jessica and I started something called Y Combinator that is basically a startup factory. Since 2005, Y Combinator has funded over 4000 startups. So we know exactly what you need to start a startup, because we've helped people do it for the last 19 years.",
    "All you can know when you start working on a startup is that it seems worth pursuing. You can't know whether it will turn into a company worth billions or one that goes out of business. So when I say I'm going to tell you how to start Google, I mean I'm going to tell you how to get to the point where you can start a company that has as much chance of being Google as Google had of being Google.",
    "Those of you who are taking computer science classes in school may at this point be thinking, ok, we've got this sorted. We're already being taught all about programming. But sorry, this is not enough. You have to be working on your own projects, not just learning stuff in classes. You can do well in computer science classes without ever really learning to program. In fact you can graduate with a degree in computer science from a top university and still not be any good at programming. That's why tech companies all make you take a coding test before they'll hire you, regardless of where you went to university or how well you did there. They know grades and exam results prove nothing.",
]

questions: List[QuestionAnswerPair] = run(generate_questions(chunks))
```
This in turn gives us the following questions when we generate them in parallel.

| Question | Original Source |
| --- | --- |
| What is the name of the startup factory mentioned in the text that has funded over 4000 startups since 2005? | The companies at the Google end of the continuum are called startups when they're young. The reason I know about them is that my wife Jessica and I started something called Y Combinator that is basically a startup factory. Since 2005, Y Combinator has funded over 4000 startups. So we know exactly what you need to start a startup, because we've helped people do it for the last 19 years. |
| What does the text suggest about starting a startup and the uncertainty of its success? | All you can know when you start working on a startup is that it seems worth pursuing. You can't know whether it will turn into a company worth billions or one that goes out of business. So when I say I'm going to tell you how to start Google, I mean I'm going to tell you how to get to the point where you can start a company that has as much chance of being Google as Google had of being Google. |
| Why do tech companies make candidates take a coding test before hiring them? | Those of you who are taking computer science classes in school may at this point be thinking, ok, we've got this sorted. We're already being taught all about programming. But sorry, this is not enough. You have to be working on your own projects, not just learning stuff in classes. You can do well in computer science classes without ever really learning to program. In fact you can graduate with a degree in computer science from a top university and still not be any good at programming. That's why tech companies all make you take a coding test before they'll hire you, regardless of where you went to university or how well you did there. They know grades and exam results prove nothing. |

We can see that for each individual chunk of text that we have, we now have a well formatted question that is directly targetted at the content of the text itself. 

## Scaling Our Chunking

Now that we've written a simple function to generate questions from chunks, let's generate some text chunks from some Paul Graham essays. We've included 5 essays inside the `data` folder alongside our code at `/examples/synthethic-evals`. A good fit for this is the `lancedb` library which natively supports Pydantic.

This gives us a Vector Database which we can define entirely using `Pydantic` base models that also handles the batching for us out of the box nicely.

### Data Models

We need a simple data model to represent a chunk of text - this is simply an excerpt from one of the essays that we've provided.

```python
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector

openai = get_registry().get("openai").create(name="text-embedding-3-large", dim=256)

class TextChunk(LanceModel):
    chunk_id: str
    text: str = openai.SourceField()
    vector: Vector(openai.ndims()) = openai.VectorField(default=None)
```

Note here that a `LanceModel` is a `LanceDB` specific class which is based off a simple Pydantic `BaseModel`. It just adds some `LanceDB` specific functionality so that it works with the library. We've also defined a new field called `vector` which will automatically create an embedding vector using the OpenAI `text-embedding-3-large` model for us when we do the insertions.

Creating a new `LanceDB` vector database is simple - all we do is to use the `connect` method provided by the library and `lancedb` handles the rest.

```python
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from lancedb import connect

openai = get_registry().get("openai").create(name="text-embedding-3-large", dim=256)


class TextChunk(LanceModel):
    chunk_id: str
    text: str = openai.SourceField()
    vector: Vector(openai.ndims()) = openai.VectorField(default=None)
```

This creates a new folder for us at the path `./db` which will store all of our folder metadata and data when we run the code snippet below

```python
db_path = "./db"
table_name = "pg"
db = connect(db_path)
db_table = db.open_table(table_name)
```

We chunk the data in a general way by splitting on newlines and then inserting into our lancedb database.

??? info "Chunking Our Data"

    Now that we have created a new `lancedb` database locally, we need to do two things

    1. Read in the text data from the individual `.md` files containing the essays
    2. Split the text data by `\n`, generate an embedding for each and a corresponding hash using the `hashlib` library
    3. Split the chunks into batches and insert it into our lancedb in batches

    We can perform the first part by writing two simple iterators - one that returns a list of all the `.md` files in a directory and another that generates chunks from these files. This is relatively simple in python.

    ```python
    from lancedb.embeddings import get_registry
    from lancedb.pydantic import LanceModel, Vector
    from lancedb import connect
    from typing import Iterable, List
    from pathlib import Path
    import hashlib
    from tqdm import tqdm

    def read_files(path: str) -> Iterable[str]:
        path_obj = Path(path)
        for file in path_obj.rglob(f"*.md"):
            yield file


    def generate_chunks(docs: Iterable[List[Path]]):
        for doc in docs:
            with open(doc, "r", encoding="utf-8") as file:
                content = file.read()
                for chunk in content.split("\n"):
                    if not chunk:
                        continue
                    yield TextChunk(
                        text=chunk, 
                        chunk_id=hashlib
                                .md5(chunk.encode("utf-8"))
                                .hexdigest()
                    )
    ```

    We can then batch each of these individual group of text chunks by using another iterator as 

    ```python
    def batch_items(chunks: List[TextChunk], batch_size: int = 20):
        batch = []
        for chunk in chunks:
            batch.append(chunk)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch
    ```

    Finally, we can combine all of these together into a simple function as seen below.

    ```python
    db_path = "./db"
    table_name = "pg"
    data_path = "./data"

    db = connect(db_path)
    db_table = db.create_table(table_name, exist_ok=True, schema=TextChunk)

    files = read_files(data_path)
    chunks = generate_chunks(files)

    batched_chunks = batch_items(chunks, batch_size=50)

    for batch in tqdm(batched_chunks):
        db_table.add(batch)
    ```

    What's really neat about this entire setup is that `lancedb` is handling the automatic batching of embedding calls and iterators for us. We don't need to manually generate the embeddings and then create new objects with these embeddings.

### Retrieving Data

For simplicity sake, we'll be using semantic search to select the most relevant chunks of data. This is pretty easy with lancedb, as long as we provide a path to our db, a table name, we can query our database table using the following function below

```python
import openai
from lancedb import connect
from ingest import TextChunk
from rich.console import Console
from rich.table import Table
from rich import box
from typing import List

def get_response(db_path: str, table_name: str, query: str) -> List[TextChunk]:
    db = connect(db_path)
    db_table = db.open_table(table_name)

    client = openai.OpenAI()
    query_vector = (
        client.embeddings.create(
            input=query, 
            model="text-embedding-3-large", 
            dimensions=256
        )
        .data[0]
        .embedding
    )

    return db_table.search(query_vector).limit(5).to_pydantic(TextChunk)
```

We can then run this using a few lines as seen below which in turn gives the results in the table below

```python
query = "What's the best way to be succesful?"
db = "./db"
table = "pg"

response = get_response(db, table, query)
```



| Chunk Id | Content | 
| -- | -- |
| c6e3dba2cc1f38b704ec6437eec9fb23 | And there is of course one other thing you need: to be lucky. Luck is always a factor, but it's even more of a factor when you're working on your own rather than as part of an organization. And though there are some valid aphorisms about luck being where preparedness meets opportunity and so on, there's also a component of true chance that you can't do anything about. The solution is to take multiple shots. Which is another reason to start taking risks early.  |
| 44b1f682be6d29b399b2947a426137e8 | What should you do if you're young and ambitious but don't know what to work on? What you should not do is drift along passively, assuming the problem will solve itself. You need to take action. But there is no systematic procedure you can follow. When you read biographies of people who've done great work, it's remarkable how much luck is involved. They discover what to work on as a result of a chance meeting, or by reading a book they happen to pick up. So you need to make yourself a big target for luck, and the way to do that is to be curious. Try lots of things, meet lots of people, read lots of books, ask lots of questions. |
| 5ff0ae69052dccc9af9cb6a211dfe127 | The first step is to decide what to work on. The work you choose needs to have three qualities: it has to be something you have a natural aptitude for, that you have a deep interest in, and that offers scope to do great work. |
| bf23afd092d5c6d8179c72d2ab7f1d46 | The factors in doing great work are factors in the literal, mathematical sense, and they are: ability, interest, effort, and luck. Luck by definition you can't do anything about, so we can ignore that. And we can assume effort, if you do in fact want to do great work. So the problem boils down to ability and interest. Can you find a kind of work where your ability and interest will combine to yield an explosion of new ideas? |
| 87aa6353fe45ce7dae2b7d6e42d66733 | Fortunately there's a kind of economy of scale here. Though it might seem like you'd be taking on a heavy burden by trying to be the best, in practice you often end up net ahead. It's exciting, and also strangely liberating. It simplifies things. In some ways it's easier to try to be the best than to try merely to be good. |


And with that, we've figured out how to implement retrieval

## Evaluations

There are two useful evaluations which we can use when evaluating the quality of retrievals - NDCG and MRR. Intuitively, since we used a single chunk to generate a question, we want to measure how often it appears as the top result and its overall ranking when we fetch `k` different chunks.

Eventually, as we utilise more complex methods to generate our questions - either by combining multiple chunks or writing more complex queries, our approach will change. But for now, these two metrics are great for quickly determining how good our retrieval is performing.

??? info "Evaluations"
    
    For a more complex and in-depth look into different metrics, consider looking at [this article written by Jason on evaluating Machine Learning Systems](https://jxnl.github.io/blog/writing/2024/02/05/when-to-lgtm-at-k/#mean-reciprocal-rank-mrr-k)

Thankfully, we have a native implementation of NDCG in sklearn and MRR is relatively simple to implement. Let's see how we can calculate these metrics

### Metrics

#### NDCG

NDCG refers to Normalized Discounted Cumulative Gain. The higher the NDCG value, the more often we have relevant results being ranked higher in our list of retrieved elements.

There are two key portions here that we care about

- Discounted: Relevant Results are penalized the lower their ranking by assigning a weightage to each value ( in this case it is $1/log(2i)$ where $i$ is the position of the relevant item)
- Normalized : Without Normalization, we can get a higher score even if our relevant items rankings do not change ( due to the cumulative nature of DCG ). By normalizing the DCG scores, we can therefore obtain a more accurate score.

We can calculate the NDCG using the `sklearn` implementation as seen below. 

```python
def calculate_ndcg(chunk_id, predictions):
    if chunk_id not in predictions:
        return 0
    y_pred = np.linspace(1, 0, len(predictions)).tolist()
    y_true = [0 if item != chunk_id else 1 for item in predictions]

    return ndcg_score([y_true], [y_pred])
```

This is a simple implementation. LanceDB returns the results for us with most relevant results at the front of the list. We can create a relevant score using a simple `np.linspace` value. As we see below, similar to our retrieved results, values that are further in front will have larger scores, indicating higher relevancy.

```
>>> np.linspace(1,0,4)
array([1.        , 0.66666667, 0.33333333, 0.        ])
```

Since we only have a single relevant chunk, only our known chunk will have a label of `1` while all of the others will have a value of 0. 

#### MRR

MRR refers to Mean Reciprocal Rank is much simpler to implement and understand. It's important to note here that the MRR is only useful in calculating the retrieval quality with respect to the **first relevant item in the returned list**. If we have multiple relevant items, then NDCG is a much better alternative.

If we have 4 items `a,b,c,d` where only `a` is the relevant item, then our Reciprocal Rank(RR) is simply 1. If `c` is the relevant item,then our RR is going to be `1/3`. But, if all of the items are irrelevant, then our RR is going to be 0

 We can express this in the form of a function as 

```python
def calculate_mrr(chunk_id:str,predictions:List[str]):
    return 0 if chunk_id not in predictions else 1 / (predictions.index(chunk_id) + 1)
```

Once we've performed this calculation for a few different retrievals, then the MRR is simply the mean of the individual RRs for each list of retrieved chuns.

### Calculation

Now, let's bring it all together in a single call 

```python
results = [["a", "b", "c"], ["b", "a", "c"], ["b", "c", "a"]]

evals = {
    "MRR":calculate_mrr,
    "NDCG":calculate_ndcg
}
evaluations = [
    {metric: fn("a", result) for metric, fn in evals.items()} for result in results
]

df = pd.DataFrame(evaluations)
console = Console()
console.print(df)
```

This gives us the values as seen below


|MRR |     NDCG |
| --- | --- |
| 1.00 |  1.00 |
| 0.50 |  0.63 |
| 0.33 |  0.50 |


As we can see, as the relevant item ( in this example above 'a' ) gets shifted further, our MRR and NDCG decrease slowly. But, MRR decreases significantly faster and more aggressively than that of NDCG.

### Varying K

Now, we also want to make sure we can calculate these metrics for different values of `k` - to do so, we can use a simple decorator which passes a slice of the list of elements into the metric calculation. 

```python
def slice_predictions_decorator(num_elements: int):
    def decorator(func):
        def wrapper(chunk_id, predictions):
            sliced_predictions = predictions[:num_elements]
            return func(chunk_id, sliced_predictions)

        return wrapper

    return decorator
```

Let's scale our original example just now to 5 values where `a` gets shifted back progressively by one position on each iteration.


```python
evals = {}
SIZES = [3, 5]
for size in SIZES:
    evals[f"MRR@{size}"] = slice_predictions_decorator(size)(calculate_mrr)

for size in SIZES:
    evals[f"NDCG@{size}"] = slice_predictions_decorator(size)(calculate_ndcg)

results = [
    ["a", "b", "c", "d", "e"],
    ["e", "a", "b", "c", "d"],
    ["d", "e", "a", "b", "c"],
    ["c", "d", "e", "a", "b"],
    ["b", "c", "d", "e", "a"],
]

evaluations = [
    {metric: fn("a", result) for metric, fn in evals.items()} for result in results
]

df = pd.DataFrame(evaluations)
console = Console()
console.print(df)
```


This gives us the output as seen below. It makes sense to have a MRR@3/NDCG@3 at 0 from the 4th element onwards since by that point, `a` no longer exists within the slice of the first 3 elements that we're takking.


| MRR@3 | MRR@5 | NDCG@3 | NDCG@5 |
| --- | --- | --- | --- |
| 1.00 | 1.00 | 1.00 | 1.00 |
| 0.50 | 0.50 | 0.63 | 0.63 |
| 0.33 | 0.33 | 0.50 | 0.50 |
| 0.00 | 0.25 | 0.00 | 0.43 |
| 0.00 | 0.20 | 0.00 | 0.39 |

## Putting the Pieces together

Now that we've implemented all of the pieces, let's start testing our semantic search retrieval against a set of given synthethic queries. Let's first start by writing a function to get chunks that we previously embedded from our `lancedb` database. 

We can do this by taking advantage of the `to_batches()` method that the `LanceTable` provides. This returns a `pyArrow` dataset that provides a`RecordBatch` object which can be consumed as an iterator.

```python
def fetch_chunks(table: LanceTable, n=int) -> Iterable[TextChunk]:
    for batch in table.to_lance().to_batches():
        chunk_ids = batch["chunk_id"]
        text_arr = batch["text"]
        for id, text in zip(chunk_ids, text_arr):
            yield TextChunk(chunk_id=str(id), text=str(text))
```

??? info "What's in a batch?"
    The `RecordBatch` object is a `PyArrow` specific object and returns the specific properties of each row. We therefore need to zip the chunk_ids and the texts that we get from the batch together to match the chunk_id to its specific text paragraph.

    Once we do so, we convert the `StringScalar` object into its string representation so that we can use it in our query method

This in turn gives us a generator containing `TextChunk` objects that we can consume like any other normal list. Once we've fetched the relevant chunks, we need to generate the relevant synthethic questions. We can use our `generate_questions` that we defined earlier to batch the generation of these questions easily with a small modification.

This time, we'll set it to accept the `TextChunk` object instead so that we always get the generated question with the original chunk information. This helps prevent any potential errors arising from mixing up the generated question with the wrong chunk.

```python
async def generate_question_answer_pair(
    chunk: TextChunk,
) -> tuple[QuestionAnswerPair, TextChunk]:
    return (
        await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a world class algorithm that excels at generating great questions that can be only answered by a specific text that will soon be passed to you. ",
                },
                {
                    "role": "assistant",
                    "content": f"Generate a question and answer pair that uses information and content that is specific to the following text chunk, including a chain of thought:\n\n{chunk}",
                },
            ],
            response_model=QuestionAnswerPair,
        ),
        chunk,
    )

async def generate_questions(
    chunks: Iterable[TextChunk],
) -> List[tuple[QuestionAnswerPair, TextChunk]]:
    coros = [generate_question_answer_pair(chunk) for chunk in chunks]
    return await asyncio.gather(*coros)
```

We can then just recycle our original `get_response` methods that we used to query our database along with the evaluation metrics we defined as seen in the code below.

```python
db = connect("./db")
chunk_table = db.open_table("pg")
chunks = fetch_chunks(chunk_table)
questions = run(generate_questions(chunks))

evals = {}
SIZES = [3, 10, 25]
for size in SIZES:
    evals[f"RR@{size}"] = slice_predictions_decorator(size)(calculate_mrr)

for size in SIZES:
    evals[f"NDCG@{size}"] = slice_predictions_decorator(size)(calculate_ndcg)

results = []
for question in questions:
    qa_pair, chunk = question
    responses = get_response("./db", "pg", qa_pair.question, limit=25)
    chunk_ids = [retrieved_chunk.chunk_id for retrieved_chunk in responses]
    results.append(
        {metric: fn(chunk.chunk_id, chunk_ids) for metric, fn in evals.items()}
    )

df = pd.DataFrame(results)
console = Console()

avg = df.mean()
console.print(avg)
```

This in turn gives the following result when we run it against all the chunks in our database

| Metric | MRR@3 | MRR@10 | MRR@25 | NDCG@3 | NDCG@10 | NDCG@25 |
| --- | --- | --- | --- | --- | --- | --- |
| Score | 0.88 | 0.89 | 0.89 | 0.90 | 0.91 | 0.92 |

This is huge! We've just managed to generate and bootstrap some synthethic data in order to test how good semantic search works with our embedded data.

### Results

If we look at the results, we can see that on average, we get the most relevant results within the top 3 results. This is great because it means that on average, we can expect to get good results with our synthethic search.

We can use the `Rouge` metric to evaluate the first 30 questions that we've generated. This is done using the `rouge` package which we can install with 

```
pip install rouge
```

We can then modify our earlier script logic as seen below to calculate the `Rouge` score for unigrams, bigrams and the longest common subsequence.

```python
from rouge import Rouge

db = connect("./db")
chunk_table = db.open_table("pg")
chunks = fetch_chunks(chunk_table, 30)
questions = run(generate_questions(chunks))

rouge = Rouge()

results = []
for question in questions:
    qa_pair, chunk = question
    scores = rouge.get_scores(qa_pair.question, chunk.text)[0]
    scores = {
        f"{metric}-{key}": value
        for metric, sub_dict in scores.items()
        for key, value in sub_dict.items()
    }
    results.append({**scores, "question": qa_pair.question, "text": chunk.text})

df = pd.DataFrame(results)
console = Console()
avg = df.select_dtypes(include=["number"]).mean()
```

We want to focus on the precision here - which indicates the overlap between the generated question and the original text chunk.

| Metric | rouge-1-p | rouge-2-p | rouge-l-p |
| --- | --- | --- | --- |
| Value | 0.51 | 0.20 | 0.46 |

We can see that when it comes to unigrams and longest common subsequences, we have a ROUGE score of ~50% for both. This indicates that there is a good amount of structural or sentence-level similarity between the question and the original text chunk.

## Conclusion

In this article, we walked you through a simple example of how to generate and evaluate the quality of your retrieval algorithm using semantic search. We also showcased some short comings of the approach, in particular, the high overlap between the generated questions and the original text chunks which might explain the high performance of the embedding search.

There's a lot of room for improvement in terms of the chunking, generation of questions and the retrieval. Some easy ways are to generate metadata when doing data ingestion, generating questions using multiple chunks or even combining simple semantic search with BM25. 

In future articles, we'll explore how to explore the results in greater detail and iteratively improve on different aspects of your RAG application.
In this project I'm trying to make good AI code generator (analogue of [github copilot](https://github.com/features/copilot)) with RAG (Retrieval Augmented Generation), using [llamaindex](https://www.llamaindex.ai).

# How is RAG working?

![](assets/rag.webp)
Image source: [anyscale](https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1)

# Components

## Embeddings

Embedding models take text as input, and return a long list of numbers used to capture the semantics of the text. So it can be important what embedding are we using. In text it is not very important in what order are the words, but in code it could break everything. We can choose one of this embeddings:

1. [BAAI/bge-base-en-v1.5](https://huggingface.co/Salesforce/codet5p-110m-embedding)
2. [Salesforce/codet5p-110m-embedding](https://huggingface.co/Salesforce/codet5p-110m-embedding)

(I'm testing only free versions, so I skipped the [ada-002](https://platform.openai.com/docs/guides/embeddings))

To test these


## LLM

I've found three interesting LLM's to test. As RAG I would use my project that solves quadratic equation. I'll ask to write a function, that solves quadratic equations, using equation coefficients.

LLMs:
1. Llama 3.1 (8B)
2. Moondream 2 (1.4B)
3. deepseek-coder-v2 (16B)

(I tested every model on MacBook Pro with 8gb of RAM)

### Llama 3.1
Works pretty well. In six out of ten launches it returned well working code for my project. One time code worked almost correct (4/5 tests passed), two times partially correct (3/5) and in other cases code did not compile.

The shortest query time was 28.99s. The longest time was 56.6s. In average it needed about 40s for query. Pretty good result.

### Moondream 2
This model is not as heavy as ```llama3```, so we can notice that in the query time. This model works much faster, but it has no benefit. Usually it gives answers like ```000``` or ```________```, not even at least a code. So this is very bad model for code generation.

### deepseek-coder-v2
Deepseek is the heaviest model I've tested here. It was actually created for code generation. But on the first launch it became very clear, that for my configuration this model works too slow (It generated one answer for 20 minutes). It can generate working and good code, but it is too slow, not even comparable with ```llama3```.

After all these tests I've decided, that ```llama3``` is the best model for my configuration.


## Execution time

```py
response = query_engine.query("Give me a program, that will do XOR operation with 3 integers and return the binary result of operations"
                               "Think step by step, this is very important for my career. Respond to me only with code.")
```

That's the place where program starts working too slow.

```query_engine``` is from ```BaseQueryEngine``` class. So, ```query``` function's code is
```py
def query(self, str_or_query_bundle: QueryType) -> RESPONSE_TYPE:
        dispatcher.event(QueryStartEvent(query=str_or_query_bundle))
        with self.callback_manager.as_trace("query"):
            if isinstance(str_or_query_bundle, str):
                str_or_query_bundle = QueryBundle(str_or_query_bundle)
            query_result = self._query(str_or_query_bundle)
        dispatcher.event(
            QueryEndEvent(query=str_or_query_bundle, response=query_result)
        )
        return query_result
```

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

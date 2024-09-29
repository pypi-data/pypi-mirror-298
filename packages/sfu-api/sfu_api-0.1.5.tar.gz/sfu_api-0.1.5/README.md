# sfu-api

A client for SFU's course outline API.

## Examples

Printing all the terms of the first year

```py
client = sfu_api.Client()
years = client.get_years()
terms = client.get_terms(years[0])
for term in terms:
    print(term)

# summer
# fall
```

Getting the course description for _MATH 150 D101_ (Calculus I with Review) in the Summer 2023 term

```py
client = sfu_api.Client()
outline = client.get_outline("2023", "summer", "math", "150", "d101")
print(outline.info.description)
```

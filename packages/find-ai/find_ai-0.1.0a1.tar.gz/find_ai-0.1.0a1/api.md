# CompanyEnrichment

## Enrich

Types:

```python
from find_ai.types.company_enrichment import EnrichCreateResponse, EnrichRetrieveResponse
```

Methods:

- <code title="post /v1/companies/enrich">client.company_enrichment.enrich.<a href="./src/find_ai/resources/company_enrichment/enrich.py">create</a>(\*\*<a href="src/find_ai/types/company_enrichment/enrich_create_params.py">params</a>) -> <a href="./src/find_ai/types/company_enrichment/enrich_create_response.py">EnrichCreateResponse</a></code>
- <code title="get /v1/companies/enrich/{token}">client.company_enrichment.enrich.<a href="./src/find_ai/resources/company_enrichment/enrich.py">retrieve</a>(token) -> <a href="./src/find_ai/types/company_enrichment/enrich_retrieve_response.py">EnrichRetrieveResponse</a></code>

# PeopleEnrichment

## Enrich

Types:

```python
from find_ai.types.people_enrichment import EnrichCreateResponse, EnrichRetrieveResponse
```

Methods:

- <code title="post /v1/people/enrich">client.people_enrichment.enrich.<a href="./src/find_ai/resources/people_enrichment/enrich.py">create</a>(\*\*<a href="src/find_ai/types/people_enrichment/enrich_create_params.py">params</a>) -> <a href="./src/find_ai/types/people_enrichment/enrich_create_response.py">EnrichCreateResponse</a></code>
- <code title="get /v1/people/enrich/{token}">client.people_enrichment.enrich.<a href="./src/find_ai/resources/people_enrichment/enrich.py">retrieve</a>(token) -> <a href="./src/find_ai/types/people_enrichment/enrich_retrieve_response.py">EnrichRetrieveResponse</a></code>

# Searches

Types:

```python
from find_ai.types import SearchCreateResponse, SearchRetrieveResponse
```

Methods:

- <code title="post /v1/searches">client.searches.<a href="./src/find_ai/resources/searches.py">create</a>(\*\*<a href="src/find_ai/types/search_create_params.py">params</a>) -> <a href="./src/find_ai/types/search_create_response.py">SearchCreateResponse</a></code>
- <code title="get /v1/searches/{id}">client.searches.<a href="./src/find_ai/resources/searches.py">retrieve</a>(id) -> <a href="./src/find_ai/types/search_retrieve_response.py">SearchRetrieveResponse</a></code>

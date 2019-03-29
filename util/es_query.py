def fuzzy(value: str):
    return {
        "query": {
            "fuzzy": {
                "tags": {
                    "value": value,
                    "boost": 1.0,
                    "fuzziness": 6,
                    "prefix_length": 0,
                    "max_expansions": 100,
                    "transpositions": True,
                }
            }
        }
    }


def wildcard(value: str):
    wildcard_value = ''.join(a + b for a, b in zip(value, '*' * len(value)))
    return {
        "query": {
            "wildcard": {
                "tags": {
                    "value": wildcard_value,
                    "boost": 1.0,
                    "rewrite": "top_terms_10",
                }
            }
        }
    }


def term(value: str):
    return {
        "query": {
            "term": {
                "tags": value
            }
        }
    }


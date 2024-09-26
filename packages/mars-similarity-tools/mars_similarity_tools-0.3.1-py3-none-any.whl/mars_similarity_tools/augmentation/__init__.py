from mars_vectorizer_sdk import Vectorizer, GroupParser, VectorGroup
from mars_similarity_tools.storages import KeyValueStorage

from typing import List, Tuple, Dict
from time import sleep
from dataclasses import dataclass
from functools import reduce
from requests import post
from itertools import chain, compress as compress_iter
from more_itertools import chunked
from hashlib import sha256
from dill import dumps, loads
from gzip import compress, decompress
from maz import compose

dumps_compress = lambda x: compress(dumps(x))
loads_decompress = lambda x: loads(decompress(x))
loads_or_none = lambda x: loads(x) if x is not None else None

@dataclass
class ItemVectorizer:

    """
        A vectorizer service that takes a dictionary and returns a VectorGroup.
        In between, the dictionary is parsed using a GroupParser into a Group.
        Check mars_vectorizer_sdk for more information.
    """

    vectorizer: Vectorizer
    parser: GroupParser

    def __call__(self, items: List[dict]) -> List[VectorGroup]:
        return list(
            map(
                compose(self.vectorizer, self.parser),
                items
            )
        )
    
@dataclass
class GQLQuery:

    query: str          # The GQL query (not the body of the query, just the name of it).
    query_input: str    # The argument input name for the query.
    items_type: str     # The GQL input type for the items.
    fields: str         # Body of the query
    data_path: list     # Path to the data in the response

    def __call__(self, items: List[dict]) -> dict:
        return {
            "query": f"""
                query Query($items: [{self.items_type}]!) {{
                    {self.query}({self.query_input}: $items) {{
                        {self.fields}  
                    }}
                }}
            """,
            "variables": {
                "items": items,
            }
        }
    
    def parse_response(self, response: dict) -> list:
        return reduce(lambda x, y: x[y], self.data_path, response)
    
@dataclass
class GraphQLSource:

    url: str
    headers: dict

    def __call__(self, json: dict) -> dict:
        response = post(
            self.url,
            json=json,
            headers=self.headers,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch vectors from federated graph. Status code: {response.status_code}, response: {response.text}")
        
@dataclass
class FederatedGraphVectorizer(ItemVectorizer):

    """
        Combines a federated graph (or any GraphQL source) and a vectorizer service to create vectorized objects. 
        It works by taking a list of dict items, fetching meta data for them through the GQL source, regrouping the meta result
        using the QueryGroupParser and then vectorizing the result using the vectorizer service. Returned is a VectorGroup.
    """

    source:         GraphQLSource
    query:          GQLQuery
    
    batch_size:     int
    timeout:        float

    cache:          KeyValueStorage
    cache_key:      str = "vector"

    def _portion_call(self, batch: List[dict], force_update: bool = False) -> Dict[str, VectorGroup]:
        keys = list(map(self._hash_item, batch))
        existing = self.cache.mget(keys)

        if any(map(lambda x: x is None, existing)) or force_update:

            # We need to replace all "existing" if force_update is True
            if force_update:
                existing = [None] * len(existing)

            # Timeout needs to be set to hold for too fast requests
            sleep(self.timeout)

            response = self.source(
                json=self.query(
                    # All items that does not exist in the cache
                    list(compress_iter(batch, map(lambda x: x is None, existing)))
                ),
            )

            # Saving the once not existing to cache
            self.cache.mset(
                dict(
                    zip(
                        compress_iter(keys, map(lambda x: x is None, existing)),
                        map(
                            lambda x: self.vectorizer(self.parser(x)), 
                            self.query.parse_response(response)
                        )
                    )
                )
            )

        return self.cache.mget(keys)
        
    def _hash_item(self, item: dict):
        """Needs to be hashed with specific settings"""
        return f"{self.cache_key}:{sha256(dumps({**item, 'qg': self.query.fields, 'source': self.source.url, 'parser': self.parser.sha256(), 'vectorizer': self.vectorizer.sha256()})).hexdigest()}"
    
    def __call__(self, items: List[dict], force_update: bool = False) -> List[Tuple[str, VectorGroup]]:
        return list(
            chain(
                *map(
                    lambda batch: self._portion_call(
                        batch,
                        force_update,
                    ),
                    chunked(
                        items, 
                        self.batch_size
                    )
                )
            )
        )
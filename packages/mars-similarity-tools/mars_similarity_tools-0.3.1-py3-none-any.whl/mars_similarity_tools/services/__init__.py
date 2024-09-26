import numpy as np

from mars_similarity_tools.models import SimilarityObject, SimilarityResult
from mars_similarity_tools.storages import KeyValueStorage, LocalStorage
from mars_similarity_tools.augmentation import ItemVectorizer
from mars_vectorizer_sdk import VectorGroup

from pickle import dumps, loads
from gzip import compress, decompress
from itertools import starmap, islice
from dataclasses import dataclass, field
from typing import List, Dict
from maz import fnmap
from operator import itemgetter

decompress_load = lambda x: loads(decompress(x))
compress_dump   = lambda x: compress(dumps(x))

@dataclass
class VectorSimilarityService:

    augmentor:  ItemVectorizer
    
    def similarity_search(self, source_objects: List[SimilarityObject], target_obj: SimilarityObject, bias: dict = {}) -> List[SimilarityResult]:

        """Searches for similar car keys in a given namespace."""

        # Get the car keys
        objects = [target_obj.to_dict()] + list(map(lambda x: x.to_dict(), source_objects))

        # Vectorize car keys (cache is used if already vectorized)
        vector_groups = self.augmentor(objects)

        # Vectorize the car key and search for similar vectors in the vector storage.
        # Notice we apply the bias here to the vectors to get a weighted average of the vectors.
        vectors = np.array(
            list(
                map(
                    lambda x: x.aggregate(bias), 
                    vector_groups,
                )
            )
        )

        # Create a similarity search based on the vector groups
        # It is the norm between the given car key vectors to all other vectors
        query_result = np.linalg.norm(vectors[1:]-vectors[0], axis=1)

        return list(
            starmap(
                lambda o, score: SimilarityResult(
                    score=score,
                    obj=o[0].from_dict(o[1]),
                ),
                zip(
                    zip(
                        source_objects,
                        objects[1:]
                    ),
                    query_result
                )
            )
        )

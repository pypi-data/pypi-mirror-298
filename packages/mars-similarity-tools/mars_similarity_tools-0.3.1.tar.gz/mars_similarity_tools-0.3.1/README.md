# Mars Similarity Tools
A small tools library for getting vector similarity measurement working in no time.

# Example
Here's a basic similarity search and vectorization example. We instantiate a `VectorSimilarityService` which needs an `Augmentor` of some kind. The `Augmentor` should be responsible for taking objects inherited by `SimilarityObject` class and return vectorized grouped objects (as a `VectorGroup` object). Before a `SimilarityObject` can be transformed into a `VectorGroup` it will pass the `GroupParser` first. That one will rearrange the properties of the objects into groups, which is given in the parser. We need to do this since multiple properties of an object should in the end be represented by one vector together. 

```python
# First things first. Create a similarity model we want to measure similarity between
# And yes! You could create a seperate Color class that holds name and description for Color.
@dataclass(frozen=True) # "frozen" is Important!
class Bicycle(SimilarityObject):

    id: str
    color_name: str
    color_description: str
    wheel_size: int
    model: str

# Then create the parser, vectorizer, augmentor and service.
service = VectorSimilarityService(
    augmentor=ItemVectorizer(
        vectorizer=Vectorizer(),
        parser=GroupParser(
            name=Bicycle.__class__.__name__, 
            children=[
                GroupParser(
                    name="color",
                    children=[
                        PropertyParser(
                            name="color name",
                            dtype=str,
                            path=["color_name"]
                        ),
                        PropertyParser(
                            name="color description",
                            dtype=str,
                            path=["color_description"]
                        ),
                    ],
                ),
                PropertyParser(
                    name="wheel_size",
                    dtype=int,
                    path=["wheel_size"]
                ),
                PropertyParser(
                    name="model",
                    dtype=str,
                    path=["model"]
                ),
            ]
        ),
    )
)

# Now we can create a namespace and add objects to that namespace.
objects = [
    Bicycle(
        id="1",
        color_name="red",
        color_description="A red bicycle",
        wheel_size=26,
        model="mountain"
    ),
    Bicycle(
        id="2",
        color_name="blue",
        color_description="A blue bicycle",
        wheel_size=26,
        model="mountain"
    ),
    Bicycle(
        id="3",
        color_name="green",
        color_description="A green bicycle",
        wheel_size=28,
        model="racer"
    ),
]

# Now we can perform a similarity search.
similarity_result = service.similarity_search(
    objects, 
    Bicycle(
        id="4",
        color_name="yellow",
        color_description="A yellow bicycle",
        wheel_size=28,
        model="racer"
    ), 
)

# Sort by similarity score
sorted_similarity_result = sorted(
    similarity_result,
    key=lambda x: x.score
)

assert len(sorted_similarity_result) == 3
assert type(sorted_similarity_result[0].obj) == Bicycle
assert type(sorted_similarity_result[1].obj) == Bicycle

# We could also do a similarity search including some bias to the search.
# For instance, we might want to find a similar bicycle but we want to bias the search
# towards the color.
biased_similarity_result = service.similarity_search(
    objects, 
    Bicycle(
        id="4",
        color_name="yellow",
        color_description="A yellow bicycle",
        wheel_size=28,
        model="racer"
    ), 
    bias={"color": 1.2, "wheel_size": 0.2, "model": 0.2}
)

# Sort by similarity score
sorted_biased_similarity_result = sorted(
    biased_similarity_result,
    key=lambda x: x.score
)

assert len(sorted_biased_similarity_result) == 3
assert type(sorted_biased_similarity_result[0].obj) == Bicycle
assert type(sorted_biased_similarity_result[1].obj) == Bicycle
```
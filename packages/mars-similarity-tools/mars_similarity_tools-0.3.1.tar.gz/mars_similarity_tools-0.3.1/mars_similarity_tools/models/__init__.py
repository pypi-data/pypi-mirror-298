from dataclasses import dataclass, asdict
from hashlib import sha256
from dill import dumps

@dataclass(frozen=True)
class SimilarityObject:

    def sha256(self) -> str:
        return sha256(dumps(self)).hexdigest()
    
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SimilarityObject":
        return cls(**d)
    
@dataclass
class SimilarityResult:
    
    score: float
    obj: SimilarityObject
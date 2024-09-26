import re
from typing import List, Optional, Any
from dataclasses import dataclass, field
from dill import dumps, loads, HIGHEST_PROTOCOL
from gzip import compress, decompress
from maz import compose

compress_dumps = lambda x: compress(dumps(x, HIGHEST_PROTOCOL))
decompress_loads = lambda x: loads(decompress(x)) if x is not None else None

@dataclass
class KeyValueStorage:

    """
        Key-value storage specification data model.
    """
    
    def set(self, key: str, value: str):
        raise NotImplementedError("Method not implemented")
    
    def get(self, key: str) -> Optional[str]:
        raise NotImplementedError("Method not implemented")
    
    def delete(self, key: str):
        raise NotImplementedError("Method not implemented")
    
    def exists(self, key: str) -> bool:
        raise NotImplementedError("Method not implemented")
    
    def mget(self, keys: List[str]) -> List[Optional[str]]:
        raise NotImplementedError("Method not implemented")
                                  
    def mset(self, mapping: dict):
        raise NotImplementedError("Method not implemented")
    
    def keys(self, pattern: str) -> List[str]:
        raise NotImplementedError("Method not implemented")
    
@dataclass
class EmptyStorage(KeyValueStorage):

    """
        Empty key-value cache storage data model.
    """
    
    def set(self, key: str, value: Any):
        pass
    
    def get(self, key: str) -> Optional[str]:
        return None
    
    def delete(self, key: str):
        pass
    
    def exists(self, key: str) -> bool:
        return False
    
    def mget(self, keys: List[str]) -> List[Optional[str]]:
        return [None] * len(keys)
                                  
    def mset(self, mapping: dict):
        pass

    def keys(self, pattern: str) -> List[str]:
        return []
    
@dataclass
class LocalStorage(KeyValueStorage):

    """
        Local key-value cache storage data model.
    """

    data: dict = field(default_factory=dict)
    
    def set(self, key: str, value: Any):
        self.data[key] = compress_dumps(value)
    
    def get(self, key: str) -> Optional[str]:
        return decompress_loads(self.data.get(key, None))
    
    def delete(self, key: str):
        self.data.pop(key, None)
    
    def exists(self, key: str) -> bool:
        return key in self.data
    
    def mget(self, keys: List[str]) -> List[Optional[str]]:
        return list(map(compose(decompress_loads, self.data.get), keys))
                                  
    def mset(self, mapping: dict):
        self.data.update(
            dict(
                zip(
                    mapping.keys(),
                    map(compress_dumps, mapping.values())
                )
            )
        )

    def keys(self, pattern: str) -> List[str]:
        return list(filter(lambda x: re.search(pattern, x), self.data.keys()))
    
@dataclass
class RemoteStorage(KeyValueStorage):

    """
        RemoteStorage accepts a dict-like object as a remote storage to act on.
        Requires functions "set", "get", "delete", "exists", "mget" and "mset" to be implemented.
    """

    remote: type
    
    def set(self, key: str, value: Any):
        self.remote.set(key, compress_dumps(value))
    
    def get(self, key: str) -> Optional[str]:
        return decompress_loads(self.remote.get(key))
    
    def delete(self, key: str):
        self.remote.delete(key)
    
    def exists(self, key: str) -> bool:
        return self.remote.exists(key)
    
    def mget(self, keys: List[str]) -> List[Optional[str]]:
        return list(map(decompress_loads, self.remote.mget(keys)))
                                  
    def mset(self, mapping: dict):
        self.remote.mset(
            dict(
                zip(
                    mapping.keys(),
                    map(compress_dumps, mapping.values())
                )
            )
        )

    def keys(self, pattern: str) -> List[str]:
        return self.remote.keys(pattern)
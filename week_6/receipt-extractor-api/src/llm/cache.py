"""Simple in-memory LRU cache keyed by (prompt_version, input_hash).

Rule: the cache key MUST include prompt_version, because changing the prompt
invalidates every previous answer.
"""
import hashlib
from collections import OrderedDict
from typing import Optional
from src.llm.schema import ExtractOutput

_MAX_ENTRIES = 256
_cache: "OrderedDict[str, ExtractOutput]" = OrderedDict()


def _key(prompt_version: str, user_text: str) -> str:
    h = hashlib.sha256(user_text.encode("utf-8")).hexdigest()[:16]
    return f"{prompt_version}:{h}"


def get(prompt_version: str, user_text: str) -> Optional[ExtractOutput]:
    k = _key(prompt_version, user_text)
    if k in _cache:
        _cache.move_to_end(k)  # LRU refresh
        return _cache[k]
    return None


def put(prompt_version: str, user_text: str, value: ExtractOutput) -> None:
    k = _key(prompt_version, user_text)
    _cache[k] = value
    _cache.move_to_end(k)
    while len(_cache) > _MAX_ENTRIES:
        _cache.popitem(last=False)


def stats() -> dict:
    return {"size": len(_cache), "max": _MAX_ENTRIES}
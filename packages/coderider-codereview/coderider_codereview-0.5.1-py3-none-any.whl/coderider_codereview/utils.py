import hashlib
import json


def calc_digest(content) -> str:
    try:
        if not isinstance(content, str):
            content = json.dumps(content, sort_keys=True)
    except TypeError as _e:
        content = repr(content)

    return hashlib.sha256(content.encode()).hexdigest()

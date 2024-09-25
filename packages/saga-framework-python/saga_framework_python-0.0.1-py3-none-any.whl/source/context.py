from typing import Dict, Any


class Context:
    def __init__(self):
        self.data: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)
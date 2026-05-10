"""Persistent storage of already-notified item URLs (JSON file)."""
import json
import logging
import os
import threading
from typing import Iterable, Set

log = logging.getLogger("storage")
_lock = threading.Lock()


class SeenStore:
    def __init__(self, path: str):
        self.path = path
        self._seen: Set[str] = set()
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            log.info("No existing store at %s; starting empty.", self.path)
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self._seen = set(data)
            log.info("Loaded %d seen URLs from %s", len(self._seen), self.path)
        except (OSError, json.JSONDecodeError) as e:
            log.error("Could not load store (%s); starting empty.", e)

    def _save(self) -> None:
        tmp = f"{self.path}.tmp"
        try:
            os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(sorted(self._seen), f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)
        except OSError as e:
            log.error("Could not persist store: %s", e)

    def is_empty(self) -> bool:
        return not self._seen

    def has(self, url: str) -> bool:
        return url in self._seen

    def add_many(self, urls: Iterable[str]) -> None:
        with _lock:
            before = len(self._seen)
            self._seen.update(urls)
            if len(self._seen) != before:
                self._save()

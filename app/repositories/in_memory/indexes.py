from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, Hashable, TypeVar

TEntity = TypeVar("TEntity")
TKey = TypeVar("TKey", bound=Hashable)
TId = TypeVar("TId", bound=Hashable)


@dataclass
class IndexManager(Generic[TEntity, TId]):
    field_to_extractor: dict[str, Callable[[TEntity], Any]]

    _indexes: dict[str, _FieldIndex[TEntity, Any, TId]] = field(init=False)

    def __post_init__(self) -> None:
        self._indexes = {
            _field: _FieldIndex(key_extractor=extractor)
            for _field, extractor in self.field_to_extractor.items()
        }

    def create_one(self, entity_id: TId, entity: TEntity) -> None:
        for index in self._indexes.values():
            index.create_one(entity_id, entity)

    def delete_one(self, entity_id: TId, entity: TEntity) -> None:
        for index in self._indexes.values():
            index.delete_one(entity_id, entity)

    def update_one(
        self, entity_id: TId, old_entity: TEntity, new_entity: TEntity
    ) -> None:
        for index in self._indexes.values():
            index.update_one(entity_id, old_entity, new_entity)

    def read_many(self, **params: Any) -> set[TId]:
        if not params:
            raise ValueError("No parameters specified")

        for _field in params:
            if _field not in self._indexes:
                raise ValueError(f"Unknown parameter <{_field}>")

        candidate_ids = [
            self._indexes[_field].read_one(value) for _field, value in params.items()
        ]

        candidate_ids.sort(key=len)
        ids = candidate_ids[0]
        for candidate_id in candidate_ids[1:]:
            ids = ids.intersection(candidate_id)
            if not ids:
                break

        return ids


@dataclass
class _FieldIndex(Generic[TEntity, TKey, TId]):
    key_extractor: Callable[[TEntity], TKey]

    _index: defaultdict[TKey, set[TId]] = field(
        default_factory=lambda: defaultdict(set), init=False
    )

    def create_one(self, entity_id: TId, entity: TEntity) -> None:
        key = self.key_extractor(entity)
        self._index[key].add(entity_id)

    def read_one(self, key: TKey) -> set[TId]:
        return self._index[key].copy()

    def update_one(
        self, entity_id: TId, old_entity: TEntity, new_entity: TEntity
    ) -> None:
        old_key = self.key_extractor(old_entity)
        new_key = self.key_extractor(new_entity)

        if old_key != new_key:
            self._index[old_key].discard(entity_id)
            self._clean_empty_index(old_key)
            self._index[new_key].add(entity_id)

    def delete_one(self, entity_id: TId, entity: TEntity) -> None:
        key = self.key_extractor(entity)
        self._index[key].discard(entity_id)

        self._clean_empty_index(key)

    def _clean_empty_index(self, old_key: TKey) -> None:  # pragma: no cover
        if not self._index[old_key]:
            del self._index[old_key]

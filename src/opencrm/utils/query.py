from typing import Literal, Self

Operator = Literal["=", "LIKE", "BEGINS", "ENDS", "CONTAINS"]


class QueryBuilder:
    def __init__(self) -> None:
        self._conditions: list[str] = []

    def where(self, field: str, operator: Operator, value: str) -> Self:
        self._conditions.append(f"{field}|{operator}|{value}")
        return self

    def equals(self, field: str, value: str) -> Self:
        return self.where(field, "=", value)

    def like(self, field: str, value: str) -> Self:
        return self.where(field, "LIKE", value)

    def begins_with(self, field: str, value: str) -> Self:
        return self.where(field, "BEGINS", value)

    def ends_with(self, field: str, value: str) -> Self:
        return self.where(field, "ENDS", value)

    def contains(self, field: str, value: str) -> Self:
        return self.where(field, "CONTAINS", value)

    def build(self) -> str | None:
        if not self._conditions:
            return None
        return self._conditions[0] if len(self._conditions) == 1 else self._conditions[0]

    def clear(self) -> Self:
        self._conditions.clear()
        return self


def query() -> QueryBuilder:
    return QueryBuilder()

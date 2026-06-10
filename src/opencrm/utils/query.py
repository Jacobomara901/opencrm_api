"""
Query builder for OpenCRM API filters.

OpenCRM uses a specific query string format: FIELDNAME|OPERATOR|VALUE
This module provides a fluent interface for building these queries.

Supported operators:
    - = : Exact match
    - LIKE : Pattern match (use % as wildcard)
    - BEGINS : Starts with
    - ENDS : Ends with
    - CONTAINS : Contains substring

Multiple conditions are joined with ``;`` which OpenCRM interprets as AND.
This is undocumented but verified against the live endpoint.

Example:
    >>> from opencrm import query
    >>> q = query().equals("leadstatus", "New")
    >>> q.build()
    'leadstatus|=|New'

Note:
    Negative operators (``!=``, ``NOT LIKE``, ``<>``, ``NE``, ...) are silently
    ignored by OpenCRM and treated as ``=``. They are deliberately not exposed.
"""

from typing import Literal, Self

Operator = Literal["=", "LIKE", "BEGINS", "ENDS", "CONTAINS"]
"""Valid operators for OpenCRM query strings."""


class QueryBuilder:
    """
    Fluent query builder for OpenCRM API filters.

    Builds query strings in OpenCRM's format: FIELDNAME|OPERATOR|VALUE.
    Multiple conditions are joined with ``;`` and combined with AND semantics.

    Example:
        >>> q = QueryBuilder()
        >>> q.equals("lastname", "Smith").equals("leadstatus", "New").build()
        'lastname|=|Smith;leadstatus|=|New'
    """

    def __init__(self) -> None:
        self._conditions: list[str] = []

    def where(self, field: str, operator: Operator, value: str) -> Self:
        """
        Add a condition with explicit operator.

        Args:
            field: The API field name to filter on. Use the query string field name
                from OpenCRM's field reference, not the API field name.
            operator: One of "=", "LIKE", "BEGINS", "ENDS", "CONTAINS".
            value: The value to match against.

        Returns:
            Self for method chaining.

        Example:
            >>> query().where("email", "LIKE", "%@example.com").build()
            'email|LIKE|%@example.com'
        """
        self._conditions.append(f"{field}|{operator}|{value}")
        return self

    def equals(self, field: str, value: str) -> Self:
        """
        Add an exact match condition (field = value).

        Example:
            >>> query().equals("leadstatus", "New").build()
            'leadstatus|=|New'
        """
        return self.where(field, "=", value)

    def like(self, field: str, value: str) -> Self:
        """
        Add a pattern match condition using LIKE operator.

        Example:
            >>> query().like("email", "%@gmail.com").build()
            'email|LIKE|%@gmail.com'
        """
        return self.where(field, "LIKE", value)

    def begins_with(self, field: str, value: str) -> Self:
        """
        Add a "starts with" condition.

        Example:
            >>> query().begins_with("company", "Acme").build()
            'company|BEGINS|Acme'
        """
        return self.where(field, "BEGINS", value)

    def ends_with(self, field: str, value: str) -> Self:
        """
        Add an "ends with" condition.

        Example:
            >>> query().ends_with("phone", "1234").build()
            'phone|ENDS|1234'
        """
        return self.where(field, "ENDS", value)

    def contains(self, field: str, value: str) -> Self:
        """
        Add a "contains" condition.

        Example:
            >>> query().contains("description", "urgent").build()
            'description|CONTAINS|urgent'
        """
        return self.where(field, "CONTAINS", value)

    def and_(self, other: "QueryBuilder") -> Self:
        """
        Append all conditions from another QueryBuilder.

        Returns:
            Self for method chaining.
        """
        self._conditions.extend(other._conditions)
        return self

    def is_empty(self) -> bool:
        """Whether the builder has no conditions."""
        return not self._conditions

    def build(self) -> str | None:
        """
        Build the query string.

        Returns:
            The query string in OpenCRM format, with multiple conditions joined
            by ``;`` (AND), or None if no conditions were added.
        """
        if not self._conditions:
            return None
        return ";".join(self._conditions)

    def clear(self) -> Self:
        """Clear all conditions and return self for chaining."""
        self._conditions.clear()
        return self


def query() -> QueryBuilder:
    """
    Create a new QueryBuilder instance.

    Example:
        >>> from opencrm import query
        >>> q = query().equals("status", "Active")
        >>> leads = client.leads.list(query=q)
    """
    return QueryBuilder()

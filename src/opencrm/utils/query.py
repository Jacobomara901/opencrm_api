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

Example:
    >>> from opencrm import query
    >>> q = query().equals("leadstatus", "New")
    >>> q.build()
    'leadstatus|=|New'

Note:
    OpenCRM has limited query support:
    - No negative queries (!=, NOT LIKE)
    - Chaining multiple conditions may produce inconsistent results
    - For complex filtering, retrieve data and filter client-side
"""

from typing import Literal, Self

Operator = Literal["=", "LIKE", "BEGINS", "ENDS", "CONTAINS"]
"""Valid operators for OpenCRM query strings."""


class QueryBuilder:
    """
    Fluent query builder for OpenCRM API filters.

    Builds query strings in OpenCRM's format: FIELDNAME|OPERATOR|VALUE

    Example:
        >>> q = QueryBuilder()
        >>> q.equals("lastname", "Smith").build()
        'lastname|=|Smith'

    Warning:
        OpenCRM only reliably supports single conditions. Multiple conditions
        may produce unexpected results. For complex queries, filter client-side.
    """

    def __init__(self) -> None:
        """Initialize an empty query builder."""
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

        Args:
            field: The API query string field name.
            value: The exact value to match.

        Returns:
            Self for method chaining.

        Example:
            >>> query().equals("leadstatus", "New").build()
            'leadstatus|=|New'
        """
        return self.where(field, "=", value)

    def like(self, field: str, value: str) -> Self:
        """
        Add a pattern match condition using LIKE operator.

        Args:
            field: The API query string field name.
            value: Pattern to match. Use % as wildcard.

        Returns:
            Self for method chaining.

        Example:
            >>> query().like("email", "%@gmail.com").build()
            'email|LIKE|%@gmail.com'
        """
        return self.where(field, "LIKE", value)

    def begins_with(self, field: str, value: str) -> Self:
        """
        Add a "starts with" condition.

        Args:
            field: The API query string field name.
            value: The prefix to match.

        Returns:
            Self for method chaining.

        Example:
            >>> query().begins_with("company", "Acme").build()
            'company|BEGINS|Acme'
        """
        return self.where(field, "BEGINS", value)

    def ends_with(self, field: str, value: str) -> Self:
        """
        Add an "ends with" condition.

        Args:
            field: The API query string field name.
            value: The suffix to match.

        Returns:
            Self for method chaining.

        Example:
            >>> query().ends_with("phone", "1234").build()
            'phone|ENDS|1234'
        """
        return self.where(field, "ENDS", value)

    def contains(self, field: str, value: str) -> Self:
        """
        Add a "contains" condition.

        Args:
            field: The API query string field name.
            value: The substring to search for.

        Returns:
            Self for method chaining.

        Example:
            >>> query().contains("description", "urgent").build()
            'description|CONTAINS|urgent'
        """
        return self.where(field, "CONTAINS", value)

    def build(self) -> str | None:
        """
        Build the query string.

        Returns:
            The query string in OpenCRM format, or None if no conditions added.

        Note:
            Due to OpenCRM API limitations, only the first condition is used
            when multiple conditions are added.
        """
        if not self._conditions:
            return None
        return self._conditions[0] if len(self._conditions) == 1 else self._conditions[0]

    def clear(self) -> Self:
        """
        Clear all conditions.

        Returns:
            Self for method chaining.
        """
        self._conditions.clear()
        return self


def query() -> QueryBuilder:
    """
    Create a new QueryBuilder instance.

    This is a convenience function for creating query builders with a cleaner syntax.

    Returns:
        A new QueryBuilder instance.

    Example:
        >>> from opencrm import query
        >>> q = query().equals("status", "Active")
        >>> leads = client.leads.list(query=q)
    """
    return QueryBuilder()

"""
SQLAlchemy converter module.
"""

from importlib.util import find_spec

if find_spec(name='sqlalchemy') is None:
    raise ImportError("SQLAlchemy is not installed. Please install it using 'pip install criteria-pattern[sqlalchemy]'")

from typing import Any, TypeVar, assert_never

from sqlalchemy import Column, and_, not_, or_
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import ColumnElement, UnaryExpression

from criteria_pattern import Criteria, FilterOperator, OrderDirection
from criteria_pattern.criteria import AndCriteria, NotCriteria, OrCriteria

T = TypeVar('T', bound=DeclarativeMeta)


class SqlAlchemyConverter:
    """
    SQLAlchemy converter.
    """

    @classmethod
    def convert(cls, criteria: Criteria, model: type[T], columns_mapping: dict[str, str] | None = None) -> Query[T]:
        """
        Convert the Criteria object to a SQLAlchemy Query.

        Args:
            criteria (Criteria): Criteria to convert.
            model (DeclarativeMeta): SQLAlchemy model.
            alias_mapping (dict[str, str], optional): Alias for column names. Default to {}.

        Returns:
            Query: Query object.
        """
        query: Query[T] = Query(model)

        if columns_mapping is None:
            columns_mapping = {}

        filters = cls._process_filters(criteria=criteria, model=model, columns_mapping=columns_mapping)
        if filters:
            query = query.filter(*filters)

        orders = cls._process_orders(criteria=criteria, model=model, columns_mapping=columns_mapping)
        if orders:
            query = query.order_by(*orders)

        return query

    @classmethod
    def _process_filters(  # noqa: C901
        cls,
        criteria: Criteria,
        model: type[T],
        columns_mapping: dict[str, str],
    ) -> list[ColumnElement[bool]]:
        """
        Process the Criteria and return a list of conditions.

        Args:
            criteria (Criteria): Criteria to process.
            model (DeclarativeMeta): SQLAlchemy model.
            columns_mapping (dict[str, str]): Alias for column names.

        Returns:
            list[BinaryExpression]: List of conditions.
        """
        conditions: list[ColumnElement[bool]] = []

        if isinstance(criteria, AndCriteria):
            left_conditions = cls._process_filters(
                criteria=criteria.left,
                model=model,
                columns_mapping=columns_mapping,
            )
            right_conditions = cls._process_filters(
                criteria=criteria.right,
                model=model,
                columns_mapping=columns_mapping,
            )
            conditions.append(and_(*left_conditions, *right_conditions))

            return conditions

        if isinstance(criteria, OrCriteria):
            left_conditions = cls._process_filters(
                criteria=criteria.left,
                model=model,
                columns_mapping=columns_mapping,
            )
            right_conditions = cls._process_filters(
                criteria=criteria.right,
                model=model,
                columns_mapping=columns_mapping,
            )
            conditions.append(or_(*left_conditions, *right_conditions))

            return conditions

        if isinstance(criteria, NotCriteria):
            not_conditions = cls._process_filters(
                criteria=criteria.criteria,
                model=model,
                columns_mapping=columns_mapping,
            )
            conditions.append(not_(*not_conditions))

            return conditions

        for filter in criteria.filters:
            field_name = columns_mapping.get(filter.field, filter.field)
            field: Column[Any] = getattr(model, field_name)

            match filter.operator:
                case FilterOperator.EQUAL:
                    conditions.append(field == filter.value)

                case FilterOperator.NOT_EQUAL:
                    conditions.append(field != filter.value)

                case FilterOperator.GREATER:
                    conditions.append(field > filter.value)

                case FilterOperator.GREATER_OR_EQUAL:
                    conditions.append(field >= filter.value)

                case FilterOperator.LESS:
                    conditions.append(field < filter.value)

                case FilterOperator.LESS_OR_EQUAL:
                    conditions.append(field <= filter.value)

                case FilterOperator.LIKE:
                    conditions.append(field.like(filter.value))

                case FilterOperator.NOT_LIKE:
                    conditions.append(~field.like(filter.value))

                case FilterOperator.CONTAINS:
                    conditions.append(field.contains(filter.value))

                case FilterOperator.NOT_CONTAINS:
                    conditions.append(~field.contains(filter.value))

                case FilterOperator.STARTS_WITH:
                    conditions.append(field.startswith(filter.value))

                case FilterOperator.NOT_STARTS_WITH:
                    conditions.append(~field.startswith(filter.value))

                case FilterOperator.ENDS_WITH:
                    conditions.append(field.endswith(filter.value))

                case FilterOperator.NOT_ENDS_WITH:
                    conditions.append(~field.endswith(filter.value))

                case FilterOperator.BETWEEN:
                    conditions.append(field.between(filter.value[0], filter.value[1]))

                case FilterOperator.NOT_BETWEEN:
                    conditions.append(~field.between(filter.value[0], filter.value[1]))

                case FilterOperator.IN:
                    conditions.append(field.in_(filter.value))

                case FilterOperator.NOT_IN:
                    conditions.append(~field.in_(filter.value))

                case FilterOperator.IS_NULL:
                    conditions.append(field.is_(None))

                case FilterOperator.IS_NOT_NULL:
                    conditions.append(field.isnot(None))

                case _:  # pragma: no cover
                    assert_never(filter.operator)

        return conditions

    @classmethod
    def _process_orders(
        cls,
        criteria: Criteria,
        model: type[T],
        columns_mapping: dict[str, str],
    ) -> list[UnaryExpression[Any]]:
        """
        Process the Criteria and return a list of order fields.

        Args:
            criteria (Criteria): Criteria to process.
            model (DeclarativeMeta): SQLAlchemy model.
            columns_mapping (dict[str, str]): Alias for column names.

        Returns:
            list[Column]: List of order fields.
        """
        orders = []

        for order in criteria.orders:
            field_name = columns_mapping.get(order.field, order.field)
            field: Column[Any] = getattr(model, field_name)

            match order.direction:
                case OrderDirection.ASC:
                    orders.append(field.asc())

                case OrderDirection.DESC:
                    orders.append(field.desc())

                case _:  # pragma: no cover
                    assert_never(order.direction)

        return orders

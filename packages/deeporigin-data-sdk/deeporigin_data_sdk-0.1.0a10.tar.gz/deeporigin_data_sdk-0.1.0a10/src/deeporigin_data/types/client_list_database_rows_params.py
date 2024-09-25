# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ClientListDatabaseRowsParams",
    "ColumnSelection",
    "Filter",
    "FilterRowFilterText",
    "FilterRowFilterNumber",
    "FilterRowFilterBoolean",
    "FilterRowFilterJoin",
    "FilterRowFilterJoinCondition",
    "FilterRowFilterJoinConditionRowFilterJoin",
    "FilterRowFilterJoinConditionRowFilterJoinCondition",
    "FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterText",
    "FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterNumber",
    "FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterBoolean",
    "FilterRowFilterJoinConditionRowFilterText",
    "FilterRowFilterJoinConditionRowFilterNumber",
    "FilterRowFilterJoinConditionRowFilterBoolean",
]


class ClientListDatabaseRowsParams(TypedDict, total=False):
    database_row_id: Required[Annotated[str, PropertyInfo(alias="databaseRowId")]]

    column_selection: Annotated[ColumnSelection, PropertyInfo(alias="columnSelection")]

    creation_block_id: Annotated[str, PropertyInfo(alias="creationBlockId")]

    creation_parent_id: Annotated[str, PropertyInfo(alias="creationParentId")]

    filter: Filter


class ColumnSelection(TypedDict, total=False):
    exclude: List[str]

    include: List[str]


class FilterRowFilterText(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["text"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[str, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "blank", "notBlank"]]


class FilterRowFilterNumber(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["number"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[float, PropertyInfo(alias="filterValue")]]

    operator: Required[
        Literal[
            "equals",
            "notEqual",
            "lessThan",
            "lessThanOrEqual",
            "greaterThan",
            "greaterThanOrEqual",
            "blank",
            "notBlank",
        ]
    ]


class FilterRowFilterBoolean(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["boolean"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[bool, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "blank", "notBlank"]]


class FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterText(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["text"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[str, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "blank", "notBlank"]]


class FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterNumber(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["number"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[float, PropertyInfo(alias="filterValue")]]

    operator: Required[
        Literal[
            "equals",
            "notEqual",
            "lessThan",
            "lessThanOrEqual",
            "greaterThan",
            "greaterThanOrEqual",
            "blank",
            "notBlank",
        ]
    ]


class FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterBoolean(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["boolean"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[bool, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "blank", "notBlank"]]


FilterRowFilterJoinConditionRowFilterJoinCondition: TypeAlias = Union[
    FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterText,
    FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterNumber,
    FilterRowFilterJoinConditionRowFilterJoinConditionRowFilterBoolean,
    object,
]


class FilterRowFilterJoinConditionRowFilterJoin(TypedDict, total=False):
    conditions: Required[Iterable[FilterRowFilterJoinConditionRowFilterJoinCondition]]

    filter_type: Required[Annotated[Literal["join"], PropertyInfo(alias="filterType")]]

    join_type: Required[Annotated[Literal["and", "or"], PropertyInfo(alias="joinType")]]


class FilterRowFilterJoinConditionRowFilterText(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["text"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[str, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "blank", "notBlank"]]


class FilterRowFilterJoinConditionRowFilterNumber(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["number"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[float, PropertyInfo(alias="filterValue")]]

    operator: Required[
        Literal[
            "equals",
            "notEqual",
            "lessThan",
            "lessThanOrEqual",
            "greaterThan",
            "greaterThanOrEqual",
            "blank",
            "notBlank",
        ]
    ]


class FilterRowFilterJoinConditionRowFilterBoolean(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["boolean"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[bool, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "blank", "notBlank"]]


FilterRowFilterJoinCondition: TypeAlias = Union[
    FilterRowFilterJoinConditionRowFilterJoin,
    FilterRowFilterJoinConditionRowFilterText,
    FilterRowFilterJoinConditionRowFilterNumber,
    FilterRowFilterJoinConditionRowFilterBoolean,
]


class FilterRowFilterJoin(TypedDict, total=False):
    conditions: Required[Iterable[FilterRowFilterJoinCondition]]

    filter_type: Required[Annotated[Literal["join"], PropertyInfo(alias="filterType")]]

    join_type: Required[Annotated[Literal["and", "or"], PropertyInfo(alias="joinType")]]


Filter: TypeAlias = Union[FilterRowFilterText, FilterRowFilterNumber, FilterRowFilterBoolean, FilterRowFilterJoin]

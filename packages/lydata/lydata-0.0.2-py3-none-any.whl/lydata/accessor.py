"""Module containing a custom accessor and helpers for querying lydata."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd
import pandas.api.extensions as pd_ext

from lydata.utils import (
    ModalityConfig,
    get_default_column_map,
    get_default_modalities,
)
from lydata.validator import construct_schema


def get_all_true(df: pd.DataFrame) -> pd.Series:
    """Return a mask with all entries set to ``True``."""
    return pd.Series([True] * len(df))


class CombineQMixin:
    """Mixin class for combining queries."""

    def __and__(self, other: QTypes) -> AndQ:
        """Combine two queries with a logical AND."""
        return AndQ(self, other)

    def __or__(self, other: QTypes) -> OrQ:
        """Combine two queries with a logical OR."""
        return OrQ(self, other)

    def __invert__(self) -> NotQ:
        """Negate the query."""
        return NotQ(self)


class Q(CombineQMixin):
    """Combinable query object for filtering a DataFrame."""

    _OPERATOR_MAP: dict[str, Callable[[pd.Series, Any], pd.Series]] = {
        "==": lambda series, value: series == value,
        "<": lambda series, value: series < value,
        "<=": lambda series, value: series <= value,
        ">": lambda series, value: series > value,
        ">=": lambda series, value: series >= value,
        "!=": lambda series, value: series != value,  # same as ~Q("col", "==", value)
        "in": lambda series, value: series.isin(value),  # value is a list
    }

    def __init__(
        self,
        column: str,
        operator: Literal["==", "<", "<=", ">", ">=", "!=", "in"],
        value: Any,
    ) -> None:
        """Create query object that can compare a ``column`` with a ``value``."""
        self.colname = column
        self.operator = operator
        self.value = value
        self._column_map = get_default_column_map()

    def __repr__(self) -> str:
        """Return a string representation of the query."""
        return f"Q({self.colname!r}, {self.operator!r}, {self.value!r})"

    def execute(self, df: pd.DataFrame) -> pd.Series:
        """Return a boolean mask where the query is satisfied for ``df``."""
        try:
            colname = self._column_map.from_short[self.colname].long
        except KeyError:
            colname = self.colname

        column = df[colname]

        if callable(self.value):
            return self.value(column)

        return self._OPERATOR_MAP[self.operator](column, self.value)


class AndQ(CombineQMixin):
    """Query object for combining two queries with a logical AND.

    >>> df = pd.DataFrame({'col1': [1, 2, 3]})
    >>> q1 = Q('col1', '>', 1)
    >>> q2 = Q('col1', '<', 3)
    >>> and_q = q1 & q2
    >>> print(and_q)
    Q('col1', '>', 1) & Q('col1', '<', 3)
    >>> isinstance(and_q, AndQ)
    True
    >>> and_q.execute(df)
    0    False
    1     True
    2    False
    Name: col1, dtype: bool
    """

    def __init__(self, q1: QTypes, q2: QTypes) -> None:
        """Combine two queries with a logical AND."""
        self.q1 = q1
        self.q2 = q2

    def __repr__(self) -> str:
        """Return a string representation of the query."""
        return f"{self.q1!r} & {self.q2!r}"

    def execute(self, df: pd.DataFrame) -> pd.Series:
        """Return a boolean mask where both queries are satisfied."""
        return self.q1.execute(df) & self.q2.execute(df)


class OrQ(CombineQMixin):
    """Query object for combining two queries with a logical OR.

    >>> df = pd.DataFrame({'col1': [1, 2, 3]})
    >>> q1 = Q('col1', '==', 1)
    >>> q2 = Q('col1', '==', 3)
    >>> or_q = q1 | q2
    >>> print(or_q)
    Q('col1', '==', 1) | Q('col1', '==', 3)
    >>> isinstance(or_q, OrQ)
    True
    >>> or_q.execute(df)
    0     True
    1    False
    2     True
    Name: col1, dtype: bool
    """

    def __init__(self, q1: QTypes, q2: QTypes) -> None:
        """Combine two queries with a logical OR."""
        self.q1 = q1
        self.q2 = q2

    def __repr__(self) -> str:
        """Return a string representation of the query."""
        return f"{self.q1!r} | {self.q2!r}"

    def execute(self, df: pd.DataFrame) -> pd.Series:
        """Return a boolean mask where either query is satisfied."""
        return self.q1.execute(df) | self.q2.execute(df)


class NotQ(CombineQMixin):
    """Query object for negating a query.

    >>> df = pd.DataFrame({'col1': [1, 2, 3]})
    >>> q = Q('col1', '==', 2)
    >>> not_q = ~q
    >>> print(not_q)
    ~Q('col1', '==', 2)
    >>> isinstance(not_q, NotQ)
    True
    >>> not_q.execute(df)
    0     True
    1    False
    2     True
    Name: col1, dtype: bool
    """

    def __init__(self, q: QTypes) -> None:
        """Negate the given query ``q``."""
        self.q = q

    def __repr__(self) -> str:
        """Return a string representation of the query."""
        return f"~{self.q!r}"

    def execute(self, df: pd.DataFrame) -> pd.Series:
        """Return a boolean mask where the query is not satisfied."""
        return ~self.q.execute(df)


class NoneQ(CombineQMixin):
    """Query object that always returns the entire DataFrame. Useful as default."""

    def __repr__(self) -> str:
        """Return a string representation of the query."""
        return "NoneQ()"

    def execute(self, df: pd.DataFrame) -> pd.Series:
        """Return a boolean mask with all entries set to ``True``."""
        return get_all_true(df)


QTypes = Q | AndQ | OrQ | NotQ | None


@dataclass
class QueryPortion:
    """Dataclass for storing the portion of a query."""

    match: int
    total: int

    def __post_init__(self) -> None:
        """Check that the portion is valid.

        >>> QueryPortion(5, 2)
        Traceback (most recent call last):
            ...
        ValueError: Match must be less than or equal to total.
        """
        if self.total < 0:
            raise ValueError("Total must be non-negative.")
        if self.match < 0:
            raise ValueError("Match must be non-negative.")
        if self.match > self.total:
            raise ValueError("Match must be less than or equal to total.")

    @property
    def fail(self) -> int:
        """Get the number of failures.

        >>> QueryPortion(2, 5).fail
        3
        """
        return self.total - self.match

    @property
    def ratio(self) -> float:
        """Get the ratio of matches over the total.

        >>> QueryPortion(2, 5).ratio
        0.4
        """
        return self.match / self.total

    @property
    def percent(self) -> float:
        """Get the percentage of matches over the total.

        >>> QueryPortion(2, 5).percent
        40.0
        """
        return self.ratio * 100

    def invert(self) -> QueryPortion:
        """Return the inverted portion.

        >>> QueryPortion(2, 5).invert()
        QueryPortion(match=3, total=5)
        """
        return QueryPortion(match=self.fail, total=self.total)


def align_diagnoses(
    dataset: pd.DataFrame,
    modalities: list[str],
) -> list[pd.DataFrame]:
    """Stack aligned diagnosis tables in ``dataset`` for each of ``modalities``."""
    diagnosis_stack = []
    for modality in modalities:
        this = dataset[modality].copy().drop(columns=["info"])

        for i, other in enumerate(diagnosis_stack):
            this, other = this.align(other, join="outer")
            diagnosis_stack[i] = other

        diagnosis_stack.append(this)

    return diagnosis_stack


def create_raising_func(method: str):
    """Raise ValueError for wrong ``method``."""

    def raise_value_err(*args, **kwargs):
        raise ValueError(f"Unknown method {method}")

    return raise_value_err


def false_estimate(
    obs: np.ndarray,
    false_pos_probs: np.ndarray,
    true_neg_probs: np.ndarray,
    method: Literal["prod", "max"],
) -> float:
    """Compute estimate of ``False``, given ``obs``.

    >>> false_estimate([True, False], [0.1, 0.6], [0.4, 0.7], method="whatever")
    Traceback (most recent call last):
        ...
    ValueError: Unknown method whatever
    """
    false_llhs = np.where(obs, false_pos_probs, true_neg_probs)
    nans_masked = np.where(
        pd.isna(obs),
        1.0 if method == "prod" else 0.0,
        false_llhs,
    )
    method = getattr(np, method, create_raising_func(method))
    return method(nans_masked)


def true_estimate(
    obs: np.ndarray,
    true_pos_probs: np.ndarray,
    false_neg_probs: np.ndarray,
    method: Literal["prod", "max"],
) -> float:
    """Compute estimate of ``True``, given ``obs``.

    >>> obs = [True, False, np.nan]
    >>> true_pos_probs = [0.8, 0.6, 0.9]
    >>> false_neg_probs = [0.6, 0.7, 0.9]
    >>> true_estimate(obs, true_pos_probs, false_neg_probs, method="max")
    np.float64(0.8)
    >>> tmp = true_estimate(obs, true_pos_probs, false_neg_probs, method="prod")
    >>> np.isclose(tmp, 0.56)
    np.True_
    """
    true_llhs = np.where(obs, true_pos_probs, false_neg_probs)
    nans_masked = np.where(
        pd.isna(obs),
        1.0 if method == "prod" else 0.0,
        true_llhs,
    )
    method = getattr(np, method, create_raising_func(method))
    return method(nans_masked)


def max_likelihood(
    obs: np.ndarray,
    specificities: np.ndarray,
    sensitivities: np.ndarray,
) -> bool:
    """Compute most likely true state based on all ``obs``.

    >>> obs = np.array([True, False, np.nan, None])
    >>> sensitivities = np.array([0.9, 0.7, 0.7, 0.7])
    >>> specificities = np.array([0.9, 0.7, 0.7, 0.7])
    >>> max_likelihood(obs, sensitivities, specificities)
    np.True_
    >>> obs = np.array([True, False, False, False])
    >>> max_likelihood(obs, sensitivities, specificities)
    np.False_
    """
    healthy_llh = false_estimate(obs, 1 - specificities, specificities, method="prod")
    involved_llhs = true_estimate(obs, sensitivities, 1 - sensitivities, method="prod")
    return healthy_llh < involved_llhs


def rank_trustworthy(
    obs: np.ndarray,
    specificities: np.ndarray,
    sensitivities: np.ndarray,
) -> bool:
    """Estimate true state based on most trustworthy value in ``obs``.

    >>> obs = np.array([True, False, np.nan, None])
    >>> sensitivities = np.array([0.9, 0.7, 0.7, 0.7])
    >>> specificities = np.array([0.9, 0.7, 0.7, 0.7])
    >>> rank_trustworthy(obs, sensitivities, specificities)
    np.True_
    >>> obs = np.array([True, False, False, False])
    >>> rank_trustworthy(obs, sensitivities, specificities)
    np.True_
    """
    healthy_llh = false_estimate(obs, 1 - specificities, specificities, method="max")
    involved_llhs = true_estimate(obs, sensitivities, 1 - sensitivities, method="max")
    return healthy_llh < involved_llhs


def expand_mapping(
    short_map: dict[str, Any],
    colname_map: dict[str | tuple[str, str, str], Any] | None = None,
) -> dict[tuple[str, str, str], Any]:
    """Expand the column map to full column names.

    >>> expand_mapping({'age': 'foo', 'hpv': 'bar'})
    {('patient', '#', 'age'): 'foo', ('patient', '#', 'hpv_status'): 'bar'}
    """
    colname_map = colname_map or get_default_column_map().from_short
    expanded_map = {}

    for colname, func in short_map.items():
        expanded_colname = getattr(colname_map.get(colname), "long", colname)
        expanded_map[expanded_colname] = func

    return expanded_map


AggFuncType = dict[str | tuple[str, str, str], Callable[[pd.Series], pd.Series]]


@pd_ext.register_dataframe_accessor("ly")
class LyDataAccessor:
    """Custom accessor for handling lymphatic involvement data."""

    def __init__(self, obj: pd.DataFrame) -> None:
        """Initialize the accessor with a DataFrame."""
        self._obj = obj
        self._column_map = get_default_column_map()

    def __contains__(self, key: str) -> bool:
        """Check if a column is contained in the DataFrame.

        >>> df = pd.DataFrame({("patient", "#", "age"): [61, 52, 73]})
        >>> "age" in df.ly
        True
        >>> "foo" in df.ly
        False
        >>> ("patient", "#", "age") in df.ly
        True
        """
        key = self._get_safe_long(key)
        return key in self._obj

    def __getitem__(self, key: str) -> pd.Series:
        """Allow column access by short name, too."""
        key = self._get_safe_long(key)
        return self._obj[key]

    def __getattr__(self, name: str) -> Any:
        """Access columns also by short name.

        >>> df = pd.DataFrame({("patient", "#", "age"): [61, 52, 73]})
        >>> df.ly.age
        0    61
        1    52
        2    73
        Name: (patient, #, age), dtype: int64
        >>> df.ly.foo
        Traceback (most recent call last):
            ...
        AttributeError: Attribute 'foo' not found.
        """
        try:
            return self[name]
        except KeyError as key_err:
            raise AttributeError(f"Attribute {name!r} not found.") from key_err

    def _get_safe_long(self, key: Any) -> tuple[str, str, str]:
        """Get the long column name or return the input."""
        return getattr(self._column_map.from_short.get(key), "long", key)

    def validate(self, modalities: list[str] | None = None) -> pd.DataFrame:
        """Validate the DataFrame against the lydata schema."""
        modalities = modalities or list(get_default_modalities().keys())
        lydata_schema = construct_schema(modalities=modalities)
        return lydata_schema.validate(self._obj)

    def query(self, query: QTypes = None) -> pd.DataFrame:
        """Return a DataFrame with rows that satisfy the ``query``."""
        mask = (query or NoneQ()).execute(self._obj)
        return self._obj[mask]

    def portion(self, query: QTypes = None, given: QTypes = None) -> QueryPortion:
        """Compute how many rows satisfy a ``query``, ``given`` some other conditions.

        >>> df = pd.DataFrame({'x': [1, 2, 3]})
        >>> df.ly.portion(query=Q('x', '==', 2), given=Q('x', '>', 1))
        QueryPortion(match=np.int64(1), total=np.int64(2))
        >>> df.ly.portion(query=Q('x', '==', 2), given=Q('x', '>', 3))
        QueryPortion(match=np.int64(0), total=np.int64(0))
        """
        given_mask = (given or NoneQ()).execute(self._obj)
        query_mask = (query or NoneQ()).execute(self._obj)

        return QueryPortion(
            match=query_mask[given_mask].sum(),
            total=given_mask.sum(),
        )

    def stats(
        self,
        agg_funcs: AggFuncType | None = None,
        use_shortnames: bool = True,
        out_format: str = "dict",
    ) -> Any:
        """Compute statistics.

        >>> df = pd.DataFrame({
        ...     ('patient', '#', 'age'): [61, 52, 73, 61],
        ...     ('patient', '#', 'hpv_status'): [True, False, None, True],
        ...     ('tumor', '1', 't_stage'): [2, 3, 1, 2],
        ... })
        >>> df.ly.stats()   # doctest: +NORMALIZE_WHITESPACE
        {'age': {61: 2, 52: 1, 73: 1},
         'hpv': {True: 2, False: 1, None: 1},
         't_stage': {2: 2, 3: 1, 1: 1}}
        """
        _agg_funcs = self._column_map.from_short.copy()
        _agg_funcs.update(agg_funcs or {})
        stats = {}

        for colname, func in _agg_funcs.items():
            if colname not in self:
                continue

            column = self[colname]
            if use_shortnames and colname in self._column_map.from_long:
                colname = self._column_map.from_long[colname].short

            stats[colname] = getattr(func(column), f"to_{out_format}")()

        return stats

    def combine(
        self,
        modalities: list[ModalityConfig] | None = None,
        method: Literal["max_llh", "rank"] = "max_llh",
    ) -> pd.DataFrame:
        """Combine diagnoses of ``modalities`` using ``method``."""
        modalities = modalities or list(get_default_modalities().values())
        modality_names = list(get_default_modalities().keys())
        diagnosis_stack = align_diagnoses(self._obj, modality_names)
        columns = diagnosis_stack[0].columns
        diagnosis_stack = np.array([diagnosis_stack])

        funcs1d = {"max_llh": max_likelihood, "rank": rank_trustworthy}
        result = np.apply_along_axis(
            func1d=funcs1d[method],
            axis=0,
            arr=diagnosis_stack,
            sensitivities=np.array([mod.sens for mod in modalities]),
            specificities=np.array([mod.spec for mod in modalities]),
        )
        return pd.DataFrame(result, columns=columns)


def main() -> None:
    """Run main function."""
    ...


if __name__ == "__main__":
    main()

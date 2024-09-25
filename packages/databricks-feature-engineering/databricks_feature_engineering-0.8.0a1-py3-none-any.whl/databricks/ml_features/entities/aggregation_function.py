from abc import abstractmethod

from databricks.ml_features_common.entities._feature_store_object import (
    _FeatureStoreObject,
)


class AggregationFunction(_FeatureStoreObject):
    """Abstract base class for all aggregation functions."""

    @abstractmethod
    def to_sql(self, column_name) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the aggregation function."""
        pass


class Avg(AggregationFunction):
    """Class representing the average (avg) aggregation function."""

    def to_sql(self, column_name) -> str:
        return f"AVG({column_name})"

    @property
    def name(self) -> str:
        return "avg"


class Count(AggregationFunction):
    """Class representing the count aggregation function."""

    def to_sql(self, column_name) -> str:
        return f"COUNT({column_name})"

    @property
    def name(self) -> str:
        return "count"


class ApproxCountDistinct(AggregationFunction):
    """
    Class representing the approximate count distinct aggregation function.
    See https://docs.databricks.com/en/sql/language-manual/functions/approx_count_distinct.html

    :param relativeSD: The relative standard deviation allowed in the approximation.
    """

    def __init__(self, relativeSD: float):
        self._relativeSD = relativeSD

    @property
    def name(self) -> str:
        return "approx_count_distinct"

    @property
    def relativeSD(self) -> float:
        return self._relativeSD

    def to_sql(self, column_name) -> str:
        raise NotImplementedError(
            "ApproxCountDistinct is not a supported aggregation function."
        )


class PercentileApprox(AggregationFunction):
    """
    Class representing the percentile approximation aggregation function.
    See https://docs.databricks.com/en/sql/language-manual/functions/approx_percentile.html

    :param percentile: The percentile to approximate.
    :param accuracy: The accuracy of the approximation.
    """

    def __init__(self, percentile: float, accuracy: int):
        self._percentile = percentile
        self._accuracy = accuracy

    @property
    def name(self) -> str:
        return "percentile_approx"

    @property
    def percentile(self) -> float:
        return self._percentile

    @property
    def accuracy(self) -> int:
        return self._accuracy

    def to_sql(self, column_name) -> str:
        raise NotImplementedError(
            "PercentileApprox is not a supported aggregation function."
        )


class First(AggregationFunction):
    """Class representing the first aggregation function."""

    def to_sql(self, column_name) -> str:
        raise NotImplementedError("First is not a supported aggregation function.")

    @property
    def name(self) -> str:
        return "first"


class Last(AggregationFunction):
    """Class representing the last aggregation function."""

    def to_sql(self, column_name) -> str:
        raise NotImplementedError("Last is not a supported aggregation function.")

    @property
    def name(self) -> str:
        return "last"


class Max(AggregationFunction):
    """Class representing the maximum (max) aggregation function."""

    def to_sql(self, column_name) -> str:
        return f"MAX({column_name})"

    @property
    def name(self) -> str:
        return "max"


class Min(AggregationFunction):
    """Class representing the minimum (min) aggregation function."""

    def to_sql(self, column_name) -> str:
        return f"MIN({column_name})"

    @property
    def name(self) -> str:
        return "min"


class StddevPop(AggregationFunction):
    """Class representing the population standard deviation (stddev_pop) aggregation function."""

    def to_sql(self, column_name) -> str:
        raise NotImplementedError("StddevPop is not a supported aggregation function.")

    @property
    def name(self) -> str:
        return "stddev_pop"


class StddevSamp(AggregationFunction):
    """Class representing the sample standard deviation (stddev_samp) aggregation function."""

    def to_sql(self, column_name) -> str:
        raise NotImplementedError("StddevSamp is not a supported aggregation function.")

    @property
    def name(self) -> str:
        return "stddev_samp"


class Sum(AggregationFunction):
    """Class representing the sum aggregation function."""

    def to_sql(self, column_name) -> str:
        return f"SUM({column_name})"

    @property
    def name(self) -> str:
        return "sum"


class VarPop(AggregationFunction):
    """Class representing the population variance (var_pop) aggregation function."""

    def to_sql(self, column_name) -> str:
        raise NotImplementedError("VarPop is not a supported aggregation function.")

    @property
    def name(self) -> str:
        return "var_pop"


class VarSamp(AggregationFunction):
    """Class representing the sample variance (var_samp) aggregation function."""

    def to_sql(self, column_name) -> str:
        raise NotImplementedError("VarSamp is not a supported aggregation function.")

    @property
    def name(self) -> str:
        return "var_samp"


# Mapping from shorthand strings to instances of corresponding classes
AGGREGATION_FUNCTION_BY_SHORTHAND = {
    "mean": Avg(),
    "avg": Avg(),
    "count": Count(),
    "first": First(),
    "last": Last(),
    "max": Max(),
    "min": Min(),
    "stddev_pop": StddevPop(),
    "stddev_samp": StddevSamp(),
    "sum": Sum(),
    "var_pop": VarPop(),
    "var_samp": VarSamp(),
}

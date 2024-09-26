"""Removing touches with simple rules."""

import fnmatch
import itertools
import logging
from typing import Iterable, Iterator, List, Tuple

import numpy as np

from ..property import MTypeValidator, Property, PropertyGroup

# dendrite mapping here is for historical purposes only, when we
# distinguished only between soma and !soma.
BRANCH_TYPES = {
    "*": [0, 1, 2, 3],
    "soma": [0],
    "axon": [1],
    "dendrite": [2, 3],
    "basal": [2],
    "apical": [3],
}


logger = logging.getLogger(__name__)


class TouchRule(Property):
    """Class representing a Touch rule."""

    _name = "touchRule"

    _attributes = {
        "fromMType": "*",
        "fromBranchType": "*",
        "fromLayer": "*",
        "toMType": "*",
        "toBranchType": "*",
        "toLayer": "*",
    }

    _attribute_alias = {"type": "toBranchType"}

    def __init__(self, *args, **kwargs):
        """Create a new touch rule.

        Enforces that the deprecated attributes `fromLayer` and `toLayer` are set to
        ``*``, and raises a `ValueError` if not.
        """
        super().__init__(*args, **kwargs)
        if self.fromLayer != "*":
            raise ValueError("fromLayer is deprecated and needs to be '*'")
        if self.toLayer != "*":
            raise ValueError("toLayer is deprecated and needs to be '*'")

    def __call__(
        self, src_mtypes: Iterable[str], dst_mtypes: Iterable[str]
    ) -> Iterator[Tuple[str, str, str, str]]:
        """Expands the rule for the given mtypes.

        Will yield one tuple for every possible combination, containing:

        * source mtype
        * target mtype
        * source branch types allowed
        * target branch types allowed
        """
        for src, dst in itertools.product(
            fnmatch.filter(src_mtypes, self.fromMType),
            fnmatch.filter(dst_mtypes, self.toMType),
        ):
            yield (src, dst, self.fromBranchType, self.toBranchType)


class TouchRules(PropertyGroup, MTypeValidator):
    """A collection of `TouchRule` elements."""

    _kind = TouchRule

    def to_matrix(self, src_mtypes: List[str], dst_mtypes: List[str]) -> np.array:
        """Construct a touch rule matrix.

        Args:
            src_mtypes: The morphology types associated with the source population
            dst_mtypes: The morphology types associated with the target population
        Returns:
            A multidimensional matrix, containing a one (1) for every
            connection allowed. The dimensions correspond to the numeical
            indices of morphology types of source and destination, as well
            as the rule type.
        """
        src_mtype_rev = {name: i for i, name in enumerate(src_mtypes)}
        dst_mtype_rev = {name: i for i, name in enumerate(dst_mtypes)}

        ntypes = max(len(v) for v in BRANCH_TYPES.values())

        matrix = np.zeros(
            shape=(len(src_mtype_rev), len(dst_mtype_rev), ntypes, ntypes),
            dtype="uint8",
        )

        for r in self:
            for src_mt, dst_mt, src_bt, dst_bt in r(src_mtypes, dst_mtypes):
                for i in BRANCH_TYPES[src_bt]:
                    for j in BRANCH_TYPES[dst_bt]:
                        matrix[src_mtype_rev[src_mt], dst_mtype_rev[dst_mt], i, j] = 1

        return matrix

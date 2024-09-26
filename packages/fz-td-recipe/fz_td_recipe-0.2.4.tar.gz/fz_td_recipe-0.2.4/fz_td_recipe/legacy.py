"""Top-level interface for legacy XML recipe handling."""

import logging
import textwrap
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, TextIO

from . import utils
from .parts.bouton_density import InitialBoutonDistance
from .parts.gap_junction_properties import GapJunctionProperties
from .parts.seeds import Seeds
from .parts.spine_lengths import SpineLengths
from .parts.structure import InterBoutonInterval, StructuralSpineLengths
from .parts.synapse_properties import SynapseProperties
from .parts.synapse_reposition import SynapseShifts
from .parts.touch_connections import ConnectionRules
from .parts.touch_reduction import TouchReduction
from .parts.touch_rules import TouchRules
from .property import NotFound

logger = logging.getLogger(__name__)


class XMLRecipe:
    """Recipe information used for functionalizing circuits.

    Instances of this class can be used to parse the XML description of our
    brain circuits, passed in via the parameter `path`.
    All parts of the recipe present are extracted and can be accessed via
    attributes, where optional parts may be set to ``None``.

    Args:
        path: path to an XML file to extract the recipe from
        strict: will raise when additional attributes are encountered, on by default
    """

    bouton_interval: InterBoutonInterval
    """The interval parametrization specifying how touches should be
    distributed where cell morphologies overlap.
    """

    bouton_distances: Optional[InitialBoutonDistance] = None
    """Optional definition of the bouton distances from the soma."""

    connection_rules: Optional[ConnectionRules] = None
    """Optional parameters for the connectivity reduction."""

    gap_junction_properties: Optional[GapJunctionProperties] = None
    """Optional definition of attributes for gap junctions."""

    touch_reduction: Optional[TouchReduction] = None
    """Optional parameter for a simple trimming of touches with a survival
    probability."""

    touch_rules: TouchRules
    """Detailed definition of allowed synapses. All touches not matching
    the definitions here will be removed."""

    seeds: Seeds
    """Seeds to use when generating random numbers during the touch
    reduction stage."""

    spine_lengths: SpineLengths
    """Defines percentiles for the length of spines of synapses, i.e., the
    distance between the surface positions of touches."""

    structural_spine_lengths: StructuralSpineLengths
    """Defines the maximum length of spines used by TouchDetector."""

    synapse_properties: SynapseProperties
    """Classifies synapses and assigns parameters for the physical
    properties of the synapses."""

    synapse_reposition: SynapseShifts
    """Definition of re-assignment of somatic synapses to the first axon
    segment."""

    def __init__(self, path: Path, strict: bool = True):
        """Create a new instance from `path`."""
        xml = utils.load_xml(path)
        for name, kind in self.__annotations__.items():  # pylint: disable=no-member
            try:
                if not hasattr(kind, "load"):
                    (kind,) = [cls for cls in kind.__args__ if cls != type(None)]  # noqa
                setattr(self, name, kind.load(xml, strict=strict))
            except NotFound as e:
                logger.warning("missing recipe part: %s", e)

    def validate(self, values: Dict[str, List[str]]) -> bool:
        """Validate basic functionality of the recipe.

        Checks provided here-in test for basic coverage, and provides a
        weak assertion that the recipe should be functional.

        The parameter `values` should be a dictionary containing all
        allowed values in the form ``fromMType``
        """

        def _inner():
            for name in self.__annotations__:  # pylint: disable=no-member
                attr = getattr(self, name, None)
                if attr and not attr.validate(values):
                    yield False
                yield True

        return all(_inner())

    def dump(self, fd: TextIO, connectivity_fd: Optional[TextIO] = None):
        """Write the recipe to the provided file descriptors.

        If `connectivity_fd` is given, the connection rules of the recipe
        are written to it, otherwise dump the whole recipe to `fd`.
        """
        contents = []
        header = ""
        for name in self.__annotations__:  # pylint: disable=no-member
            if not (hasattr(self, name) and getattr(self, name)):
                continue
            text = str(getattr(self, name))
            if len(text) == 0:
                # the attribute may be present, but defaulted. In this case `text` is
                # going to be empty, and will result in spurious newlines we want to
                # avoid.
                continue
            if name == "connection_rules" and connectivity_fd:
                connectivity_fd.write(text)
                contents.append("&connectivity;")
                header = _CONNECTIVITY_DECLARATION.format(
                    getattr(connectivity_fd, "name", "UNKNOWN")
                )
            else:
                contents.append(text)
        inner = textwrap.indent("\n".join(contents), "  ")
        if inner:
            inner = "\n" + inner
        fd.write(_RECIPE_SKELETON.format(header, inner))

    def __str__(self) -> str:
        """Converts the recipe into XML."""
        output = StringIO()
        self.dump(output)
        return output.getvalue()


_RECIPE_SKELETON = """\
<?xml version="1.0"?>{}
<blueColumn>{}
</blueColumn>
"""

_CONNECTIVITY_DECLARATION = """
<!DOCTYPE blueColumn [
  <!ENTITY connectivity SYSTEM "{}">
]>\
"""

"""Read and modify HPC circuit building recipes.

This module provides the :class:`XMLRecipe` class to handle recipe reading and writing.  A
short example to read a recipe and modify the initial bouton distance for inhibitory
synapses:

>>> from fz_td_recipe import XMLRecipe
>>> r = XMLRecipe("tests/data/v7.xml")
>>> print(r.bouton_distances)
<InitialBoutonDistance inhibitorySynapsesDistance="5.0" excitatorySynapsesDistance="25.0" />
>>> r.bouton_distances.inhibitorySynapsesDistance = 4.5

To write the recipe into a single file, containing all parts:

>>> with open("one_file.xml", "w") as fd:
...     r.dump(fd)

And to produce a "classical" split, where the connectivity part of the
recipe is written to a different file:

>>> with open("recipe.xml", "w") as f1, open("connectivitiy.xml", "w") as f2:
...     r.dump(f1, connectivity_fd=f2)
"""

from .legacy import XMLRecipe
from .recipe import Recipe

__all__ = ["Recipe", "XMLRecipe"]

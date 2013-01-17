
__author__     = "Alexander Urban"
__version__    = "0.1"

import numpy as np

from pymatgen.core.structure                     import Structure
from pymatgen.core.sites                         import PeriodicSite
from pymatgen.transformations.transformation_abc import AbstractTransformation

class RandomOrderingTransformation(AbstractTransformation):
    """
    Generate one particular random ordering for a statistically 
    decorated lattice.
    """

    def apply_transformation(self, structure):
        
        natoms = int(structure.composition.num_atoms)
        elems  = structure.composition.elements
        
        natoms_of_elem = {}
        natoms_of_elem_placed = {}
        for el in elems:
            frac = structure.composition.get_atomic_fraction(el)
            natoms_of_elem[el] = int(frac*natoms)
            natoms_of_elem_placed[el] = 0
        
        # the individual atom counts must sum up to
        # the total number of atoms
        assert np.sum(natoms_of_elem.values()) == natoms

        new_sites = []
        for site in structure.sites:
            species = p = []
            # assign each possible element a probability
            for el in site.keys():
                if (natoms_of_elem_placed[el] < natoms_of_elem[el]):
                    species.append(el)
                    p.append(site[el]+np.sum(p))
            # convert to NumPy array for slicing
            species = np.array(species)
            # draw a random number r in [0,1]
            r = np.random.random()*p[-1]
            # select the corresponding element
            el = species[p >= r][0]
            new_sites.append(PeriodicSite(el.symbol, site.frac_coords, site.lattice))
            natoms_of_elem_placed[el] += 1

        # return new Structure() based on the random site decorations
        new_structure = Structure.from_sites(new_sites)
        return new_structure

    @property
    def inverse(self):
        return None

    @property
    def is_one_to_many(self):
        return True

    @property
    def to_dict(self):
        return {"name": self.__class__.__name__, "version": __version__,
                "init_args": {"algo": self._algo},
                "@module": self.__class__.__module__,
                "@class": self.__class__.__name__}


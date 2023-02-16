========================================================================
           Dribble - Monte Carlo Percolation Simulations
========================================================================

What is Dribble?
----------------

The *Dribble* package implements a lattice-model Monte-Carlo method for 
simulating ionic transport properties in atomic structures.  In
essence, *Dribble* solves the *site percolation* problem of `percolation
theory`_ for a given set of *percolation rules*.  These rules can be
quite complex and reflect the physical interactions of the percolating
species with other atomic species in the structure.

For more information about the method and for applications see:

A.\  Urban, "Modeling ionic transport and disorder in crystalline electrodes using percolation theory" *arXiv* (2023) 2302.06759 (https://doi.org/10.48550/arXiv.2302.06759) |br|

A. Urban, J. Lee, and G. Ceder,
*Adv. Energy Mater.* **4** (2014) 1400478 (https://doi.org/10.1002/aenm.201400478). |br|
J. Lee, A. Urban, X. Li, D. Su, G. Hautier, and G. Ceder,
*Science* **343** (2014) 519-522 (https://doi.org/10.1126/science.1246432 ). |br|
G. S. Gautam, P. Canepa, A. Urban, S.-H. Bo, G. Ceder, *Chem. Mater.* **29** (2017) 7918-7930 (https://doi.org/10.1021/acs.chemmater.7b02820). |br| 
B. Ouyang†, N. Artrith†, Z. Lun†, Z. Jadidi, D. A. Kitchaev, H. Ji, A. Urban, G. Ceder,
*Adv. Energy Mater.* **10** (2020) 1903240 (https://doi.org/10.1002/aenm.201903240). 

.. _`percolation theory`: https://en.wikipedia.org/wiki/Percolation_theory
.. |br| raw:: html

   <br />


Installation
------------

To use ``pip`` to install *Dribble*,
run the following command inside the ``dribble`` directory:

::

  pip install .

or to install in "editable" mode, use

::

  pip install -e .


Examples
--------

See the `examples`_ directory for a number of Jupyter notebooks 
explaining different aspects of simulations with Dribble.

.. _`examples`: ./examples/


Dribble package
---------------

The two main object classes needed for most applications are ``Lattice``
and ``Percolator``.  The ``Lattice`` class holds the lattice that the
simulation is run on, and the ``Percolator`` class implements the
percolation Monte Carlo algorithm.  For the sake of convenience, a third
class, ``Input``, is provided to parse input files in the JSON_ format.
Provided an input file ``parameters.json``, a minimal example of a
percolation simulation is:

.. code:: python

   from dribble.io import Input
   from dribble.lattice import Lattice
   from dribble.percolator import Percolator

   inp = Input.from_file('parameters.json')
   lat = Lattice.from_input_object(inp)
   percol = Percolator.from_input_object(inp, lattice)

   percol.percolation_point(inp.flip_sequence)


.. _JSON: http://www.json.org

Here an example input file:

.. code:: json

   {
       "structure": "POSCAR",
       "formula_units": 240,
       "sublattices": {
           "oct": {
               "description": "octahedral site",
               "sites": {"species": ["Li", "Mn", "Nb"]}
           },
           "oxygen": {
               "description": "oxygen sites",
               "sites": {"species": ["O"]},
               "ignore": true
           }
       },
       "bonds": [
           {
               "sublattices": ["oct", "oct"],
               "bond_rules": [
                   ["MinCommonNNNeighborsBR", {"num_neighbors": 2}]
               ]
           }
       ],
       "percolating_species": ["Li"]
   }


Here, ``POSCAR`` is an atomic structure file in the VASP format.


Command line tool
-----------------

Along with the python package, a command line tool also named
``dribble`` is installed.

Display usage information with the ``--help`` flag::

   usage: dribble [-h] [--supercell SUPERCELL SUPERCELL SUPERCELL]
                  [--inaccessible SPECIES] [--pc] [--check] [--pinf] [--pwrap]
                  [--samples SAMPLES] [--file-name FILE_NAME] [--save-clusters]
                  [--save-raw] [--debug]
                  input_file [structure_file]

   Dribble - Percolation Simulation on Lattices

   Analyze the ionic percolation properties of an input structure.

   positional arguments:
     input_file            Input file in JSON format
     structure_file        Input file in JSON format

   optional arguments:
     -h, --help            show this help message and exit
     --supercell SUPERCELL SUPERCELL SUPERCELL
                           List of multiples of the lattice cell in the three
                           lattice directions
     --inaccessible SPECIES, -i SPECIES
                           Calculate fraction of inaccessible sites for given
                           reference species
     --pc, -p              Calculate critical site concentrations
     --check               Check, if the initial structure is percolating.
     --pinf, -s            Estimate P_infinity and percolation susceptibility
     --pwrap, -w           Estimate P_wrap(p)
     --samples SAMPLES     number of samples to be averaged
     --file-name FILE_NAME
                           base file name for all output files
     --save-clusters       save wrapping clusters to file
     --save-raw            Also store raw data before convolution (where
                           available).
     --debug               run in debugging mode

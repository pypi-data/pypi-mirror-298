"""wrapper classes for ASE calculators and algorithms"""
import numpy
import matplotlib.pyplot as plt
import ase
from ase.utils import IOContext
from ase.build import minimize_rotation_and_translation
from ase.geometry.analysis import Analysis
from ase.eos import EquationOfState
from ase.dft.dos import DOS
from virtmat.language.utilities.errors import RuntimeValueError


class RMSD(IOContext):  # not covered
    """A wrapper algorithm to calculate root mean square deviation"""
    results = None

    def __init__(self, atoms):
        self.atoms_list = [atoms] if isinstance(atoms, ase.Atoms) else atoms

    def run(self, reference, adjust=True):
        """Calculate the root mean square deviation (RMSD) between a structure
           and a reference"""
        assert len(reference) == 1
        rmsd = []
        for atoms in self.atoms_list:
            ref_atoms = reference.to_ase()[0]
            if adjust:
                minimize_rotation_and_translation(ref_atoms, atoms)
            rmsd.append(numpy.sqrt(numpy.mean((numpy.linalg.norm(atoms.get_positions()
                                   - ref_atoms.get_positions(), axis=1))**2, axis=0)))
        self.results = {'rmsd': numpy.mean(rmsd), 'output_structure': self.atoms_list}
        return True


class RDF(IOContext):
    """A wrapper algorithm to calculate radial distribution function"""
    results = None

    def __init__(self, atoms):
        self.atoms_list = [atoms] if isinstance(atoms, ase.Atoms) else atoms
        if any(sum(sum(a.cell)) == 0 for a in self.atoms_list):  # not covered
            msg = 'the structure cell must have at least one non-zero vector'
            raise RuntimeValueError(msg)

    def run(self, rmax=None, nbins=40, neighborlist=None, neighborlist_pars=None,
            elements=None):
        """Calculate the radial distribution function for a structure"""
        neighborlist_pars = neighborlist_pars or {}
        analysis = Analysis(self.atoms_list, neighborlist, **neighborlist_pars)
        rmax = rmax or 0.49*max(max(a.cell.lengths()) for a in self.atoms_list)
        ret = analysis.get_rdf(rmax, nbins, elements=elements, return_dists=True)
        self.results = {'rdf': numpy.mean([a for a, b in ret], axis=0),
                        'rdf_distance': numpy.mean([b for a, b in ret], axis=0)}
        return True


class EOS(IOContext):
    """A wrapper algorithm to fit the equation of state"""
    results = None

    def __init__(self, configs):
        assert isinstance(configs, list)
        self.volumes = [a.get_volume() for a in configs]

    def run(self, energies, eos='sjeos', filename=None):
        """v0: optimal volume, e0: minimum energy, B: bulk modulus"""
        obj = EquationOfState(self.volumes, energies, eos=eos)
        keys = ('minimum_energy', 'optimal_volume', 'bulk_modulus', 'eos_volume',
                'eos_energy')
        self.results = dict(zip(keys, obj.getplotdata()[1:7]))
        obj.plot(filename)
        plt.close()
        return True


class DensityOfStates(IOContext):
    """A wrapper algorithm to calculate the density of states"""
    results = None

    def __init__(self, atoms):
        atoms.get_potential_energy()
        self.calc = atoms.calc

    def run(self, width=0.1, window=None, npts=401, spin=None):
        """add density of states and sampling energy points to results"""
        window = window if window is None else tuple(window.tolist())
        obj = DOS(self.calc, width=width, window=window, npts=npts)
        self.results = {'dos_energy': obj.get_energies(), 'dos': obj.get_dos(spin=spin)}
        return True


class BandStructure(IOContext):
    """A wrapper algorithm to calculate the band structure"""
    results = None

    def __init__(self, atoms):
        atoms.get_potential_energy()
        self.calc = atoms.calc

    def run(self, **kwargs):
        """add band structure path, energies, reference to results"""
        obj = self.calc.band_structure()
        keys = ('path', 'energies', 'reference')
        self.results = {'band_structure': {k: getattr(obj, k) for k in keys}}
        if kwargs.get('filename'):
            obj.plot(**kwargs)
            plt.close()
        return True

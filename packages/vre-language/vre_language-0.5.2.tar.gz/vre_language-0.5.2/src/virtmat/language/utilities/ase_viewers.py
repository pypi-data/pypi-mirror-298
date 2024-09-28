"""various viewer functions for ASE"""
import pandas
from ase.eos import EquationOfState
from ase.spectrum.band_structure import BandStructure
from ase.dft.kpoints import BandPath
from ase import visualize


def display_amml_structure(obj, show=True):
    """display an atomic structure using ASE"""
    if show:
        visualize.view(obj.params[0].value.to_ase())


def display_bs(obj, show=True):
    """display a band structure using ASE"""
    assert issubclass(obj.params[0].type_, pandas.DataFrame)
    assert isinstance(obj.params[0].value, pandas.DataFrame)
    bs_dct = dict(next(obj.params[0].value.iterrows())[1])
    bs_dct['energies'] = bs_dct['energies'].to('eV').magnitude
    bs_dct['reference'] = bs_dct['reference'].to('eV').magnitude
    bp_dct = bs_dct['band_path']
    bp_dct = dict(next(bp_dct.iterrows())[1])
    sp_dct = bp_dct['special_points']
    sp_dct = dict(next(sp_dct.iterrows())[1])
    sp_dct = {k: v.to('angstrom**-1').magnitude for k, v in sp_dct.items()}
    bp_dct['special_points'] = sp_dct
    bp_dct['cell'] = bp_dct['cell'].to('angstrom').magnitude
    bp_dct['kpts'] = bp_dct['kpts'].to('angstrom**-1').magnitude
    band_path = BandPath(**bp_dct)
    bs = BandStructure(band_path, bs_dct['energies'], bs_dct['reference'])
    plt_kwargs = {}
    if len(obj.params) > 1:
        assert issubclass(obj.params[1].type_, pandas.DataFrame)
        assert isinstance(obj.params[1].value, pandas.DataFrame)
        plt_dct = dict(next(obj.params[1].value.iterrows())[1])
        if 'emin' in plt_dct:
            plt_kwargs['emin'] = plt_dct['emin'].to('eV').magnitude
        if 'emax' in plt_dct:
            plt_kwargs['emax'] = plt_dct['emax'].to('eV').magnitude
    bs.plot(show=show, **plt_kwargs)


def display_eos(obj, show=True):
    """display fit to equation of state"""
    volumes = obj.params[0].value
    energies = obj.params[1].value
    eos_kwargs = {}
    if len(obj.params) == 3:
        eos_kwargs['eos'] = obj.params[2].value
    eos_obj = EquationOfState(volumes, energies, **eos_kwargs)
    eos_obj.plot(show=show)

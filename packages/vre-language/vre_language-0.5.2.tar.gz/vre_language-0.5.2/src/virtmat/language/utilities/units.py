"""
pint units registry, utility functions for the pint package
"""
from math import floor, ceil
import pint
import pandas
import pint_pandas
from virtmat.language.utilities.errors import StaticValueError, RuntimeTypeError

ureg = pint.UnitRegistry()
ureg.autoconvert_offset_to_baseunit = True
# ureg.setup_matplotlib(True)
# ureg.mpl_formatter = '[{:~P}]'
pint.set_application_registry(ureg)


def get_units(val):
    """extract the unit from pint Quantity or pandas Series"""
    if isinstance(val, ureg.Quantity):
        return val.units
    if isinstance(val.dtype, pint_pandas.PintType):
        return val.dtype.units
    if val.dtype == 'object':
        units = set(v.units for v in val)
        assert len(units) == 1
        return next(iter(units))
    raise RuntimeTypeError(f'unsupported dtype: {val.dtype}')


def get_dimensionality(val):
    """evaluate the dimensionality of pint Quantity or pandas Series"""
    if isinstance(val, ureg.Quantity):
        return val.dimensionality
    if isinstance(val.dtype, pint_pandas.PintType):
        return val.pint.dimensionality
    if val.dtype == 'object':
        dim = set(v.dimensionality for v in val)
        assert len(dim) == 1
        return next(iter(dim))
    raise RuntimeTypeError(f'unsupported dtype: {val.dtype}')


def get_df_units(df):
    """extract a tuple of units frompandas DataFrame"""
    tuple_0 = tuple(next(df.iloc[[0]].itertuples(index=False, name=None)))
    return tuple(getattr(t, 'units', None) for t in tuple_0)


def convert_df_units(df, units):
    """convert units of dataframe columns of numeric dtype"""
    columns = []
    if any(not isinstance(u, (str, type(None))) for u in units):
        w_type = next(u for u in units if not isinstance(u, (str, type(None))))
        raise RuntimeTypeError(f'unsupported dtype: {w_type}')
    for col, unit in zip(df.columns, units):
        if unit:
            if isinstance(df[col].dtype, pint_pandas.PintType):
                columns.append(df[col].pint.to(unit))
            elif df[col].dtype == 'object':
                columns.append(df[col].apply(lambda x, u=unit: x.to(u)))
            else:
                raise RuntimeTypeError(f'unsupported dtype: {df[col].dtype}')
        else:
            columns.append(df[col])
    return pandas.concat(columns, axis='columns')


def strip_units(val):
    """return the magnitude for quantity objects"""
    if isinstance(val, ureg.Quantity):
        return val.magnitude
    return val


def get_pint_series(ser):
    """convert dtype of numeric series from object to PintType"""
    assert isinstance(ser, pandas.Series)
    if (isinstance(ser.dtype, pint_pandas.PintType) or len(ser) == 0
       or not isinstance(ser[0], ureg.Quantity)):
        return ser
    units = set(val.units for val in ser)
    assert len(units) == 1
    return ser.astype(pint_pandas.PintType(next(iter(units))))


def norm_mem(mem):
    """
    Convert memory size units to get the next most compact integer magnitude

    Args:
        mem (pint.Quantity): pint.Quantity representing memory size

    Returns:
        tuple(int, str): the magnitude as integer, decimal memory size units

    Raises:
        StaticValueError: if mem is not an integer multiple of 1 byte

    """
    units = {'petabyte': 'PB', 'terabyte': 'TB', 'gigabyte': 'GB',
             'megabyte': 'MB', 'kilobyte': 'KB', 'byte': 'B'}
    for unit, slurm_unit in units.items():
        mag = mem.to(unit).magnitude
        if ceil(mag) == floor(mag):
            return ceil(mag), slurm_unit
    raise StaticValueError('memory size must be integer number of bytes')

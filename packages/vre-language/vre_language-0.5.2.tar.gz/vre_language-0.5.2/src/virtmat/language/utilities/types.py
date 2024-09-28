"""utility functions and classes to work with types"""
from collections.abc import Iterable
import numpy
import pandas
import pint_pandas
from fireworks.utilities.fw_serializers import FWSerializable
from virtmat.language.utilities.units import ureg

dtypemap = {'BoolArray': bool, 'StrArray': str, 'IntArray': int,
            'FloatArray': float, 'ComplexArray': complex, 'IntSubArray': int,
            'FloatSubArray': float, 'ComplexSubArray': complex}

scalar_realtype = (int, float, numpy.integer, numpy.floating)
scalar_numtype = (*scalar_realtype, complex, numpy.complexfloating)
scalar_booltype = (bool, numpy.bool_)
scalar_type = (str, *scalar_booltype, *scalar_numtype)


def is_numeric_type(type_):
    """check if the type_ is numeric"""
    if issubclass(type_, scalar_numtype) and not issubclass(type_, bool):
        return True
    if issubclass(type_, ureg.Quantity):
        return True
    if issubclass(type_, numpy.ndarray) and type_.datatype in scalar_numtype:
        return True
    if issubclass(type_, pandas.Series):
        if type_.datatype is None:
            return None
        if issubclass(type_.datatype, scalar_booltype):
            return False
        if issubclass(type_.datatype, (scalar_numtype, ureg.Quantity)):
            return True
        if issubclass(type_.datatype, numpy.ndarray):
            if type_.datatype.datatype in scalar_numtype:
                return True
    return False


def is_scalar_type(type_):
    """check if type_ is a scalar type"""
    if issubclass(type_, scalar_type):
        return True
    if issubclass(type_, ureg.Quantity) and not is_array_type(type_):
        return True
    return False


def is_array_type(type_):
    """check if type_ is array type"""
    return hasattr(type_, 'arraytype') and type_.arraytype


def is_numeric_scalar_type(type_):
    """check if the type_ is numeric scalar type"""
    return is_numeric_type(type_) and is_scalar_type(type_)


def is_numeric_array_type(type_):
    """check if the type is numeric array type"""
    return is_numeric_type(type_) and is_array_type(type_)


def is_numeric(obj):
    """check if the object is of numeric type"""
    if isinstance(obj, scalar_numtype) and not isinstance(obj, bool):
        return True
    if isinstance(obj, ureg.Quantity):
        return True
    if isinstance(obj, numpy.ndarray) and issubclass(obj.dtype.type, numpy.number):
        return True
    if isinstance(obj, pandas.Series):
        if len(obj) == 0 and isinstance(obj.dtype, pint_pandas.PintType):
            return True
        if hasattr(obj.values[0], 'magnitude'):
            return True
    if isinstance(obj, str):
        return False
    if isinstance(obj, Iterable):
        return all(is_numeric(item) for item in obj)
    return False


def is_scalar(obj):
    """check if the object is of scalar type"""
    if isinstance(obj, scalar_type):
        return True
    if isinstance(obj, ureg.Quantity) and not isinstance(obj.magnitude, numpy.ndarray):
        return True
    return False


def is_array(obj):
    """check if the obj is of an array type"""
    if isinstance(obj, numpy.ndarray):
        return True
    if isinstance(obj, ureg.Quantity) and isinstance(obj.magnitude, numpy.ndarray):
        return True
    return False


def is_numeric_scalar(obj):
    """check if the object is of numeric scalar type"""
    return is_numeric(obj) and is_scalar(obj)


def is_numeric_array(obj):
    """check if the object is of numeric array type"""
    return is_numeric(obj) and is_array(obj)


def settype(func):
    """
    Adapt the type of values at run time
    func: any value function
    Returns: a wrapped func
    """
    def wrapper(*args, **kwargs):
        rval = func(*args, **kwargs)
        if isinstance(rval, bool):
            return rval
        if isinstance(rval, numpy.bool_):
            return rval.item()
        if isinstance(rval, scalar_numtype):
            return ureg.Quantity(rval)
        if isinstance(rval, list):
            return tuple(rval)
        if isinstance(rval, FWSerializable) and hasattr(rval, 'to_base'):
            return rval.to_base()
        return rval
    return wrapper


def get_units(obj):
    """return the units of an object; if object is non-numeric return None"""
    if isinstance(obj, scalar_numtype) and not isinstance(obj, bool):
        return None
    if isinstance(obj, ureg.Quantity):
        return str(obj.units)
    if isinstance(obj, numpy.ndarray) and issubclass(obj.dtype.type, numpy.number):
        return None
    if isinstance(obj, pandas.Series):
        if len(obj) == 0 and isinstance(obj.dtype, pint_pandas.PintType):
            return str(obj.pint.units)
        if hasattr(obj.values[0], 'magnitude'):
            return str(obj.values[0].units)
    return None


class NotComputed:
    """Singleton that acts as placeholder not computed values"""
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __repr__(self):
        return 'n.c.'


NC = NotComputed()

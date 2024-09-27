"""Fractional uncertainty for Wanninkhof (2014)."""

from fluxerror.gas_transfer_velocity.wanninkhof2014._utils import (
    schmidt_number as _schmidt_number,
)
from fluxerror.gas_transfer_velocity.wanninkhof2014.derivative import (
    schmidt_number_wrt_temp,
)


def kw_umean(u_mean: float, u_std: float, delta_umean: float, *args, **kwargs) -> float:
    """Fractional uncertainy kw wrt to mean wind speed.

    Parameters
    ----------
    u_mean : float
        mean wind speed m/s
    u_std : float
        standard deviation of wind speed m/s
    delta_umean : float
        uncertainty in mean wind speed m/s

    Returns
    -------
    float :
        fractional uncertainty in kw wrt to mean wind speed
    """  # noqa: E501
    numerator = 2 * u_mean * delta_umean
    denominator = (u_mean * u_mean) + (u_std * u_std)
    return numerator / denominator


def kw_ustd(u_mean: float, u_std: float, delta_ustd: float, *args, **kwargs) -> float:
    """Fraction uncertainty in kw wrt to std of wind speed.

    Parameters
    ----------
    u_mean : float
        mean wind speed in m/s
    u_std : float
        standard deviatino of wind speed m/s
    delta_ustd : float
        uncertainty in standard deviation of wind speed m/s

    Returns
    -------
    float :
        fractional uncerttainty kw wrt to U std
    """  # noqa: E501
    numerator = 2 * u_std * delta_ustd
    denominator = u_mean * u_mean + u_std * u_std
    return numerator / denominator


def kw_sc(temp_C: float, delta_T: float, *args, **kwargs) -> float:
    """Fractional uncertainty in kw wrt to schmidt number.

    Parameters
    ----------
    temp_C : float
        temperature in degrees C
    delta_T : float
        uncertainty in temperature in degrees C

    Returns
    -------
    float :
        fractional uncertainty in kw wrt to Sc
    """  # noqa: E501
    Sc = _schmidt_number(temp_C)
    dSc_dT = schmidt_number_wrt_temp(temp_C)
    delta_Sc = dSc_dT * delta_T
    return (0.5 * delta_Sc) / Sc

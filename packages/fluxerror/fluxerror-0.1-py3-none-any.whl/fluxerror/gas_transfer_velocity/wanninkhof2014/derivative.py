"""Derivaties for Wanninkhof (2014)."""

from numpy import nanmedian as _nanmedian

from fluxerror.gas_transfer_velocity.wanninkhof2014._utils import (
    schmidt_number as _schmidt_number,
)


def schmidt_number_wrt_temp(temp_C, *args, **kwargs):
    r"""Calculate derivative of the Schmidt number wrt temperature.

    .. math::

        B + 2 \cdot C \cdot T + 3 \cdot D \cdot T^2 + 4 \cdot E \cdot T^3

    Paramters
    ---------
    temp_C : array
        temperature in degrees C

    Returns
    -------
    array :
        derivative of Schmidt number wrt temperature, dSc/dT, (1/degC)
    """  # noqa: E501
    if _nanmedian(temp_C) > 270:
        raise ValueError("temperature is not in degC")

    B = -136.25
    C = 4.7353
    D = -0.092307
    E = 0.000755
    return B + 2 * C * temp_C + 3 * D * (temp_C**2) + 4 * E * (temp_C**3)


def kw_wrt_umean(temp_C, u_mean, a=0.251, *args, **kwargs):
    r"""Calculate deriviative of kw wrt to mean wind speed.

    .. math::
        2 \cdot a \cdot U_{mean} \cdot \bigg(\frac{Sc}{660}\bigg)^{0.5}

    Parameters
    ----------
    temp_C : float
        temperature in degrees C
    u_mean : float
        mean wind speed in m/s
    a : float, optional
        constant. Defaults to 0.251.

    Returns
    -------
    float :
        derivative of kw wrt to mean wind speed
    """  # noqa: E501
    Sc = _schmidt_number(temp_C)
    return a * (2 * u_mean) * (Sc / 660) ** (0.5)


def kw_wrt_ustd(temp_C: float, u_std: float, a: float = 0.251) -> float:
    r"""Deriviative of kw wrt to standard deviation of wind speed.

    .. math::
        2 \cdot a \cdot U_{std} \cdot \bigg(\frac{Sc}{660}\bigg)^{0.5}

    Paramters
    ---------
    temp_C : float)
        temperature in degrees C
    u_std : float)
        standard deviation of wind speed in m/s
    a : float, optional
        constant. Defaults to 0.251.

    Returns
    -------
    float :
        derivative of kw wrt to standard deviation of wind speed
    """  # noqa: E501
    Sc = _schmidt_number(temp_C)
    return a * (2 * u_std) * (Sc / 660) ** (0.5)

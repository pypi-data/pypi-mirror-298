"""Fractional uncertainty equations for Weiss (1974)."""

from fluxerror.solubility.weiss1974 import derivative


def ko_wrt_temp(temp_C, S, delta_T, *args, **kwargs):
    r"""Fractional uncertainty of K from temperature.

    .. math::

        \frac{\partial K / \partial T]}{\delta T}

    Parameters
    ----------
    temp_C : float
        temperature in degrees C
    S : float
        salinity in PSU
    delta_T : float
        uncertainty in temperature in degrees C

    Returns
    -------
    frac :
        fractional uncertainty in K from temperature
    """  # noqa: E501
    T = temp_C + 273.15
    d_ko_dT = derivative.ko_wrt_temp(T, S)
    return d_ko_dT * delta_T


def ko_wrt_salt(temp_C, delta_S, *args, **kwargs):
    r"""Fractional uncertainty of K from salinity.

    .. math::

        \frac{\partial K / \partial S}{\delta S}

    Parameters
    ----------
    temp_C : float
        temperature in degrees C
    delta_S : float
        uncertainty in salinity

    Returns
    -------
    frac :
        fractional uncertainty in K from salinity
    """  # noqa: E501
    T = temp_C + 273.15
    d_ko_ds = derivative.ko_wrt_salt(T)
    return d_ko_ds * delta_S

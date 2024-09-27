"""Utility functions for fluxerror."""


def fractional_uncertainty(value, delta, *args, **kwargs):
    r"""Fractional uncertainty calculation.

    .. math::
        \frac{delta}{value}

    Parameters
    ----------
    value : float
        data point
    delta : float
        uncertainty in the value

    Returns
    -------
    fractional uncertainty : float
        fractional uncertainty calculated as delta / value
    """
    assert value != 0, "!! value can not be 0"
    return delta / value


def fractional_uncertainty_squared(delta, value, *args, **kwargs):
    r"""Fractional uncertainty squared calculation.

    .. math::

        \frac{delta}{value}^2

    Parameters
    ----------
    value : float
        data point
    delta : float
        uncertainty in the value

    Returns
    -------
    fractional uncertainty_squared : float
        squared fractional uncertainty
    """
    assert value != 0, "!! value can not be 0"
    return fractional_uncertainty(delta, value) * fractional_uncertainty(delta, value)


def frac_pco2ocn(pco2, delta_pco2, *args, **kwargs):
    """Fractional uncertainty in ocean pCO2.

    Parameters
    ----------
    pco2 : float
        ocean pco2
    delta_pco2 : float
        uncertainty in ocean pco2

    Returns
    -------
    float
        fractional uncertainty in pco2
    """
    return delta_pco2 / pco2

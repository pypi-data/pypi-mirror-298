"""Fractional uncertainty for delta pCO2."""


def pco2ocn(pco2, delta_pco2, *args, **kwargs):
    r"""Fractional uncertainty in pCO2.

    .. math::

        \frac{pCO_2}{\delta pCO_2}

    Parameters
    ----------
    pco2 : float
        ocean partial pressure of CO2
    delta_pco2 : float
       uncertainty in pCO2

    Returns
    -------
    float
       fractional uncertainty in pCO2
    """  # noqa: E501
    return delta_pco2 / pco2

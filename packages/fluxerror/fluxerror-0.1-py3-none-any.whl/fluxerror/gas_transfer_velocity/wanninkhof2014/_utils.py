"""Utilties for Wannikhof 2014."""

from numpy import nanmedian as _nanmedian


def schmidt_number(temp_C, *args, **kwargs):
    r"""Calculate the Schmidt number.

    Calculates the Schmidt number as defined by Jahne et al. (1987) and listed
    in Wanninkhof (2014) Table 1.

    .. math::
        Sc = a + b \cdot T + c \cdot T^2 + d \cdot T^3 + e \cdot T^4

    constants:

    * :math:`a = +2116.8`
    * :math:`b = -136.25`
    * :math:`c = +4.7353`
    * :math:`d = -0.092307`
    * :math:`e = +0.0007555`

    Parameters
    ----------
    temp_C : array
        temperature in degrees C

    Returns
    -------
    array :
        Schmidt number
        Units: dimensionless

    References
    ----------
    .. [1] Jähne, B., Heinz, G., & Dietrich, W. (1987).
        Measurement of the diffusion coefficients of sparingly soluble gases in water.
        Journal of Geophysical Research: Oceans, 92(C10), 10767–10776.
        `https://doi.org/10.1029/JC092iC10p10767 <https://doi.org/10.1029/JC092iC10p10767>`_
    """  # noqa: E501
    if _nanmedian(temp_C) > 270:
        raise ValueError("temperature is not in degC")

    T = temp_C

    a = +2116.8
    b = -136.25
    c = +4.7353
    d = -0.092307
    e = +0.0007555

    Sc = a + b * T + c * T**2 + d * T**3 + e * T**4

    return Sc

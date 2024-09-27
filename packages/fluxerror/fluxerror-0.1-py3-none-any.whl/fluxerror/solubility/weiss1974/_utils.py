"""Utility functions for Weiss (1974)."""

from math import log


def weiss1974_f1(temp_C, *args, **kwargs):
    r"""Calculate function 1 of Weiss (1974) parameterization.

    .. math::

        f_1(T) = a_1 + a_2 \cdot \bigg( \frac{100}{T} \bigg ) + a_3 \cdot \log \bigg ( \frac{T}{100} \bigg)

    Constants:

    * :math:`a_1 = -58.0931`
    * :math:`a_2 = +90.5069`
    * :math:`a_3 = +22.2940`

    Parameters
    ----------
    temp_C : float
        temperature in degrees C

    Returns
    -------
    float :
        function 1 of parameterization
    """  # noqa: E501
    T = temp_C + 273.15

    a1 = -58.0931
    a2 = +90.5069
    a3 = +22.2940
    T100 = T / 100
    return a1 + a2 * (100 / T) + a3 * log(T100)


def weiss1974_f2(temp_C, *args, **kwargs):
    r"""Calculate function 2 of Weiss (1974) parameterization.

    .. math::

        f_2(T) = b_1 + b_2 \cdot \bigg ( \frac{T}{100} \bigg)  + b_3 \cdot \bigg ( \frac{T}{100} \bigg)^2

    Constants:

    * :math:`b_1 = +0.027766`
    * :math:`b_2 = -0.025888`
    * :math:`b_3 = +0.0050578`

    Parameters
    ----------
    temp_C : float
        temperature in degrees C

    Returns
    -------
    float :
        function 2 of parameterization
    """  # noqa: E501
    T = temp_C + 273.15

    b1 = +0.027766
    b2 = -0.025888
    b3 = +0.0050578
    T100 = T / 100
    return b1 + b2 * T100 + b3 * T100**2


def weiss1974(temp_C, S, *args, **kwargs):
    r"""Weiss (1974) solubility parameterization.

    .. math::

        K = f_1(T) + S \cdot f_2(T)

    where

    .. math::

        f_1(T) = a_1 + a_2 \cdot \bigg( \frac{100}{T} \bigg ) + a_3 \\cdot \log \bigg ( \frac{T}{100} \bigg)

        f_2(T) = b_1 + b_2 \cdot \bigg ( \frac{T}{100} \bigg)  + b_3 \cdot \\bigg ( \frac{T}{100} \bigg)^2


    Constants:

    * :math:`a_1 = -58.0931`
    * :math:`a_2 = +90.5069`
    * :math:`a_3 = +22.2940`
    * :math:`b_1 = +0.027766`
    * :math:`b_2 = -0.025888`
    * :math:`b_3 = +0.0050578`

    Parameters
    ----------
    temp_C : float
        temperature in degrees C
    S : float
        salinity if practical salinity units

    Returns
    -------
    float :
        solubility using Weiss (1974) parameterization
    """  # noqa: E501
    T = temp_C + 273.15
    ko = weiss1974_f1(T) + (S * weiss1974_f2(T))
    return ko

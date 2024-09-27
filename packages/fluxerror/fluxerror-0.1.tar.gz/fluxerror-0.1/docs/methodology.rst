Methodology
===========

Here, we will derive the equations to calculate the uncertainty in the flux.
Uncertainty is calculated by applying the error propagation equation.
This is applicable when uncertainties are independent and random.

.. math::

    (\delta f)^2 =  \sum_i \bigg(\frac{\partial f}{\partial x_i} \delta x_i \bigg)^2

where (:math:`x_i`) are the measured quantities in :math:`f` and :math:`\delta x_i` are the associated uncertainties.

.. note::
    We used the simplifying assumption that the covariance is neglible and thus we dropped the higher order terms:
    :math:`\sum_{i \ne j} \bigg(\frac{\partial f}{\partial x_i} \bigg) \bigg(\frac{\partial f}{\partial x_j} \bigg) \text{cov}(x_i, x_j)`


........................................................

Bulk formula
-------------

The following expression is used to quantify the air-sea :math:`\text{CO}_2` flux (:math:`\text{FCO}_2`)
from gridded datasets in terms of gas transfer velocity (:math:`k_w`), solubility (:math:`K_o`),
sea-ice fraction in the grid cell (:math:`f_{ice}`), and the difference in :math:`\text{pCO}_2`
between the atmosphere and the ocean (:math:`\Delta \text{pCO}_2`):


.. math::
    \text{FCO}_2 = k_w \cdot K_o \cdot (1-f_{ice}) \cdot \Delta \text{pCO}_2
    \label{eq:bulk_formula}


Gas transfer velocity
......................

There are various formulations for the gas transfer velocity that are applicable across a range of wind speeds.
Here, we use the Wanninkhof 2014 parameterization, which depends on the square of the wind speed as well as the Schmidt number through the following parameterization:

.. math::
    k_w = a \cdot \langle U^2 \rangle \cdot \left(\frac{Sc}{660}\right)^{0.5} \label{eq:gas_trasnfer}

where :math:`a` is a scaling factor; :math:`\langle U^2 \rangle` is the average of the 10m neutral stability wind speed (:math:`U_{10}`) squared,
i.e., the second moment; and :math:`Sc` is the dimensionless Schmidt number.
This parameterization was chosen given its widely accepted use in the literature, including data products and models.

**Schmidt number**

The Schmidt number is defined as the kinematic viscosity of water divided by the molecular diffusion coefficient of the gas in water.
Wanninkhof 2014 provides a fourth-order polynomial fit versus temperature:

.. math::

    Sc = A + BT + CT^2 + DT^3 + ET^4

where :math:`T` (:math:`^\circ \text{C}`) is the sea surface temperature and A, B, C, D, and E are fit coefficients.

.. list-table:: Fit paramters to fourth-rder polynomial
   :widths: 30 30
   :header-rows: 1

   * - Parameter
     - Value
   * - A
     - 2116.8
   * - B
     - -136.25
   * - C
     - 4.735
   * - D
     - -0.092307
   * - E
     - 0.0007555


Solubility
..........

The temperature- and salinity-dependent solubility is calculated as:

.. math::

    \ln(K_0) = A_1 + A_2\bigg(\frac{100}{T}\bigg) + A_3 \cdot \ln\bigg(\frac{T}{100}\bigg) + S\bigg[B_1 + B_2\bigg(\frac{T}{100}\bigg)+B_3\bigg(\frac{T}{100}\bigg)^2\bigg]

where :math:`T` (K) is temperature and :math:`S` (PSU) is salinity while :math:`A_i` and :math:`B_i` are fit coeffcients.

.. list-table:: Solubility parameterization coefficients
   :widths: 30 30
   :header-rows: 1

   * - Parameter
     - Value (:math:`\frac{moles}{l * atm}`)
   * - :math:`A_1`
     -  -58.0931
   * - :math:`A_2`
     - -90.5069
   * - :math:`A_3`
     - 22.2940
   * - :math:`B_1`
     - 0.027766
   * - :math:`B_2`
     - -0.025888
   * - :math:`B_3`
     - 0.0050578


Partial pressure of :math:`\text{CO}_2`
.......................................

The partial pressure of :math:`\text{CO}_2` between the atmosphere and ocean
is defined as

.. math::

    \Delta pCO_2 = pCO_2^{atm} - pCO_2^{ocn}


.........................................


Propagation of errors
----------------------

Applying the propagation of error to the bulk formula, and writing it in terms of fractional uncertainties, we arrive at the following expression:

.. math::

    \bigg(\frac{\delta FCO2}{FCO2}\bigg)^2 = \bigg(\frac{\delta kw}{kw} \bigg)^2 +  \bigg(\frac{\delta K0}{K0} \bigg)^2 +  \bigg(\frac{\delta \Delta pCO2}{\Delta pCO2} \bigg)^2


:math:`k_w`: Wanninkhof 2014 parameterization
................................................

The fractional uncertainty associated with the gas transfer velocity
can be expanded into contributions from wind speed and the Schdmit number

.. math::

    \bigg(\frac{\delta k_w}{k_w}\bigg)^2  = \bigg(\frac{2 \cdot \overline{U} \cdot \delta \overline{U}}{\overline{U}^2 + \sigma_U^2}\bigg)^2 + \bigg(\frac{2 \cdot \sigma_U \cdot \delta \sigma_U}{\overline{U}^2 + \sigma_U^2}\bigg)^2 + \bigg(\frac{0.5 \cdot \delta Sc}{Sc}\bigg)^2 \label{eq:frac_kw}

:math:`K_o` : Weiss 1974 parameterization
...........................................

The fractional uncertainty associated with the solubility
can be expanded into contributiosns from temperature and salinity

.. math::

    \bigg(\frac{\delta K_0}{K_0}\bigg)^2  = \bigg(\frac{\partial f_1(T)}{\partial T} + S*\frac{\partial f_2(T)}{\partial T}\bigg)^2 \delta T^2 + f_2(T)^2*\delta S^2 \label{eq:frac_ko}


Air-sea difference partial pressure
....................................

Here we use the obesrvation that uncertainty in ocean :math:`pCO_2` is
order of magnitude greater than uncertainty: :math:`\delta pCO_2^{ocen} >> \delta pCO_2^{atm}`.
Assuming uncertainty in the atmospheric :math:`pCO_2` to be negligible, we arrive at the following

.. math::

    \frac{\delta \Delta pCO_2}{\Delta pCO_2} \approx \frac{\delta pCO_2^{ocn}}{\Delta pCO_2}

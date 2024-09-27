.. FluxError documentation master file, created by
   sphinx-quickstart on Tue Jul 16 22:57:10 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FluxError Documentation
========================================

The goal of `FluxError` is to make it easy to calculate the uncertainty in air-sea CO2 flux
and the contribution of each term to total uncertainty. `FluxError` assumes the bulk
formula is used to estimate flux:

.. math::

   FCO2 = k_w \cdot K_o \cdot \Delta pCO_2

Where the air-sea flux of CO2 (:math:`FCO2`) is expressed in terms of the piston velocity (:math:`k_w`),
solubility (:math:`K_o`), and difference in partial pressure between atmosphere and ocean (:math:`\Delta pCO_2`).

Applying a propagation of errors, and assuming independence, we can express the flux in terms of fractional uncertainties

.. math::

       \bigg(\frac{\delta FCO2}{FCO2}\bigg)^2 = \bigg(\frac{\delta kw}{kw} \bigg)^2 +  \bigg(\frac{\delta K_o}{K_o} \bigg)^2 +  \bigg(\frac{\delta \Delta pCO2}{\Delta pCO2} \bigg)^2

Where all the :math:`\delta` terms are the uncertainties.

To calculate these terms you just need to know the uncertainty of the of the components that make it up.
For instance, solubility depends on temperature and salinity. So as long as you know the uncertainty of
each dataset (ideally spatiotemporal uncertainty), then you can calculate the uncertainty in solubility.

We have used a common parameterization for piston velocity and solubility, but other can be included in the future.


Installation
------------

.. code-block:: bash

   # for bleeding-edge up-to-date commit
   pip install -e git+https://github.com/lgloege/fluxerror.git

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   methodology
   api

.. toctree::
   :maxdepth: 2
   :caption: Help and References:

   contributing
   authors
   GitHub repo <https://github.com/lgloege/fluxerror>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

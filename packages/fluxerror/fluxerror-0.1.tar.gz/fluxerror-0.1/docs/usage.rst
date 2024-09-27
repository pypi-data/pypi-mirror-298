Quickstart Guide
====================================================

Installation
------------

.. code-block:: bash

   # for bleeding-edge up-to-date commit
   pip install -e git+https://github.com/lgloege/fluxerror.git


Calculating fractional uncertainty
----------------------------------------------------

solubility
...........

To calculate fractional uncertainty from the Weiss (1974)
solubility parameterization, you can use the following

.. code-block:: python

   from fluxerror import solubility as sol

   # fractional uncertainty in Weiss (1974)
   frac_sol = sol.weiss1974.frac.ko_wrt_temp(temp_C =32, delta_S = 0.1)


Gas Transfer Velocity
......................

.. code-block:: python

   from fluxerror import gas_transfer_velocity as kw

   # fractional uncertainty in Weiss (1974)
   frac_sol = kw.wanninkhof2014.frac.kw_umean(temp_C =32, delta_S = 0.1)

:math:`\Delta \text{pCO}_2`
...........................

.. code-block:: python

   from fluxerror import delta_pco2 as dpco2

   # fractional uncertainty in Weiss (1974)
   frac_sol = kdpco2.frac.pco2ocn(temp_C =32, delta_S = 0.1)
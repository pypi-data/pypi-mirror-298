|CC WANG LAB IMG| # Description The package calculates freatures for
different types of fins and tubes.

LouverFinFlatTube is a class representing a louver fin used in heat
exchangers. # Usage

Install
-------

   pip install finsHt-0.0.1-py3-none-any.whl

Tutorial
========

Louverfin-Flat tube
-------------------

Create a Louverfin-Flat tube
----------------------------

   def
   **init**\ (k,pitch,thickness,louver_pitch,louver_height,louver_angle,louver_length,depth)

Sample
======

.. code:: python

   from finsHt import fins as ff
   louver = ff.LouverFinFlatTube(k=180,pitch=1.25e-3,thickness=0.1e-3,louver_pitch=0.8e-3,louver_height=0.8e-3,louver_angle=25,louver_length=6.5e-3,depth=20e-3,)
   louver.__post_init__(outside_tube_diameter=2e-3,mu_air=1.5e-5,rho_air=1.2,cp_air=1000,Pr_air=0.7,air_velocity=4,coil_length=0.15,P_t=9.97e-3,P_l=20e-3,tube_depth=20e-3,)
   print(louver.eta_overall)

Git Hub Repository
==================

You can know our project here:
`GitHub <https://github.com/maysam-gholampour/MyHT.git>`__.

References
==========

https://www.sciencedirect.com/science/article/pii/0017931096001160
https://www.sciencedirect.com/science/article/pii/S0017931099002896?via%3Dihub

-  Free software: MIT license

Credits
-------

-  CC Wang Laboratory
-  Maysam & Roger

.. |CC WANG LAB IMG| image:: https://media.licdn.com/dms/image/v2/D4E16AQH3PdcsyioUCw/profile-displaybackgroundimage-shrink_200_800/profile-displaybackgroundimage-shrink_200_800/0/1710633034047?e=2147483647&v=beta&t=dNiK32tceLYythWcCEs8BbXMswVZcShixcy2wLiz6T0

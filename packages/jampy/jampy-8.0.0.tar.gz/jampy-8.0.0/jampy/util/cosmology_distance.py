"""
    Copyright (C) 2016-2023, Michele Cappellari

    E-mail: michele.cappellari_at_physics.ox.ac.uk

    Updated versions of the software are available from my web page
    https://purl.org/cappellari/software

    This software is provided as is without any warranty whatsoever.
    Permission to use, for non-commercial purposes is granted.
    Permission to modify for personal or internal use is granted,
    provided this copyright and disclaimer are included unchanged
    at the beginning of the file. All other rights are reserved.
    In particular, redistribution of the code is not allowed.

    Changelog
    ---------

    V1.0.0: Michele Cappellari, Oxford, 6 June 2016
    +++++++++++++++++++++++++++++++++++++++++++++++

    - Written and tested as a separate procedure.

    V1.1.0: MC, Oxford, 17 August 2022
    ++++++++++++++++++++++++++++++++++

    - Included angular_diameter_distance and luminosity_distance.

    Vx.x.x: MC, Oxford
    ++++++++++++++++++

    - Additional changes are documented in the CHANGELOG of the JamPy package.
            
"""
import numpy as np

from jampy.util.quad1d import quad1d

###############################################################################

def integrand(z, omega_m, omega_k, omega_lam):
    """Equation (14) of Hogg-99 http://arxiv.org/abs/astro-ph/9905116v4"""

    ez = np.sqrt(omega_m*(1 + z)**3 + omega_k*(1 + z)**2 + omega_lam)

    return 1/ez

###############################################################################

def comoving_distance(z, h0=70, omega_m=0.3, omega_lam=None):
    """Calculate comoving distance D_C (in Mpc) of an object given its redshift"""
    
    if omega_lam is None:   # flat Universe
        omega_lam = 1 - omega_m

    # Equation (7) of Hogg-99
    omega_k = 1 - omega_m - omega_lam

    c = 299792.458                  #  speed of light in km/s
    dh = c/h0

    is_scalar = np.isscalar(z)
    z = np.atleast_1d(z)
    dc = np.zeros_like(z, dtype=float)
    for i, zi in enumerate(z):  # equation (15) of Hogg-99
        dc[i] = dh*quad1d(integrand, [0, zi], args=(omega_m, omega_k, omega_lam)).integ

    # Equation (16) of Hogg-99
    if omega_k > 0:
        dm = dh*np.sinh(np.sqrt(omega_k)*dc/dh)/np.sqrt(omega_k)
    elif omega_k < 0:
        dm = dh*np.sin(np.sqrt(np.abs(omega_k))*dc/dh)/np.sqrt(np.abs(omega_k))
    else:
        dm = dc

    if is_scalar:
        dm = dm.item()  # Make it a scalar if input was scalar

    return dm
 
##############################################################################

def angular_diameter_distance(z, **kwargs):
    """Calculate angular diameter distance D_A (in Mpc) of an object given its redshift"""

    return comoving_distance(z, **kwargs)/(1 + z)

##############################################################################

def luminosity_distance(z, **kwargs):
    """Calculate luminosity distance D_L (in Mpc) of an object given its redshift"""

    return comoving_distance(z, **kwargs)*(1 + z)

##############################################################################

if __name__ == '__main__':
    """Usage example"""

    z = 3.0
    dm = comoving_distance(z)
    print(f"redshift: {z}\nComoving distance: {dm}\nLuminosity distance: {dm*(1 + z)}\n"
          f"Angular diameter distance: {dm/(1 + z)}")

    dm = comoving_distance(z, omega_m=0.4, omega_lam=0.3)
    print(f"redshift: {z}\nComoving distance: {dm}\nLuminosity distance: {dm*(1 + z)}\n"
          f"Angular diameter distance: {dm/(1 + z)}")

from math import pi
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike


def xy2ll(
    x: ArrayLike,
    y: ArrayLike,
    sgn: Literal[1, -1],
    *args,
) -> tuple[ArrayLike, ArrayLike]:
    """Convert x y arrays to lat long arrays.

    Converts Polar  Stereographic (X, Y) coordinates for the polar regions to
    latitude and longitude Stereographic (X, Y) coordinates for the polar
    regions.
    Author: Michael P. Schodlok, December 2003 (map2xy.m)

    Parameters:
        - x: ArrayLike (float scalar or array)
        - y: ArrayLike (float scalar or array)
        - sgn (sign of latitude): integer (1 or -1) inidcating the hemisphere.
              1 : north latitude (default is mer = 45 lat = 70).
              -1 : south latitude (default is mer = 0  lat = 71).
        - *args: optional args. First optional arg is `delta` and second is
           `slat`. Review code for how these are used in practice.
    Returns:
        - (lat, lon)

    Usage:
        [lat, lon] = xy2ll(x, y, sgn)
        [lat, lon] = xy2ll(x, y, sgn, central_meridian, standard_parallel)
    """
    # Get central_meridian and standard_parallel depending on hemisphere
    if len(args) == 2:
        delta = args[0]
        slat = args[1]
    elif len(args) == 0:
        if sgn == 1:
            delta = 45.
            slat = 70.
            print(
                '       '
                ' xy2ll: creating coordinates in north polar stereographic'
                ' (Std Latitude: 70degN Meridian: 45deg)'
            )
        elif sgn == -1:
            delta = 0.
            slat = 71.
            print(
                '       '
                ' xy2ll: creating coordinates in south polar stereographic'
                ' (Std Latitude: 71degS Meridian: 0deg)'
            )
        else:
            raise ValueError('sgn should be either 1 or -1')
    else:
        raise Exception('bad usage: type "help(xy2ll)" for details')

    # if x, y passed as lists, convert to np.arrays
    if not np.issubdtype(type(x), np.ndarray):
        x = np.array(x)
    if not np.issubdtype(type(y), np.ndarray):
        y = np.array(y)

    # Conversion constant from degrees to radians
    # cde = 57.29577951
    # Radius of the earth in meters
    re = 6378.273 * 10**3
    # Eccentricity of the Hughes ellipsoid squared
    ex2 = .006693883
    # Eccentricity of the Hughes ellipsoid
    ex = np.sqrt(ex2)

    sl = slat * pi / 180.
    rho = np.sqrt(x**2 + y**2)
    cm = np.cos(sl) / np.sqrt(1.0 - ex2 * (np.sin(sl)**2))
    T = np.tan((pi / 4.0) - (sl / 2.0)) / ((1.0 - ex * np.sin(sl)) / (1.0 + ex * np.sin(sl)))**(ex / 2.0)

    if abs(slat - 90.) < 1.e-5:
        T = rho * np.sqrt((1. + ex)**(1. + ex) * (1. - ex)**(1. - ex)) / 2. / re
    else:
        T = rho * T / (re * cm)

    chi = (pi / 2.0) - 2.0 * np.arctan(T)
    lat = chi + ((ex2 / 2.0) + (5.0 * ex2**2.0 / 24.0) + (ex2**3.0 / 12.0)) * np.sin(2 * chi) + ((7.0 * ex2**2.0 / 48.0) + (29.0 * ex2**3 / 240.0)) * np.sin(4.0 * chi) + (7.0 * ex2**3.0 / 120.0) * np.sin(6.0 * chi)

    lat = sgn * lat
    lon = np.arctan2(sgn * x, -sgn * y)
    lon = sgn * lon

    res1 = np.nonzero(rho <= 0.1)[0]
    if len(res1) > 0:
        lat[res1] = pi / 2. * sgn
        lon[res1] = 0.0

    lon = lon * 180. / pi
    lat = lat * 180. / pi
    lon = lon - delta

    return lat, lon

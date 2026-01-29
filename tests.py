import numpy as np
from netCDF4 import Dataset

from interp_bedmachine_antarctica import interp_bedmachine_antarctica
from xy2ll import xy2ll
from ll2xy import ll2xy


def test_interp_bedmachine_antarctica():
    to_x = np.linspace(-1666500.0, 1666500.0, 13332)
    to_y = np.linspace(-1666500.0, 1666500.0, 13332)
    variable = 'bed'
    bedmachine_nc_path = './NSIDC-0756_BedMachineAntarctica_19700101-20191001_V04.1.nc'
    interpolated = interp_bedmachine_antarctica(
            to_x,
            to_y,
            variable,
            bedmachine_nc_path=bedmachine_nc_path
    )

    assert interpolated is not None


def test_xy2ll():
    ds = Dataset('NSIDC-0756_BedMachineAntarctica_19700101-20191001_V04.1.nc')
    xs = ds.variables['x'][:]
    ys = ds.variables['y'][:]

    # cast xs and ys as float. `xy2ll` will not return correct results
    # otherwise.
    xs = xs.astype(float)
    ys = ys.astype(float)

    lats, lons = xy2ll(
        xs,
        ys,
        -1,  # -1 is a flag indicating the southern hemisphere.
    )

    assert lats is not None
    assert lons is not None


def test_ll2xy():
    lat = np.array([-48.46])
    lon = np.array([-45])
    x, y = ll2xy(lat, lon)

    assert x is not None
    assert y is not None

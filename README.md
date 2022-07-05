![NSIDC logo](/images/nsidc_logo.png)
![NSIDC DAAC Logo](/images/nsidc_daac_logo.png)
![NASA logo](/images/nasa_logo.png)

nsidc0756-scripts
---

Scripts related to [NSIDC-0756](https://nsidc.org/data/nsidc-0756): MEaSUREs
BedMachine Antarctica, Version 2. This repository is a work in progress! 

The scripts that are currently in this repository can be used to convert between
geographic lat/lon and polar stereographic coordinates, and for interpolating
BedMachine Antarctica data onto user-defined coordinates.

For example, one could interpolate bedrock elevation values from BedMachine
Antarctica onto a latitude/longitude grid. First, use the `ll2xy` script to
convert lat/lon coordinates to polar stereographic coordinates. Then these
coordinates can be used as input for the `interpBedmachineantarctica` script which
will interpolate BedMachine Antarctica values onto the input coordinates. The
scripts are available both as Matlab and python scripts, for further details
please see below.

## Level of Support

* This repository is fully supported by NSIDC. If you discover any problems or
  bugs, please submit an Issue. If you would like to contribute to this
  repository, you may fork the repository and submit a pull request.

See the [LICENSE](LICENSE.md) for details on permissions and warranties.  Please
contact nsidc@nsidc.org for more information.

# Scripts

## xy2ll.m | xy2ll.py

Converts polar stereographic (x, y) coodinates to geodetic (latitude, longitude) coordinates.

Usage example for `xy2ll.py`:

```
from netCDF4 import Dataset

from xy2ll import xy2ll

ds = Dataset('BedMachineAntarctica_2019-11-05_v01.nc')
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
```


## ll2xy.m | ll2xy.py

Converts geodetic (latitude, longitude) coordinates to polar sterographic (x, y) coordinates.

## interpBedmachineantarctica.m | interp_bedmachine_antarctica.py

Interpolates values from the BedMachineAntarctica netcdf file onto requested (x,
y) polar stereographic coordinates.

NOTE: 

`interp_bedmachine_antarctica.py` does not provide a perfect re-implementation
of `interpBedMachineAntarctica.m`! When used with a `to_x` array of <1000, this
code should perform in roughly the same way. When interpolating onto larger
grids, `interpBedMachineAntarctica.m` uses a custom interpolation algorithm that
has not yet been implemented in Python.

Outputs from `interpBedMachineAntarctica.m` have not been directly compared to
`interp_bedmachine_antarctica.py` yet. Results may differ.

### Setup

To use `interp_bedmachine_antarctica.py`, the requirements listed under
`environment.yml` must be installed.

To create an environment with `conda`:

```
$ conda env create -f environment.yml
$ conda activate interp_bedmachine
```

#### Example usage (Python):

```
$ python
>>> from interp_bedmachine_antarctica import interp_bedmachine_antarctica
>>> import numpy as np
>>> to_x = np.linspace(-1666500.0, 1666500.0, 13332)
>>> to_y = np.linspace(-1666500.0, 1666500.0, 13332)
>>> variable = 'bed'
>>> bedmachine_nc_path = './BedMachineAntarctica_2019-11-05_v01.nc'
>>> interpolated = interp_bedmachine_antarctica(
        to_x,
        to_y,
        variable,
        bedmachine_nc_path=bedmachine_nc_path
)
>>> interpolated
array([[-4442.84863281, -4442.40963504, -4441.97063731, ...,
          386.82238055,   388.31525668,   389.80810547],
       [-4442.15570974, -4441.8033949 , -4441.45106056, ...,
          385.1755937 ,   386.62244517,   388.06926655],
       [-4441.46270859, -4441.19708971, -4440.93143181, ...,
          383.52890537,   384.92973833,   386.33053843],
       ...,
       [-4019.93213131, -4021.66220741, -4023.39202323, ...,
          241.79977309,   241.0239085 ,   240.24799334],
       [-4018.98273722, -4020.62648272, -4022.27007854, ...,
          264.8464815 ,   262.60142472,   260.35621881],
       [-4018.03344727, -4019.59069298, -4021.14789963, ...,
          287.89288765,   284.17862334,   280.46411133]])
```

#### Example usage (MATLAB):

```
% Input lat. and lon. and they can be an array or a list.
lat = [-84.72, -82.03; -83.96, -79.07];
lon = [92.41 ,85.11; 65.65, 77.67];

% For each lat., lon. calculate the stereographic coordinates
[x,y] = ll2xy(lat, lon, -1);

% Interpolate the Bedmachine values onto the coordinates
bed = interpBedmachineAntarctica(x,y,'bed');

disp(bed)
```

## License

See [LICENSE](LICENSE.md).

## Code of Conduct

See [Code of Conduct](CODE_OF_CONDUCT.md).

## Credit

This software was developed by the National Snow and Ice Data Center with
funding from multiple sources.

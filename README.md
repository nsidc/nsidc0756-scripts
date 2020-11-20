nsidc0756-m2py
---

# xy2ll.m | xy2ll.py

Converts polar stereographic (x, y) coodinates to geodetic (latitude, longitude) coordinates.

# ll2xy.m | ll2xy.py

Converts geodetic (latitude, longitude) coordinates to polar sterographic (x, y) coordinates.

# interpBedmachineantarctica.m | interp_bedmachine_antarctica.py

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

## Setup

To use `interp_bedmachine_antarctica.py`, the requirements listed under
`environment.yml` must be installed.

To create an environment with `conda`:

```
$ conda env create -f environment.yml
$ conda activate interp_bedmachine
```

## Example usage:

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

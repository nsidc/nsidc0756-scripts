import numpy as np
import xarray as xr


_POSSIBLE_VARIABLES = (
    'mask',
    'icemask',
    'firn',
    'surface',
    'bed',
    'errbed',
    'geoid',
    'source'
)


def _interpolate_with_xarray(to_x, to_y, variable, bedmachine_nc_path, *, return_grid):
    """Interpolate `variable` onto `to_x`, `to_y` coordinates using xarray.

    xarray's `interp` method should roughly correspond to MATLAB's `interp2`.
    
    Args:
        * to_x: 1D numpy array representing x coordinates to interpolate `variable` onto
        * to_y: 1D numpy array representing y coordinates to interpolate `variable` onto
        * variable: string representing variable to interpolate
        * return_grid (Bool): if True, return a grid of interpolated points of
          size `to_x` by `to_y`. E.g., if to_x is an array of length 2 and to_y
          is an array of length 3, a grid of size 2x3 will will be
          returned. Otherwies, only the coodinate pairs represented by `to_x`
          and `to_y` will be returned (the diagonal of the grid).
    
    Returns:
        a 2D numpy array of interpolated values.
    """
    xr_ds = xr.open_dataset(bedmachine_nc_path)

    if variable == 'icemask':
        # This is a derived value.
        # the MATLAB source code states:
        #   ice ocean interface is between 0 and 3, so we might get some 1 by
        #   interpolating
        icemask = xr_ds.mask.copy()
        icemask = icemask.where(icemask != 3, other=0)
        xr_variable = icemask
    else:
        xr_variable = xr_ds[variable]

    # Note, 'icemask' is not considered 'mask' in the matlab code, so it ends
    # up with method=linear.
    if variable in ('mask', 'icemask', 'source'):
        method = 'nearest'
    else:
        # xarray's linear interpolation is similar to matlab's `interp2` with
        # method=bilinear
        method = 'linear'

    if not return_grid:
        # if `return_grid` is False, `to_x` and `to_y` should be the same
        # length (each pair of values represents a point). Ultimately, we should
        # probably change this interface to make it clearer what the input args
        # represent.
        if len(to_x) != len(to_y):
            raise RuntimeError(
                'When `return_grid` is False, `to_x` and `to_y` must be arrays of the same length.'
            )

        # https://xarray.pydata.org/en/stable/indexing.html#more-advanced-indexing
        to_x = xr.DataArray(to_x, dims='z')
        to_y = xr.DataArray(to_y, dims='z')

    result = xr_variable.interp(
        coords={
            'x': to_x,
            'y': to_y
        },
        method=method
    )

    # Return a numpy array to be consistent with the other python scripts.
    return result.values


def interp_bedmachine_antarctica(to_x, to_y, variable, return_grid=False, *, bedmachine_nc_path):
    """Interpolate `variable` onto `to_x`, `to_y` coordinates.

    NOTE:
        This is not a perfect reproduction of the code in
        interpBedMachineAntarctica.m. When used with a `to_x` array of <1000,
        this code should perform in roughly the same way. When interpolating
        onto larger grids, interpBedMachineAntarctica.m uses a custom
        interpolation algorithm that has not yet been implemented in Python.

    Args:
        * to_x: 1D numpy array representing x coordinates to interpolate `variable` onto
        * to_y: 1D numpy array representing y coordinates to interpolate `variable` onto
        * variable: string representing variable to interpolate
        * return_grid (Bool): if True, return a grid of interpolated points of
          size `to_x` by `to_y`. E.g., if to_x is an array of length 2 and to_y
          is an array of length 3, a grid of size 2x3 will will be
          returned. Otherwies, only the coodinate pairs represented by `to_x`
          and `to_y` will be returned (the diagonal of the grid).
        * bedmachine_nc_path (required kwarg):

    Returns:
        a 2D numpy array of interpolated values.
    """
    if variable not in _POSSIBLE_VARIABLES:
        raise RuntimeError(
            f'Unexpected variable name {variable}. Must be one of {possible_variables}'
        )

    return _interpolate_with_xarray(
        to_x,
        to_y,
        variable,
        bedmachine_nc_path,
        return_grid=return_grid
    )


if __name__ == '__main__':
    # Example usage
    to_x = np.linspace(-1666500.0, 1666500.0, 13332)
    to_y = np.linspace(-1666500.0, 1666500.0, 13332)
    variable = 'bed'
    bedmachine_nc_path = './BedMachineAntarctica_2019-11-05_v01.nc'

    interpolated = interp_bedmachine_antarctica(
        to_x,
        to_y,
        variable,
        bedmachine_nc_path=bedmachine_nc_path
    )
    print('Done interpolating!')

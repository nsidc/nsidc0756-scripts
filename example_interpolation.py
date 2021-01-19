# TODO: turn the python code into an importable package.
from ll2xy import ll2xy
from interp_bedmachine_antarctica import interp_bedmachine_antarctica

BEDMACHINE_NC_PATH = './BedMachineAntarctica_2019-11-05_v01.nc'
VARIABLE = 'bed'

# Set `RETURN_AS_GRID` to `True` to get a grid of values instead of just the points represented
# by `to_x` and `to_y`. Set to `False` if you just want the output interpolated
# variable for the points represented by `to_x` and `to_y`.
RETURN_AS_GRID = False

lats = [-84.72, -82.03, -83.96, -79.07]
lons = [92.41, 85.11, 65.65, 77.67]

to_x = []
to_y = []

for lat, lon in zip(lats, lons):
    x, y = ll2xy(lat, lon, -1)
    to_y.append(y)
    to_x.append(x)

interpolated = interp_bedmachine_antarctica(
    to_x,
    to_y,
    VARIABLE,
    return_grid=RETURN_AS_GRID,
    bedmachine_nc_path=BEDMACHINE_NC_PATH
)

print(interpolated)

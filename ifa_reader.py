#%%
import pandas as pd
import numpy as np
import xarray as xr

file = "basic_flds.ifa"

ncols = pd.read_csv(
    file, delimiter=" ", skipinitialspace=True, skiprows=1, nrows=1, header=None
)
ncols = ncols.size

#%%
df = pd.read_csv(
    file,
    delimiter="\s*[ ]\s*",
    header=None,
    engine="python",
    index_col=False,
    names=np.arange(ncols),
)

# %%
splits = [ix for ix in df[df.isnull().any(axis=1)].index] + [len(df)]
dfs = [df[splits[i] : splits[i + 1]] for i in range(len(splits) - 1)]

# %%


def to_dataarray(dataframe):
    year, month, day, hour, *_ = dataframe.iloc[0].T.values
    dataframe = dataframe.replace(-999, np.nan)
    raw_data = dataframe.iloc[1:]
    xdata = xr.Dataset(
        {
            "pr": (["nz"], raw_data[0], dict(long_name="Pressure", units="hPa")),
            "z": (["nz"], raw_data[1], dict(long_name="Height")),
            "t": (["nz"], raw_data[2]),
            "q": (
                ["nz"],
                raw_data[3],
                dict(long_name="Specific Humidity", units="g/kg"),
            ),
            "rh": (["nz"], raw_data[4], dict(long_name="Relative Humidity", units="%")),
            "u": (["nz"], raw_data[5], dict(long_name="Zonal-wind component")),
            "v": (["nz"], raw_data[6], dict(long_name="Meridional-wind component")),
        },
        coords={
            "time": pd.to_datetime(
                f"{year+1900:.0f}-{month:02.0f}-{day:02.0f} {hour}:00"
            ),
            "nz": np.arange(raw_data[0].size),
        },
    )
    return xdata


# %%

ds_container = [to_dataarray(x) for x in dfs]
xdata = xr.concat(ds_container, dim="time", join="right")
# %%

# Save the data
xdata.to_netcdf("basic_flds.nc")
# %%

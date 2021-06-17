#%%
import numpy as np
import pandas as pd
import xarray as xr

file_basic = "basic_flds.ifa"
file_deriv = "deriv_flds.ifa"

#%%


def stacked_data(file):
    ncols = pd.read_csv(
        file, delimiter=" ", skipinitialspace=True, skiprows=1, nrows=1, header=None
    )
    ncols = ncols.size

    df = pd.read_csv(
        file,
        delimiter="\s*[ ]\s*",
        header=None,
        engine="python",
        index_col=False,
        names=np.arange(ncols),
    )

    splits = [ix for ix in df[df.isnull().any(axis=1)].index] + [len(df)]
    dfs = [df[splits[i] : splits[i + 1]] for i in range(len(splits) - 1)]

    return dfs


# %%


def basic_to_dataset(dataframe):
    year, month, day, hour, *_ = dataframe.iloc[0].values
    dataframe = dataframe.replace(-999, np.nan)
    raw_data = dataframe.iloc[2:]
    xdata = xr.Dataset(
        {
            "z": (["pr"], raw_data[1], dict(long_name="Height")),
            "t": (["pr"], raw_data[2], dict(long_name="Temperature")),
            "q": (
                ["pr"],
                raw_data[3],
                dict(long_name="Specific Humidity", units="g/kg"),
            ),
            "rh": (["pr"], raw_data[4], dict(long_name="Relative Humidity", units="%")),
            "u": (["pr"], raw_data[5], dict(long_name="Zonal-wind component")),
            "v": (["pr"], raw_data[6], dict(long_name="Meridional-wind component")),
        },
        coords={
            "time": pd.to_datetime(
                f"{year+1900:.0f}-{month:02.0f}-{day:02.0f} {hour}:00"
            ),
            # "nz": np.arange(raw_data[0].size),
            "pr": (["pr"], raw_data[0], dict(long_name="Pressure", units="hPa")),
        },
    )
    return xdata


def deriv_to_dataset(dataframe):
    year, month, day, hour, *_ = dataframe.iloc[0].values
    dataframe = dataframe.replace(-999, np.nan)
    raw_data = dataframe.iloc[2:]
    xdata = xr.Dataset(
        {
            "div": (
                ["pr"],
                raw_data[1],
                dict(long_name="Horizontal Divergence", units="1/s *10^6"),
            ),
            "w": (["pr"], raw_data[2], dict(long_name="Omega", units="mb/hr")),
            "q1": (
                ["pr"],
                raw_data[3],
                dict(long_name="Apparent Heating", units="K/day"),
            ),
            "q2": (
                ["pr"],
                raw_data[4],
                dict(long_name="Apparent Drying", units="K/day"),
            ),
        },
        coords={
            "time": pd.to_datetime(
                f"{year+1900:.0f}-{month:02.0f}-{day:02.0f} {hour}:00"
            ),
            # "nz": np.arange(raw_data[0].size),
            "pr": (["pr"], raw_data[0], dict(long_name="Pressure", units="hPa")),
        },
    )
    return xdata


# %%
basic_dfs = stacked_data(file_basic)
deriv_dfs = stacked_data(file_deriv)

xdata_basic = xr.concat([basic_to_dataset(x) for x in basic_dfs], dim="time")
xdata_deriv = xr.concat([deriv_to_dataset(x) for x in basic_dfs], dim="time")
# %%

# Save the data
xdata_basic.to_netcdf("basic_flds.nc")
xdata_deriv.to_netcdf("deriv_flds.nc")

# %%

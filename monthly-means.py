#!/usr/bin/env python3
__author__ = 'smw'
__email__ = 'smw@ceh.ac.uk'
__status__ = 'Development'

import os
import sys

from netCDF4 import Dataset, num2date
import pandas as pd
# from mpl_toolkits.basemap import Basemap
import numpy as np


def main():

    url = 'http://192.171.173.134/thredds/dodsC/chess/driving_data/aggregation/tas_aggregation'
    f = Dataset(url)
    print(f.variables)
    time = f.variables['time']
    print('\n\n', time)

    tmin, tmax = 0, 10000
    ymin, ymax = 400, 401
    xmin, xmax = 400, 401
    tas = f.variables['tas'][tmin:tmax, ymin:ymax, xmin:xmax]
    print('\n\n', tas.shape)

    # time = f.variables['time']
    # print(time)
    # START_DATE = time.units
    # print(START_DATE)
    # print(time[:])
    # dates = num2date(times=time[:], units=time.units, calendar=time.calendar)
    # print(dates)

    # lon = f.variables['lon'][:]
    # lat = f.variables['lat'][:]
    # lon, lat = np.meshgrid(lon, lat)

    dates = num2date(times=time[tmin:tmax], units=time.units)
    print('\n\n', dates)

    dates_pd = pd.to_datetime(dates)
    print('\n\n', dates_pd)
    periods = dates_pd.to_period(freq='D')
    print(periods)

    mask_1961 = periods.year==1961
    data = tas[mask_1961, :, :].mean(axis=0)
    print('\n\n', data.shape)








if __name__ == '__main__':
    main()

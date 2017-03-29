#!/usr/bin/env python3
__author__ = 'smw'
__email__ = 'smw@ceh.ac.uk'
__status__ = 'Development'

import os
import sys

from netCDF4 import Dataset, MFDataset, num2date
import pandas as pd
# from mpl_toolkits.basemap import Basemap
import numpy as np
import xarray as xr


def main():

    print("numpy version  : ", np.__version__)
    print("pandas version : ", pd.__version__)
    print("xarray version : ", xr.__version__)

    # method = 'THREDDS'
    # method = 'MULTI-FILE'
    method = 'XARRAY'

    if method == 'THREDDS':

        # Bastardised from:  http://earthpy.org/pandas_netcdf.html

        print('\n\n', method)

        url = 'http://192.171.173.134/thredds/dodsC/chess/driving_data/aggregation/tas_aggregation'
        f = Dataset(url)
        print(f.variables)
        time = f.variables['time']
        print('\n\n', time)
        print(time.shape)
        print(time.size)

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

        tmin, tmax, tstep = 0, time.size, 1

        dates = num2date(times=time[tmin:tmax], units=time.units)
        print('\n\n', dates)

        dates_pd = pd.to_datetime(dates)
        print('\n\n', dates_pd)
        periods = dates_pd.to_period(freq='D')
        print(periods)

        # mask_1961 = periods.year==1961
        # data = tas[mask_1961, :, :].mean(axis=0)
        # print('\n\n', data.shape)

        # ymin, ymax, ystep = 0, f.variables['y'].size, 1
        # xmin, xmax, xstep = 0, f.variables['x'].size, 1
        ymin, ymax, ystep = 400, 402, 1
        xmin, xmax, xstep = 400, 402, 1
        print('\n\nymin:{0}\t\tymax:{1}\t\tystep:{2}'.format(ymin, ymax, ystep))
        print('\n\nxmin:{0}\t\txmax:{1}\t\txstep:{2}'.format(xmin, xmax, xstep))

        NODATA = f.variables['tas']._FillValue
        print('\n\nNODATA:\t{0}'.format(NODATA))

        for y in range(ymin, ymax, ystep):
            for x in range(xmin, xmax, xstep):
                print('\ty:{0},\tx:{1}'.format(y, x))
                check = f.variables['tas'][0, y, x]
                print('\t\t', check, type(check))
                if type(check) == np.ma.core.MaskedConstant:
                    print('\t\tmasked')
                else:
                    print('\t\tnot masked')
                    tas = f.variables['tas'][tmin:tmax, y, x]
                    print('\t\t', tas.shape)
                    for month in range(1, 13, 1):
                        print('\t\t\tmonth:{0}'.format(month))
                        month_mask = periods.month == month
                        data = tas[month_mask].mean(axis=0)
                        print('\t\t\t', data)

        f.close()

    elif method == 'MULTI-FILE':

        # Doesn't work as the CHESS netCDF files are in NETCDF4 format.
        # Multi-file datasets works with NETCDF4_CLASSIC, NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET or NETCDF3_64BIT_DATA only.
        print('\n\n', method)

        netcdf_folder = r'Z:\eidchub\b745e7b1-626c-4ccc-ac27-56582e77b900'

        for year in range(1961, 2016, 1):
            for month in range(1, 13, 1):
                netcdf_file = r'chess_tas_{0}{1}.nc'.format(year, str(month).zfill(2))
                print('netcdf_file:\t{0}'.format(netcdf_file))
                f = Dataset(os.path.join(netcdf_folder, netcdf_file))
                print('\tf.file_format:\t{0}'.format(f.file_format))
                f.close()

        netcdf_file = r'chess_tas_*.nc'
        print(os.path.join(netcdf_folder, netcdf_file))
        f = MFDataset(os.path.join(netcdf_folder, netcdf_file), aggdim='time')
        print(f.variables['time'])
        print(f.variables['time'].shape)
        print(f.variables['time'].size)
        f.close()

    elif method == 'XARRAY':

        # Bastardised from:  http://xarray.pydata.org/en/stable/examples/monthly-means.html

        print('\n\n', method)

        variables_dict = {'dtr':     'Daily temperature range',
                          'huss':    'Specific humidity',
                          'precip':  'Rainfall',
                          'psurf':   'Air pressure',
                          'rlds':    'LW Radiation',
                          'rsds':    'SW Radiation',
                          'sfcWind': 'Wind speed',
                          'tas':     'Air temperature'
                          }

        for variable in variables_dict.keys():
            print('\n\nvariable:\t\t{0}'.format(variable))

            url = 'http://192.171.173.134/thredds/dodsC/chess/driving_data/aggregation/{0}_aggregation'.format(variable.lower())
            ds = xr.open_dataset(url)
            print(ds)

            ds_subset = ds[variable][:, 475:499, 325:349]
            print(ds_subset)

            # ds_month = ds_subset.groupby('time.month').mean(dim='time')
            # print(ds_month)
            # print(type(ds_month))
            #
            # out_netcdf_folder = r'E:\CountrysideSurvey\aidan-keith\netcdf'
            # out_netcdf_file = r'{0}_month.nc'.format(variable)
            # out_netcdf_file = os.path.join(out_netcdf_folder, out_netcdf_file)
            # ds_month.to_netcdf(path=out_netcdf_file, mode='w', format='NETCDF4')
            #
            # del ds_month
            # del ds_subset

            ds.close()




if __name__ == '__main__':
    main()

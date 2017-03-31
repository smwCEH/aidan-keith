#!/usr/bin/env python3
__author__ = 'smw'
__email__ = 'smw@ceh.ac.uk'
__status__ = 'Development'

import os
import sys

import pandas as pd

import netCDF4
# from netCDF4 import Dataset, MFDataset, num2date


print('netCDF4 version:\t{0}'.format(netCDF4.__version__))


def main():

    in_csv_file = r'E:\CountrysideSurvey\aidan-keith\CS_xplot_1km-smw01.csv'

    df = pd.read_csv(in_csv_file)
    print(df)
    print(df.describe)

    sys.exit()

    in_netcdf_folder = r'E:\CountrysideSurvey\aidan-keith\netcdf'

    variable_list = ['dtr', 'huss', 'precip', 'psurf', 'rlds', 'rsds', 'sfcWind', 'tas']

    for variable in variable_list:
        print('\n\nvariable:\t{0}'.format(variable))

        for month in range(1, 13, 1):
            print('\tmonth:\t{0}'.format(month))

            in_netcdf_file = '{0}_{1}.nc'.format(variable, str(month).zfill(2))
            in_netcdf_file = os.path.join(in_netcdf_folder, in_netcdf_file)
            print('\t\tin_netcdf_file:\t{0}'.format(in_netcdf_file))

            f = netCDF4.Dataset(in_netcdf_file)
            # print(f.variables)
            if variable == 'precip':
                print('[{0}][475, 325]:\t{1:.4e}'.format(variable,
                                                         float(f.variables[variable][475, 325])))
            else:
                print('[{0}][475, 325]:\t{1:.4f}'.format(variable,
                                                         float(f.variables[variable][475, 325])))
            f.close()


if __name__ == '__main__':
    main()

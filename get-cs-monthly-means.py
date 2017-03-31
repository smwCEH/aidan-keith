#!/usr/bin/env python3
__author__ = 'smw'
__email__ = 'smw@ceh.ac.uk'
__status__ = 'Development'

import os
import sys

import pandas as pd

import netCDF4
# from netCDF4 import Dataset, MFDataset, num2date


print('pandas version:\t{0}'.format(pd.__version__))
print('netCDF4 version:\t{0}'.format(netCDF4.__version__))


NODATA = -9999.9


def main():

    in_csv_file = r'E:\CountrysideSurvey\aidan-keith\CS_xplot_1km-smw01.csv'

    df = pd.read_csv(in_csv_file)
    print(df)
    print(df.describe())

    in_netcdf_folder = r'E:\CountrysideSurvey\aidan-keith\netcdf'

    variable_list = ['dtr', 'huss', 'precip', 'psurf', 'rlds', 'rsds', 'sfcWind', 'tas']
    # variable_list = ['dtr']

    for variable in variable_list:
        print('\n\nvariable:\t{0}'.format(variable))

        for month in range(1, 13, 1):
        # for month in range(1, 2, 1):
            print('\tmonth:\t{0}'.format(month))

            values_list = []

            in_netcdf_file = '{0}_{1}.nc'.format(variable, str(month).zfill(2))
            in_netcdf_file = os.path.join(in_netcdf_folder, in_netcdf_file)
            print('\t\tin_netcdf_file:\t{0}'.format(in_netcdf_file))

            f = netCDF4.Dataset(in_netcdf_file)
            # print(f.variables)
            print('\t\t\tf.variables[variable].shape:\t{0}'.format(f.variables[variable].shape))

            for index, row in df.iterrows():
                northing, easting = row['NORTHING'], row['EASTING']
                # print('\t\tnorthing:\t{0}\t\teasting:\t{1}'.format(northing, easting))

                ypixel, xpixel = int((northing - 500) / 1000), int((easting - 500) / 1000)
                # print('\t\typixel:\t{0}\t\txpixel:\t{1}'.format(ypixel, xpixel))

                if ypixel < f.variables[variable].shape[0] and xpixel < f.variables[variable].shape[1]:
                    y, x = f.variables['y'][ypixel], f.variables['x'][xpixel]
                    # print('\t\ty:\t{0}\t\tx:\t{1}'.format(y, x))
                    if northing != y or easting != x:
                        sys.exit('\n\n{0} northing or easting doesn\'t match y or x! {0}\n\n'.format('*' * 5))
                    values_list.append(f.variables[variable][ypixel, xpixel])
                else:
                    values_list.append(NODATA)

            f.close()

            df['{0}_{1}'.format(variable, str(month).zfill(2))] = values_list

    print(df)
    print(df.describe())

    out_csv_file = r'E:\CountrysideSurvey\aidan-keith\CS_xplot_1km-month-means.csv'
    df.to_csv(out_csv_file)



if __name__ == '__main__':
    main()

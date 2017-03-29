#!/usr/bin/env python3
__author__ = 'smw'
__email__ = 'smw@ceh.ac.uk'
__status__ = 'Development'

import os
import sys

import netCDF4


def main():

    url = 'http://192.171.173.134/thredds/dodsC/chess/driving_data/aggregation/tas_aggregation'
    dataset = netCDF4.Dataset(url)
    print(dataset.variables)





if __name__ == '__main__':
    main()

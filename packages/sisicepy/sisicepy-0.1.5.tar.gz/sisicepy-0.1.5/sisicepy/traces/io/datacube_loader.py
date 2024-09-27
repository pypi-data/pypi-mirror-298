import xarray as xr
import pyrocko.io
import numpy as np
from datetime import datetime, timezone, timedelta
import pandas as pd
import pint_xarray
import natsort
import glob
from pint_xarray import unit_registry as ureg

def load_datacube(adr,axis=[0]):
    '''
    Loader for DIGOS DataCube

    :param adr: Path to the DataCube file
    :type adr: str
    :param axis: List of axes to load
    :type axis: list of int
    :return: xarray Dataset containing the loaded data and metadata
    :rtype: xarray.Dataset
    '''

    data=pyrocko.io.load(adr,format='datacube')


    df=xr.Dataset()
    
    for i in axis:
        df['axis_'+str(i)]=xr.DataArray(data[i].ydata,dims='time')*ureg.bit
        for name in data[0].meta:
            df['axis_'+str(i)].attrs[name]=data[0].meta[name]
            df['axis_'+str(i)].attrs[name]=data[0].meta[name]
        
    ti=datetime.fromtimestamp(data[0].tmin,tz=timezone.utc)
    tf=datetime.fromtimestamp(data[0].tmax,tz=timezone.utc)
    df['time']=pd.date_range(ti,tf,data[0].data_len()).values
    
    
    for name in data[0].meta:
        df.attrs[name]=data[0].meta[name]
        df.attrs[name]=data[0].meta[name]
    
    return df

def load_mfdatacube(adr_list,**kwargs):
    '''
    Loader for DIGOS DataCube

    :param adr_list:
    :type adr_list: list
    '''

    data_list=[]
    for adr in adr_list:
        data_list.append(load_datacube(adr,**kwargs))

    return xr.concat(data_list,dim='time')

def open_day_datacube(path,day,**kwargs):
    '''
    Loader for DIGOS DataCube for a given day

    :param day: format %Y-%m-%d
    :type axis: str
    '''
    files=natsort.natsorted(glob.glob(path))
    # function to parse the path from datacube to string date
    def extract_date(file):
        fs = file.split('/')
        return '20' + fs[-2][0:2] + '-' + fs[-1][0:2] + '-' + fs[-1][2:4]

    formatted_dates = list(map(extract_date, files))

    ###########################################################
    # find file for the given day and one day before and afer #
    ###########################################################
    formatted_dates_dt = np.array([datetime.strptime(date, '%Y-%m-%d') for date in formatted_dates])

    # Define the target date (D-Day)
    target_date = datetime.strptime(day, '%Y-%m-%d')

    # Define the previous day and next day
    previous_day = target_date - timedelta(days=1)
    next_day = target_date + timedelta(days=1)

    # Use np.where to find indices for the target date, previous day, and next day
    indices = np.where(
        (formatted_dates_dt == target_date) |
        (formatted_dates_dt == previous_day) |
        (formatted_dates_dt == next_day)
    )

    #############
    # Open data #
    #############
    if len(indices[0]) != 0:
        di=day+'T00:00:00'
        df=next_day.strftime('%Y-%m-%d')+'T00:00:00'
        return load_mfdatacube(np.array(files)[indices[0]]).sel(time=slice(di,df),**kwargs)
    else:
        print('No data at this date !')


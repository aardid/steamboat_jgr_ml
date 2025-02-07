"""Utilities package for puia."""

__author__ = """Alberto Ardid and David Dempsey"""
__email__ = 'aardids@gmail.com'
__version__ = '0.1.0'


import pickle, os
import pandas as pd
from datetime import datetime
from pandas._libs.tslibs.timestamps import Timestamp
import numpy as np
try:
    from obspy import UTCDateTime
    failedobspyimport = False
except:
    failedobspyimport = True

class DummyClass(object):
    # for mocking other classes
    def __init__(self,**kwargs):
        [self.__setattr__(*item) for item in kwargs.items()]

def makedir(name): 
    os.makedirs(name, exist_ok=True)

def datetimeify(t):
    """ Return datetime object corresponding to input string.
        Parameters:
        -----------
        t : str, datetime.datetime
            Date string to convert to datetime object.
        Returns:
        --------
        datetime : datetime.datetime
            Datetime object corresponding to input string.
        Notes:
        ------
        This function tries several datetime string formats, and raises a ValueError if none work.
    """
    if type(t) in [datetime, Timestamp]:
        return t
    if not failedobspyimport:
        if type(t) is UTCDateTime:
            return t._get_datetime()
    fmts = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y %m %d %H %M %S',]
    for fmt in fmts:
        try:
            return datetime.strptime(t, fmt)
        except ValueError:
            pass
    raise ValueError("time data '{:s}' not a recognized format".format(t))

def save_dataframe(df, fl, index=True, index_label=None):
    ''' helper function for saving dataframes
    '''
    if fl.endswith('.csv'):
        df.to_csv(fl, index=index, index_label=index_label)
    elif fl.endswith('.pkl'):
        fp = open(fl, 'wb')
        pickle.dump(df,fp)
    elif fl.endswith('.hdf'):
        df.to_hdf(fl, 'test', format='fixed', mode='w')
    else:
        raise ValueError('only csv, hdf and pkl file formats supported')

def load_dataframe(fl, index_col=None, parse_dates=False, usecols=None, infer_datetime_format=False, 
    nrows=None, header='infer', skiprows=None):
    ''' helper function for loading dataframes
    '''
    if fl.endswith('.csv'):
        df = pd.read_csv(fl, index_col=index_col, parse_dates=parse_dates, usecols=usecols, infer_datetime_format=infer_datetime_format,
            nrows=nrows, header=header, skiprows=skiprows, dayfirst=True)
    elif fl.endswith('.pkl'):
        fp = open(fl, 'rb')#'rb')
        df = pickle.load(fp)
    elif fl.endswith('.hdf'):
        df = pd.read_hdf(fl, 'test')
    else:
        raise ValueError('only csv and pkl file formats supported')

    if fl.endswith('.pkl') or fl.endswith('.hdf'):
        if usecols is not None:
            if len(usecols) == 1 and usecols[0] == df.index.name:
                df = df[df.columns[0]]
            else:
                df = df[usecols]
        if nrows is not None:
            if skiprows is None: skiprows = range(1,1)
            skiprows = list(skiprows)
            inds = sorted(set(range(len(skiprows)+nrows)) - set(skiprows))
            df = df.iloc[inds]
        elif skiprows is not None:
            df = df.iloc[skiprows:]
    return df

def _is_eruption_in(days, from_time, tes):
    """ Binary classification of eruption imminence.
        Parameters:
        -----------
        days : float
            Length of look-forward.
        from_time : datetime.datetime
            Beginning of look-forward period.
        tes: list of datetimes
            Eruptive times
        Returns:
        --------
        label : int
            1 if eruption occurs in look-forward, 0 otherwise
    """
    for te in tes:
        if 0 < (te-from_time).total_seconds()/(3600*24) < days:
            return 1.
    return 0.

    from random import randrange
from datetime import timedelta

def random_date(start, end, set_seed=None):
    """Function  return a random datetime between two datetime objects.
        Parameters:
        -----------
        start : datetime.datetime
            
        end : datetime.datetime
            
        Returns:
        --------
        date : datetime.datetime
            
    """
    from random import seed
    from random import randrange
    seed(set_seed) if set_seed else seed(237)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    _t=start + timedelta(seconds=random_second)
    return start + timedelta(seconds=random_second)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]
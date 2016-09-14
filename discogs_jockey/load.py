""" load
Module for loading record collections from various data sources, to be
later processed by `collection` module. Current data sources are a .csv
exported from Discogs, as well as directly from discogs via the API.
"""
import os
import pandas as pd
from .exceptions import NoData

def load_from_dir(fdir='collection'):
    """ Return a pandas DataFrame of a csv in `fdir`.
    
    Note: chooses an arbitrary file if multiple encountered. 
    """
    # Get filepaths of all matching files
    fpaths = [os.path.join(fdir, fname) for fname in os.listdir(fdir)
            if os.path.splitext(fname)[1].lower().endswith('csv')]
    if not fpaths:
        raise NoData('No {} files found in {} directory'.format(exts, fdir))
    
    # Process first file (though should combine all)
    fpath = fpaths[0]
    df = pd.read_csv(fpath)
    
    return df

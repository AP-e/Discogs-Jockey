""" collection 

Module for loading a collection from various sources to a shelf of Records.
Note that discogs server requests should be rate limited.
"""
from discogs_client.models import Release, CollectionFolder
from collections import OrderedDict
from pandas import DataFrame, Series
import random

class Record(object):
    """ A vinyl record, do not leave in direct sunlight. """
    
    def __init__(self, release):
        if isinstance(release, Release): # from discogs client
            self._initialise_from_release(release)
        elif isinstance(release, Series): # from csv
            self._initialise_from_series(release)
        elif isinstance(release, dict): # user defined
            self._initialise_from_dict(release)
        else:
            raise TypeError('Invalid release type: {}'.format(type(release)))
    
    def _initialise_from_dict(self, details):
        """ Assign Record info from dict of release details."""
        
        # Directly assign release details
        for attr in ['release_id', 'title', 'artists', 
                'cat_nums', 'labels', 'year']:
            setattr(self, attr, details.pop(attr))

        if details: # ensure no superfluous info
            raise TypeError("Unused release details {}".format(
                    list(details.keys())))

    def _initialise_from_release(self, release):
        """ Assign Record info from discogs_client.models.Release object."""
        
        self.release_id = release.id
        self.title = release.title
        self.artists = [artist.name for artist in release.artists]
        self.labels, self.cat_nums = zip(*[(label.data['name'],
                label.data['catno']) for label in release.labels]) #append loop
        self.year = release.year

    def _initialise_from_series(self, series):
        """ Assign Record from pandas.core.series.Series object """
        
        self.release_id = series['release_id']
        self.title = series['Title']
        self.artists = series['Artist']
        self.labels = series['Label'].split(',')
        self.cat_nums = series['Catalog#'].split(',')
        self.year = series['Released']


class Crate():
    """ An old milk crate, repurposed for holding Records."""
    
    def __init__(self):
        """ Store records as {release_id: `Record`}. """
        self.records = OrderedDict()
    
    def __len__(self):
        return len(self.records)
    
    def add_records(self, records):
        """ Add records (single or iterable)."""

        # Coerce single record to iterable
        try:
            records = iter(records)
        except(TypeError):
            records = [records]

        # Add records to collection
        for record in records:
            self.records[record.release_id] = record
   
    def pick_records(self, ids):
        """ Remove and return specific records.
        
        Args:
            ids ::: iterable of release_ids of records to return
        Returns:
            records ::: list of Record objects
        """
        return [self.records.pop(id) for id in ids]

    def random_records(self, n):                                                    
        """ Return list of `n` records removed at random.
        
        `n` will be coerced to be < len(self.records)
        """                                          
        # Don't try and pick more records than there are                           
        n = min(len(self), n)

        records = []
        for i in range(n):
            # Randomly pop record
            pick = random.choice(list(self.records.keys()))                          
            records.append(self.records.pop(pick))
        
        return records
    
    def empty(self):
        """ Remove all records and return them as list. """
        return [self.records.popitem()[1]
                for i in range(len(self))]


class Shelf(Crate):
    """ A shelf to hold Records. """

    # Acceptable and unacceptable release formats
    formats = {'good': ['Vinyl'],
               'bad': ['CD', 'CDr', 'DVD', 'USB', 'Cass', 'Cassette', 'File',
                       'MP3', 'WAV', 'FLAC']}
    
    def __init__(self, collection):
        """ Fill shelf with Records from either csv or discogs collection."""
        
        super().__init__()  
        if collection is None:
            pass # let shelf remain empty
        elif isinstance(collection, CollectionFolder):
            self._initialise_from_folder(collection)
        elif isinstance(collection, DataFrame): # from pandas
            self._initialise_from_df(collection)
        else:
            raise TypeError('Invalid collection type: {}'.format(
                    type(collection)))

    def _initialise_from_folder(self, folder):
        """ Coerce discogs_client.models.CollectionFolder to Records."""

        # Extract Release objects from folder
        records = {} # ids as keys to merge copies
        for item in folder.releases:
            release = item.release
            # Only store wax (i.e. exclude CDs, Tapes, MP3s etc)
            formats = [format['name'] for format in release.formats]
            if not set(formats).isdisjoint(Shelf.formats['good']):
                self.records[release.id] = release
        
        self.records = records

    def _initialise_from_df(self, df):
        """  Coerce pandas.core.frame.DataFrame object to Records. """
        for i, release in df.iterrows():
            # Exclude non-wax releases
            formats = release['Format'].split(',')
            if set(formats).isdisjoint(Shelf.formats['bad']):
                self.records[release['release_id']] = Record(release)
   

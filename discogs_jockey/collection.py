""" collection 

Module for loading a collection from various sources to a shelf of Records.
Note that discogs server requests should be rate limited.
"""
from discogs_client.models import Release, CollectionFolder
from pandas import DataFrame

class Record(object):
    """ A vinyl record, do not leave in direct sunlight. """
    
    def __init__(self, release):
        if isinstance(release, Release):
            self._initialise_from_release()
        elif isinstance(release, dict):
            self._initialise_from_dict()
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
                label.data['catno']) for label in release.labels]) # append loop
        self.year = release.year


class Shelf():
    """ A shelf to hold Records. """

    # Acceptable and unacceptable release formats
    formats = {'good': ['Vinyl'],
               'bad': ['CD', 'CDr', 'DVD', 'USB', 'Cass', 'Cassette', 'File',
                       'MP3', 'WAV', 'FLAC']}
    
    def __init__(self, collection):
        """ Fill shelf with Records from either csv or discogs collection."""
    
        if isinstance(collection, CollectionFolder):
            self._initialise_from_folder(collection)
        elif isinstance(collection, DataFrame): # from pandas
            initialise_from_df(collection)
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
                records[release.id] = release
        
        self.records = records

    def _initialise_from_df(self, df):
        """  Coerce pandas.core.frame.DataFrame object to Records. """
        NotImplemented 

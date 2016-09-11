""" collection 

Module for loading a collection from various sources to a shelf of Records
"""
from discogs_client import Release

class Record(object):
    """ A vinyl record, do not leave in direct sunlight. """
    def __init__(self, release):
        if isinstance(release, Release):
            self._initialise_from_release()
        elif isinstance(release, dict):
            self._initialise_from_dict()
        else:
            raise TypeError('Invalid release type: {}'.format(type(release))
    
    def _initialise_from_dict(self, details):
        """ Assign Record info from dict of release details."""
        
        for attr in ['release_id', 'title', 'artists', 
                'cat_nums', 'labels', 'year']:
            setattr(self, attr) = details.pop(attr)
        
        if details:
            raise TypeError("Unused release details {}".format(
                    list(details.keys()))

    def _initialise_from_release(self, release):
        """ Assign Record info from discogs_client.models.Release object."""
        
        self.release_id = release.id
        self.title = release.title
        self.artists = [artist.name for artist in release.artists]
        self.labels, self.cat_nums = zip(*[(label.data['name'],
                label.data['catno']) for label in release.labels]) # append loop
        self.year = release.year



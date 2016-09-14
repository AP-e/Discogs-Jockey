""" exceptions

Custom Exceptions for discogs_jockey.
"""

class NoData(OSError):
    """ .tv"""
    pass

class StopPlaying(Exception):                                                   
    """ Used to process a quit request."""                                      
    pass

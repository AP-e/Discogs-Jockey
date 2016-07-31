#!/usr/bin/env python

""" Discogs Jockey """

import csv
from numpy import random
import os
from glob import glob

class StopPlaying(Exception):
    """ Used to process a quit request."""
    pass


class NoData(IOError):
    """.tv"""
    pass


class Record(object):
    """ A vinyl record. Do not leave in direct sunlight. """
    def __init__(self, catalog_number, artist, title, label, year, release_id):
        self.catalog_number = catalog_number
        self.artist = artist
        self.title = title
        self.label = label
        self.year = year
        self._id = release_id

def play_discogs_jockey(collection=None, crate_size=3, replace=False):
    """ Start the Discogs Jockey challenge.
    Args:
        collection ::: str path to record collection (.csv file exported from Discogs)
                        use `None` to autodetect from `./collection/`
        crate_size ::: int maximum number of records user can choose from (default 3)
        replace ::: bool whether unplayed records get put back on the shelf, off by default
    """
    shelf = initialise_shelf(collection)
    start_set(shelf, crate_size, replace)

def start_set(shelf, crate_size, replace):
    """ Starts a Discogs Jockey challenge with the records on the shelf and the specified rules. 
    Args:
        shelf ::: list of Record objects
        crate_size, replace ::: game rules 
    Returns:
        history ::: dict of of played and rejected records for each round
    """
    
    n_round = 0
    history = {}
    
    # Play rounds until no more records
    while len(shelf) > crate_size:  
        print  '\n ~~~ Starting next selection ~~~ \n'
        try:
            record, crate = play_round(shelf, crate_size, replace)
        except StopPlaying:
            break

        history[n_round] = {'played': record, 'rejected': crate}
        n_round += 1
        
    display_finish(history)
    
    return history

def initialise_shelf(fpath):
    """ Create a shelf of virtual records from specified .csv file, or first file in `./collection/ directory` """
   
    # Automatically use file in collection directory
    if not fpath:
        data_dir = 'collection'
        try:
            fpath = glob(os.path.join(data_dir , '*.csv'))[0]
        except IndexError:
            raise NoData, 'No .csv files found in %s directory' % data_dir
    
    # Read csv to list
    with open(fpath) as csvfile:
        table = [row for row in csv.reader(csvfile.readlines())]
    headers = table.pop(0) # get rid of header row

    # ! Should do a check that headers contain correct information, and map header names to rows, passing a table with rowmap + relevant rows only
    shelf = fill_shelf(table)
    
    return shelf

def fill_shelf(table, bad_formats = ['CD', 'CDr', 'DVD', 'USB', 'Cass', 'Cassette', 'File', 'MP3', 'WAV', 'FLAC']):
    """ Return a list of Record objects created from a table (Discogs collection)."""
    # non-vinyl formats
    shelf = [] # to store all records
    
    # Create and add records to shelf
    for row in table:
        release_format = row[4].split(', ')[0]
        if release_format not in bad_formats: # vinyl only
            record_info = {'catalog_number': row[0],'artist': row[1], 'title': row[2], 'label': row[3], 'year': row[6], 'release_id': row[7]}
            record = Record(**record_info)
            shelf.append(record)
    return shelf

def play_round(shelf, crate_size, replace):
    """ One round of the game."""
    
    # Choose a record
    record, crate = make_selection(shelf, crate_size)
    
    display_choice(record)    
    
    if replace:     # put unchosen records back on the shelf
        shelf.extend(crate.values())
        
    return record, crate

def make_selection(shelf, max_options):
    """ Repeatedly pulls draws records from the shelf until user chooses an option.

        Args:
            shelf ::: list of Records to draw from 
            max_options ::: int times to draw before forcing selection
        Returns:
            record ::: Record object chosen by user
            options ::: 
    """
    # A small crate to keep choices
    crate = {}

    for i in range(1, max_options+1): # use human indexing

        # Put random record in crate and display to user
        option = draw_from_shelf(shelf)
        crate[i] = option
        #display_option(option, i)
        display_crate(crate)
        choice = ask_to_choose(crate)
        if choice:
            break
        elif i == max_options:
            while choice is None:
                display_crate(crate)
                choice = ask_to_choose(crate)
        else: continue

    # Chosen record
    record = crate.pop(choice)
    
    return record, crate

def draw_from_shelf(shelf):
    """ Return a random record removed from the shelf. """
    rand = random.randint(len(shelf))
    record = shelf.pop(rand)
    return record

def ask_to_choose(crate):
    """ Ask user to choose a record from the crate, returning either a valid key int to choose,`None` to continue a request to quit"""
    question = "Choose a record from %s \n(<Enter> to draw again, `Q` to quit)}" % crate.keys()
    choice = raw_input(question)
    
    try:
        choice = int(choice)
    except ValueError: 
        if choice.lower() in ['q', 'quit', 'exit', 'stop']: # quit request
            raise StopPlaying, 'User requested to quit'
    
    # Only return a valid key
    return choice if choice in crate.keys() else None

def describe_record(record):
    """ Return a two-line description of the record (Artist -- Title, [Label -- CAT#]."""
    line1 = ' -- '.join((record.artist, record.title)) + ' (%s)' % record.year
    line2 = '[%s -- %s]' % (record.label, record.catalog_number)
    
    return '\n'.join((line1, line2))

def display_option(option, k):
    """ Show user the option and the number."""
    print '\n\t\t > %s <\n'% k, describe_record(option), '\n'
    
def display_crate(crate):
    """ Print current options to user. """
    print '\n'*3, '\t\t YOU HAVE THE FOLLOWING OPTIONS:\n', '_'*60,
    for k, option in crate.iteritems():
        display_option(option, k)
    print '_'*60, '\n'*3
    
def display_choice(record):
    """ Inform user of chosen record, with lots of spacing."""
    print '\n'*3 + '\t\t YOU CHOSE TO PLAY:'
    print '*'*70 + '\n\t','\n\t'.join(describe_record(record).split('\n')), '\n' + '*'*70 + '\n'*3
    
def display_finish(history):
    """ Inform user that game is over."""
    print '\n', '#'*60
    print "%s records played.\nI'll have a glass of water please, mate." % len(history)

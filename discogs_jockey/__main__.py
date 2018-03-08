#!/usr/bin/env python

import sys
from discogs_jockey.exceptions import NoData, StopPlaying
from discogs_jockey.collection import Record, Crate, Shelf
from discogs_jockey.interactor import TerminalInteractor
from discogs_jockey.load import load_from_dir
from discogs_jockey.game import Game
from discogs_jockey.discogs_api import get_collection_from_discogs
from discogs_client.exceptions import HTTPError

# Initialise interactor
io = TerminalInteractor()

# Game parameters
crate_size = 5 # How many records can you choose from?
replace = False # Should unplayed records be put back on the shelf?

def get_collection_offline():
    # Load csv collection to shelf
    fdir = "collection"
    df = load_from_dir(fdir)
    return df

def get_collection_online():
    # Get a collection
    try:
        collection = get_collection_from_discogs(io)
    except HTTPError: # it's not possible to get anything other than code 400
        print('Authorisation failed, try again?') # or upload collection, etc    
    return collection

collection = get_collection_online()
if not collection.releases:
    print("You don't have any records in your collection!")
    print("Quitting...")
    sys.exit()

# Load up shelf
shelf = Shelf(collection)
print("{} records loaded from your collection to the shelf, let's play!".format(len(collection.releases)))
game = Game(shelf, TerminalInteractor())
game.play_set() 

# Play discogs jockey game
game = Game(shelf, io, rules={'cap': crate_size, 'replace': replace})
game.play_set()
sys.exit()

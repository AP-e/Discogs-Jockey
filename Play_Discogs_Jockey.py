#!/usr/bin/env python

import sys
from discogs_jockey.exceptions import NoData, StopPlaying
from discogs_jockey.collection import Record, Crate, Shelf
from discogs_jockey.interactor import TerminalInteractor
from discogs_jockey.load import load_from_dir
from discogs_jockey.game import Game

# Initialise interactor
io = TerminalInteractor()

# Game parameters
crate_size = 5 # How many records can you choose from?
replace = False # Should unplayed records be put back on the shelf?

# Load collection to shelf
fdir = "collection"
df = load_from_dir(fdir)
shelf = Shelf(df)

# Play discogs jockey game
game = Game(shelf, io, rules={'cap': crate_size, 'replace': replace})
game.play_set()

sys.exit()

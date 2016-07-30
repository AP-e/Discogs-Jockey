#!/usr/bin/env python

from discogs_jockey import play
from discogs_jockey.discogs_jockey import NoData

# Game parameters
fpath = None # Which .csv file?
crate_size = 5 # How many records can you choose from?
replace = True # Should unplayed records be put back on the shelf?

print "* * * Enjoy your set! * * *"

try:
    play(fpath, crate_size, replace)
except NoData:
    print "You need to put your Discogs collection .csv file in a folder called collection."

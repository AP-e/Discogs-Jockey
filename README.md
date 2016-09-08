# Discogs-Jockey
A tool to help DJs to train their mixing using a DJing challenge. 

### Quick start ###
Either install this package, or just download it and work from inside the Discogs-Jockey directory. Export your collection from Discogs as a .csv file, and put it in a directory called `collection`. Then run `Play_Discogs_Jockey.py` using Python.

## The challenge ##

The rules of the challenge are pretty simple: you play a set in which each record played must to be chosen from a small pool of records drawn randomly from their Discogs collection. The idea is to force the DJ to practice their mixing skills by limiting choice.

The challenge proceeds as following:

1. A record is drawn at random from the `shelf` (the full collection) and place in the `crate`.
2. DJ can continue, or request more records be drawn up to a limit (`crate_size` option).
3. DJ chooses any record in the `crate` and mixes it in.
4. Records remaining in the crate are either discarded or returned to the shelf (`replace` option).

This continues, each round starting with a fresh crate, until the shelf is empty or DJ decides to finish.
__
## To do list

### Point scoring
It would be good to disincentivise drawing the maximum allowed number of records, so a points system could be used. Take an example in which `crate_size=5`; the following could be awarded at each round:

| n records drawn | Points |
|-----------------|--------|
|       1         |   3    |
|      2-3        |   2    |
|      4-5        |   1    |

### Alternative challenge
As an alternative to emptying the crate at each round, discarding unplayed records could stay in the crate, taking up space so that the DJ is eventually forced to choose one of them. However, they can earn the right to remove an unplayed record every few rounds or so.

### To do
Nobody wants to have to open their laptop and run a python script while DJing. Discogs Jockey can be made into a proper app by implementing the following improvements:
- ~~Convert from Python 2.7 to 3.5~~ DONE
- Use the Discogs API to retreive user collection
- Develop a simple GUI with PyQT
- Display cover art and tracklisting
- Allow interaction by clicking/touch
- Port to Android and iOS

Look after your ears, tinnitus is no joke.

""" game

The Discogs Jockey game.
"""
from .collection import Record, Crate, Shelf
from .exceptions import StopPlaying

class Game():                                                          
    """ The discogs_jockey game."""                                          
    
    def __init__(self, shelf, io, rules={'cap': 3, 'replace': True}):
        """
        Args:
            shelf ::: initialised `discogs_jockey.collection.Shelf` object
            io ::: initialised `discogs_jockey.interactor.Interactor` instance
            rules ::: dict of game rules
                    : 'cap' : int max number of records to draw per round
                    : 'replace : bool to replace unplayed records to crate
        """

        self.shelf = shelf
        self.io = io
        self.crate = Crate() # used to store options of records to play
        self.round = 1
        self.history = {}
        self.cap = rules['cap']
        self.replace = rules['replace']
    
    def play_set(self):
        """ Play a set of the discogs jockey game."""
        
        # Play rounds until no more unplayed records, or user requests quit
        while len(self.shelf):
            try:
                self.play_round()
                self.round += 1
            except(StopPlaying):
                break
        
        # Display post-set information
        self.io.display_finished()
        self.io.display_history(self.history)
    
    def play_round(self):
        """ A single round of discogs jockey game."""
        
        crate = self.crate
        
        # Start round
        choice = None # release_id of chosen record 
        self.io.display_new_round(self.round)
        while choice is None:
            # Draw a record and display
            if len(self.shelf) and len(crate) < self.cap:
                record = self.shelf.random_records(1)
                self.crate.add_records(record) 
                self.io.display_option(*record)
            else: 
                self.io.display_cap_reached(self.cap)
            
            # Request user to choose
            self.io.display_crate(crate)
            choice = self.io.get_choice(crate)
        
        # Process choice
        record = crate.pick_records([choice])
        unplayed = crate.empty()
        self.add_to_history(record, unplayed) # not implemented yet
        
        # Replace unplayed records to shelf
        if self.replace:
            self.shelf.add_records(unplayed)
        
        self.io.display_choice(*record) # not implemented yet
        
    def add_to_history(self, played, unplayed):
        """ Store information about current round in history.
        Args:
            played, unplayed ::: lists of Record objects
        """

        round_info = {'played': played, 'unplayed': unplayed}
        self.history[self.round] = round_info

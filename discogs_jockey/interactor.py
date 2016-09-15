""" interactor
Module for interaction with user, including entry of collection
information, display of game output and retrieval of user input in-game.
"""
import abc
from .exceptions import StopPlaying

class Interactor:
    """ Abstract Base Class for object defining user interaction methods.

    Other modules rely on the existence of an `interactor` variable
    containing all of these methods.

    Highly incomplete.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def display_choice(self, record):
        """ Present a choice of record to user. """
        NotImplemented

    @abc.abstractmethod
    def display_new_round(self, roundn):
        """ Inform user that new round (number `roundn`) has started."""
        NotImplemented

    @abc.abstractmethod
    def display_crate(self, crate):
        """ Display records in crate to user for selection. """
        NotImplemented

    @abc.abstractmethod
    def display_option(self, record):
        """ Present the drawn option to user."""
        NotImplemented

    @abc.abstractmethod
    def get_choice(self, crate):
        """ Return the release_id of a record in crate chosen by user input."""
        NotImplemented

    @abc.abstractmethod
    def display_cap_reached(self, cap):
        """ Inform user that no more records can be added to crate."""
        NotImplemented

    @abc.abstractmethod
    def display_history(self, history):
        """ Present the played and rejected records per round."""
        NotImplemented

    @abc.abstractmethod
    def request_username(self):
        """ Prompt user to enter their discogs username."""
        NotImplemented

    @abc.abstractmethod
    def bad_username(self, username):
        """ Inform user that their username has not been recognised. """
        NotImplemented
    
    @abc.abstractmethod
    def greet_user(self, user):
        """ Confirm user has been found on discogs. """
        NotImplemented
     
class TerminalInteractor(Interactor):
    """ Methods to display info to, and get input from, user.
    Must have:
    """
    def __init__(self):
        "Should also allow formatting options to be set"

        self.quitflags = ['q', 'quit', 'exit', 'stop']
        self.starline = '*'*70 # a line of *****
        self.scoreline = '_'*70 # a line of _____
        self.gap3 = '\n'*3 # a 3 line gap

    def _make_options(self, crate):
        """ Return dict of {'k': (release_id, record)} from crate."""
        return {k+1: option for k, option in enumerate(crate.records.items())}

    def describe_record(self, record):
        """ Return a three-line description of the record
            TITLE
            ARTISTS
            LABEL1 [CAT1], LABEL2 [CAT2]
        """

        title = record.title
        artists = record.artists
        labcats = [" ".join([lab.strip(), '[{}]'.format(catn.strip())])  # "label [catnum]"
                for lab, catn in zip(record.labels, record.cat_nums)]
        labcats = ", ".join(labcats)

        return '\n'.join((title, artists, labcats))

    def display_record(self, record):
        """ Show a record to user. """
        print(self.describe_record(record))

    def display_choice(self, record):
        """ Inform user of chosen record, with lots of spacing."""
        print(self.gap3 + '\t\t You chose:' + '\n' + self.starline)
        print(self.describe_record(record))
        print(self.starline + '\n'*3)

    def display_new_round(self, roundn):
        """ Inform user that new round has started."""
        print('\n' + '~~~ Round {} ~~~'.format(roundn) + '\n')

    def display_crate(self, crate):
        """ Print current options to user. """

        options = self._make_options(crate)

        # Display options
        print('\n'*3 + '\t\t You have the following options:\n' + self.scoreline)
        for k, (id, record) in sorted(options.items()): # sort just in case
            self.display_option(record, k)

    def display_option(self, record, k=None):
        """ Show an option to user, with optional choice number `k`.
        Nothing done if no `k`.
        """

        # Supress output if not called with option number to prevent repetition
        if k is None:
            return

        print('\n\t\t > {} <'.format(k))
        self.display_record(record)

    def get_choice(self, crate):
        """ Return the release_id of a record in crate chosen by user input."""

        options = self._make_options(crate)
        ks = sorted(options.keys())

        q_start = "Choose a record"
        opts = ["<{}> to choose".format(ks), "<Enter> to draw again",
                "<Q> to quit"]
        q_opts = '(' + ", ".join(opts) + ')'
        k = input(q_start + '\n' + q_opts)

        try:
            k = int(k)
        except ValueError:
            if k.lower() in self.quitflags: # quit request
                raise StopPlaying('User requested to quit')

        release_id, record = options.get(k, (None, None))

        return release_id

    def display_cap_reached(self, cap):
        """ Inform user that no more records can be added to crate."""
        msg = "You can only choose from {} records".format(cap)
        print(self.starline + '\n' + msg + '\n' + self.starline)

    def display_finished(self):
        """ Inform user that game has finished. """
        msg = "You have finished your set!"
        print(self.starline + '\n' + msg + '\n' + self.starline)

    def display_history(self, history):
        """ Show the record history (i.e. tracklist)."""
        print("You spun {} records:".format(len(history)) + '\n')
        for k, round in sorted(history.items()):
            self.display_new_round(k)
            self.display_record(*round['played'])
 
    def request_username(self):
        """ Prompt user to enter their discogs username."""
        username = input("Please enter your Discogs username:")
        return username

    def bad_username(self, username):
        """ Inform user that their username has not been recognised. """
        NotImplemented
        print("Discogs username '{}' not found, please try again.".format(
                username.lower()))
    
    def greet_user(self, user):
        """ Confirm user has been found on discogs. """
        print("Hello {}.".format(user.username))

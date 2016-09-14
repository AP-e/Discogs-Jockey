""" interactor
Module for interaction with user, including entry of collection
information, display of game output and retrieval of user input in-game.
"""
from abc import ABCMeta

class Interactor:
    """ Abstract Base Class for object defining user interaction methods.

    Other modules rely on the existence of an `interactor` variable 
    containing all of these methods.

    Highly incomplete.
    """
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def display_something(self, some_parameter):
        """ Description of expected behaviour."""

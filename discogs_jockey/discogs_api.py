""" discogs_api

module for interacting with the discogs server via the discogs_client
"""

from discogs_client import Client
from discogs_client.exceptions import HTTPError
from discogs_jockey.interactor import TerminalInteractor
import os

def make_app_client():
    """ Return the discogs client authorised to Discogs_Jockey. """
    # Retrieve credentials from environmental variables
    consumer_key = os.environ['DISCOGS_JOCKEY_CONSUMER_KEY']
    consumer_secret = os.environ['DISCOGS_JOCKEY_CONSUMER_SECRET']
    user_agent = 'discogs_jockey/0.1' # should also be an env var
    
    # Set up client
    client = Client(user_agent, consumer_key, consumer_secret)
    
    return client

def get_user(client, io):
    """ Return an (unauthorised) user client from user supplied username.
    Args:
        client ::: a `discogs_client.client.Client` instance (unauthorised)
        io ::: a `discogs_jockey.interactor.Interactor' instance
    Returns:
        user ::: a `discogs_client.models.User` instance (unauthorised)
    """
    # Intialise user client
    user = None
    while user is None:
        username = io.request_username()
        user = client.user(username)
        # Test for existence
        try:
            user_id = user.id # try and access a user variable
        except(HTTPError):
            io.bad_username(username)
            user = None

    io.greet_user(user)
    return user

def get_authorisation_code(client, io):
    """ Return the authorisation code for `client` requested from user.
    Args:
        client ::: a `discogs_client.client.Client` instance (unauthorised)
    Returns:
        auth_code ::: user-supplied authorisation code from link
    """
    request_token, request_secret, auth_url = client.get_authorize_url()
    auth_code = io.request_authorisation(auth_url)
    return auth_code.strip()

def get_authorisation(io):
    """ Get an authorised user and client from user.
    Returns:
        client ::: a `discogs_client.client.Client` instance (authorised)
        user ::: a `discogs_client.models.User` instance (authorised)
    """
    client = make_app_client()
    auth_code = get_authorisation_code(client, io)
    token, secret = client.get_access_token(auth_code) # store access keys if needed
    user = client.identity() # authorised user
    return client, user

def get_collection_from_discogs(io):
    """ Return a user's collection from discogs, verifying if necessary.
    Args:
        io ::: a `discogs_jockey.interactor.Interactor' instance
    Returns:
        collection ::: `discogs_client.models.CollectionFolder` instance
                        always the 'all' folder
    """
    client = make_app_client()
    user = get_user(client, io)
    
    # Try to access collection
    try:
        collection = user.collection_folders[0] # 0 is folder `all`
    except(HTTPError) as err:
        errcode = err.args[1] # extract the error code
        if errcode == 401: # only handle Authentication Error
            # Seek authorisation
            client, user = get_authorisation(io)
            collection = user.collection_folders[0]
        else: # pass on any other errors
            raise err

    return collection

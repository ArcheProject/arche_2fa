from zope.interface import Attribute
from pyramid.interfaces import IDict


class ITwoFactAuthHandler(IDict):
    name = Attribute("Name of this method, must be unique")
    title = Attribute("Human readable title, should be a translation-string")
    has_valid_tokens = Attribute("Does this session contain valid tokens? (Returns int count)")

    def __init__(context, request):
        """ Adapt root and a request. """

    def create_token(userid, length = 5, charpool =  '', minutes = 10):
        """ Create a new token. """

    def send(userid, view):
        """ Send tokens with whatever method this adapter uses. """

    def validate(value):
        """ Validate, also checks that the token hasn't expired. """

    def cleanup():
        """ Remove any tokens that has expired. """

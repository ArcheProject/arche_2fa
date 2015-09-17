from zope.interface import Interface
from pyramid.interfaces import IDict


class ITwoFactAuthHandler(IDict):

    def __init__(context, request):
        """ Adapt root and a request. """

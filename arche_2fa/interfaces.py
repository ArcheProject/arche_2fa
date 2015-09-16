from zope.interface import Interface


class ITwoFactAuthHandler(Interface):

    def __init__(context, request):
        """ Adapt root and a request. """

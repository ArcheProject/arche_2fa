from zope.interface import implementer

from arche_2fa.interfaces import ITwoFactAuthHandler



@implementer(ITwoFactAuthHandler)
class TwoFactAuthHandler(object):
    name = ''
    title = ''

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def available(self, userid):
        pass

    def send(self, userid):
        pass

    def validate(self, userid, value):
        pass

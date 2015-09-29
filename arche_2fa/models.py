from __future__ import unicode_literals
from UserDict import IterableUserDict
from datetime import timedelta
from random import choice
import string

from arche.interfaces import IRoot
from arche.interfaces import IWillLoginEvent
from arche.utils import utcnow
from pyramid.interfaces import IRequest
from zope.component import adapter
from zope.interface import implementer

from arche_2fa.interfaces import ITwoFactAuthHandler


class Token2FA(object):
    token = None
    created = None
    expires = None

    def __init__(self, userid, token, minutes):
        self.userid = userid
        self.created = utcnow()
        self.token = token
        self.expires = self.created + timedelta(minutes = minutes)

    def __str__(self): return str(self.token)
    def __repr__(self): return repr(self.token)
    def __cmp__(self, txt): return cmp(self.token, txt)

    def validate(self, value):
        return self == value and not self.expired

    @property
    def expired(self):
        return utcnow() > self.expires

_default_charpool = string.letters + string.digits


@adapter(IRoot, IRequest)
@implementer(ITwoFactAuthHandler)
class TwoFactAuthHandler(IterableUserDict):
    name = ''
    title = ''

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.data = self.request.session.setdefault('2fa_tokens', {})

    def create_token(self, userid, length = 5, charpool =  _default_charpool, minutes = 10):
        token_str = ''.join([choice(charpool) for x in range(length)])
        token = Token2FA(userid, token_str, minutes)
        self[str(token)] = token
        return token

    def send(self, userid, view): #pragma: no coverage
        raise NotImplementedError()

    def validate(self, value):
        if value in self:
            token = self[value]
            return token.validate(value)
        return False

    def cleanup(self):
        for key in tuple(self.keys()):
            if self[key].expired:
                del self[key]

    @property
    def has_valid_tokens(self):
        self.cleanup()
        return len(self)

    def __nonzero__(self):
        return True

    def __repr__(self): #pragma: no coverage
        return '<%s.%s object>' % (self.__class__.__module__,
                                   self.__class__.__name__)


def get_registered_2fas(context, request):
    """ Shorthand to fetch all registered adapters.
        returns a generator with (<name>, <adapter>)
    """
    return request.registry.getAdapters((context, request), ITwoFactAuthHandler)

def clear_used_token(event):
    """ Make sure any 2FA session data is cleared when a user authenticates."""
    session = event.request.session
    if '2fa_tokens' in session:
        #In case adapters are instantiated during the same request
        session['2fa_tokens'].clear()
        del session['2fa_tokens']

def includeme(config):
    config.add_subscriber(clear_used_token, IWillLoginEvent)

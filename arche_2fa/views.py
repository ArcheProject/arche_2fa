from arche.interfaces import IRoot
from arche.security import NO_PERMISSION_REQUIRED
from arche.views.auth import LoginForm
from arche.views.base import BaseForm
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
import deform

from arche_2fa.models import get_registered_2fas
from arche_2fa import _


class Request2FAToken(BaseForm):
    type_name = "Auth"
    schema_name = "2fa"
    buttons = (deform.Button('send', title = _("Send login token")),)

    @reify
    def methods(self):
        return dict(get_registered_2fas(self.context, self.request))

    def send_success(self, appstruct):
        userfield = appstruct['email_or_userid']
        if '@' in userfield:
            user = self.context['users'].get_user_by_email(userfield)
        else:
            user = self.context['users'].get(userfield, None)
        if not user: #This should never happen since the data is already validated
            raise HTTPForbidden("Couldn't find a user")
        userid = user.userid
        type_2fa = appstruct['type_2fa']
        self.methods[type_2fa].send(userid)
        return HTTPFound(location = self.request.resource_url(self.context, '2fa_login', query = {'type_2fa': type_2fa, 'userid': userid}))


def includeme(config):
    """ This will move the default loginform at '/login' to '/2fa_login'.
        The '/login' screen will instead initiate the 2FA token request.
    """
    config.add_view(LoginForm,
                    context = IRoot,
                    name = '2fa_login',
                    permission = NO_PERMISSION_REQUIRED,
                    renderer = 'arche:templates/form.pt')
    config.add_view(Request2FAToken,
                    context = IRoot,
                    permission = NO_PERMISSION_REQUIRED,
                    name = 'login',
                    renderer = "arche:templates/form.pt")

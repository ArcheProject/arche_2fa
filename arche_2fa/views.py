from arche.interfaces import IRoot
from arche.security import NO_PERMISSION_REQUIRED
from arche.views.base import BaseForm
import deform


#class Request2FAToken(BaseForm):
#    type_name = "Auth"
#    schema_name = "2fa"
#
#    @property
#    def buttons(self):
#        #FIXME: Figure out buttons from added 2fa methods
#        return (deform.Button('request'),)


def includeme(config):
    pass
#    config.add_view(Request2FAToken,
#                    context = IRoot,
#                    permission = NO_PERMISSION_REQUIRED,
#                    name = '2fa_login',
#                    renderer = "arche:templates/form.pt")

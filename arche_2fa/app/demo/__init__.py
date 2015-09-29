from arche_2fa.models import TwoFactAuthHandler
from arche_2fa import _


class Demo2FA(TwoFactAuthHandler):
    name = 'demo'
    title = _("Demonstration")

    def send(self, userid, view):
        token = self.create_token(userid, length = 3)
        msg = _("demo_auth_code",
                default = "Demo authentication code: ${code}",
                mapping = {'code': str(token)})
        view.flash_messages.add(msg, type = "info", auto_destruct = False)


def includeme(config):
    config.registry.registerAdapter(Demo2FA, name = Demo2FA.name)

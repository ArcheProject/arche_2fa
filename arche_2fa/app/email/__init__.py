from pyramid.httpexceptions import HTTPForbidden

from arche_2fa.models import TwoFactAuthHandler
from arche_2fa import _


class Email2FA(TwoFactAuthHandler):
    name = 'email'
    title = _("Email")

    def send(self, userid):
        user = self.context['users'].get(userid, None)
        if user and user.email:
            token = self.create_token(userid, length = 6)
            subject = _("2fa_email_subject",
                        default = "${head_title}: Two factor authentication code",
                        mapping = {'head_title': self.context.head_title})
            html = "Code: %s" % str(token)
            self.request.send_email(subject, [user.email], html, send_immediately = True)
        else:
            raise HTTPForbidden(_("UserID or email address invalid."))


def includeme(config):
    config.registry.registerAdapter(Email2FA, name = Email2FA.name)

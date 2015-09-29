from pyramid.httpexceptions import HTTPForbidden
from pyramid.renderers import render

from arche_2fa.models import TwoFactAuthHandler
from arche_2fa import _


class Email2FA(TwoFactAuthHandler):
    name = 'email'
    title = _("Email")

    def send(self, userid, view):
        user = self.context['users'].get(userid, None)
        if user and user.email:
            token = self.create_token(userid, length = 6)
            subject = _("2fa_email_subject",
                        default = "${head_title}: Two factor authentication code",
                        mapping = {'head_title': self.context.head_title})
            response = {'code': str(token), 'user': user, 'view': view}
            html = render('arche_2fa.app.email:email.pt', response, request = self.request)
            self.request.send_email(subject, [user.email], html, send_immediately = True)
            msg = _("Email sent")
            view.flash_messages.add(msg, type = 'success')
        else:
            raise HTTPForbidden(_("UserID or email address invalid."))


def includeme(config):
    config.registry.registerAdapter(Email2FA, name = Email2FA.name)

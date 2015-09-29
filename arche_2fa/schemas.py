from __future__ import unicode_literals

from arche.interfaces import ISchemaCreatedEvent
from arche.schemas import LoginSchema
from arche.schemas import to_lowercase
from arche.validators import allow_login_userid_or_email
from pyramid.httpexceptions import HTTPForbidden
import colander
import deform

from arche_2fa.models import get_registered_2fas
from arche_2fa import _
from arche_2fa.interfaces import ITwoFactAuthHandler


@colander.deferred
def registered_2fa_names_validator(node, kw):
    context = kw['context']
    request = kw['request']
    return colander.OneOf(dict(get_registered_2fas(context, request)).keys())

@colander.deferred
def type_2fa_widget(node, kw):
    context = kw['context']
    request = kw['request']
    values = []
    values.extend([(name, obj.title) for (name, obj) in get_registered_2fas(context, request)])
    if len(values) != 1: #Insert at either 0 length or anything with more than one choice.
        values.insert(0, ('', _("<Select>")))
    return deform.widget.SelectWidget(values = values)

@colander.deferred
def max_token_validator(node, kw):
    context = kw['context']
    request = kw['request']
    return MaxTokenValidator(context, request)


class MaxTokenValidator(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, node, value):
        method_adapter = self.request.registry.queryMultiAdapter((self.context, self.request),
                                                            interface = ITwoFactAuthHandler,
                                                            name = value['type_2fa'])
        if not method_adapter:
            raise colander.Invalid(node, _("2FA-method not found."))
        maxtokens = self.request.registry.settings['arche_2fa.maxtokens']
        method_adapter.cleanup()
        if len(method_adapter) >= maxtokens:
            msg = _("too_many_attempts",
                    default = "Too many attempts in a row. Wait a while before retrying.")
            raise colander.Invalid(node, msg)


class Request2FASchema(colander.Schema):
    validator = max_token_validator
    email_or_userid = colander.SchemaNode(colander.String(),
                                          preparer = to_lowercase,
                                          validator = allow_login_userid_or_email,
                                          title = _(u"Email or UserID"),)
    type_2fa = colander.SchemaNode(colander.String(),
                                         title = _("Sign in method"),
                                         validator = registered_2fa_names_validator,
                                         widget = type_2fa_widget)


class Login2FAValidator(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, node, value):
        type_2fa = self.request.GET.get('type_2fa', None)
        methods = dict(get_registered_2fas(self.context, self.request))
        if type_2fa not in methods:
            raise colander.Invalid(node, _("The authentication method is invalid."))
        if not methods[type_2fa].validate(value):
            raise colander.Invalid(node, _("Invalid code"))


@colander.deferred
def login_2fa_validator(node, kw):
    context = kw['context']
    request = kw['request']
    return Login2FAValidator(context, request)


def insert_2fa_node(schema, event):
    """ Inject the 2fa node in the schema, or abort if something seems fishy.
    """
    methods = dict(get_registered_2fas(event.context, event.request))
    type_2fa = event.request.GET.get('type_2fa', None)
    if type_2fa not in methods:
        raise HTTPForbidden()
    schema.add(colander.SchemaNode(colander.String(),
                                   name = '2fa_code',
                                   title = _("Two factor authentication code"),
                                   validator = login_2fa_validator))
    if 'email_or_userid' in schema:
        schema['email_or_userid'].widget = deform.widget.HiddenWidget()
        schema['email_or_userid'].default = event.request.GET.get('userid', '')


def includeme(config):
    config.add_subscriber(insert_2fa_node, [LoginSchema, ISchemaCreatedEvent])
    config.add_content_schema('Auth', Request2FASchema, '2fa')

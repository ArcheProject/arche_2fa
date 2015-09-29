from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

from arche_2fa.interfaces import ITwoFactAuthHandler


class Email2FATests(TestCase):

    def setUp(self):
        self.config = testing.setUp()
 
    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from arche_2fa.app.email import Email2FA
        return Email2FA

    def _mk_instance(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        return self._cut(context, request)

    def test_verify_class(self):
        self.failUnless(verifyClass(ITwoFactAuthHandler, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(ITwoFactAuthHandler, self._mk_instance()))

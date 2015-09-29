from unittest import TestCase

from pyramid import testing
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject
from arche.events import WillLoginEvent
from arche.testing import barebone_fixture
from arche.api import User

from arche_2fa.interfaces import ITwoFactAuthHandler


class TwoFactAuthHandlerTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()
 
    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from arche_2fa.models import TwoFactAuthHandler
        return TwoFactAuthHandler

    def _mk_instance(self):
        context = testing.DummyResource()
        request = testing.DummyRequest()
        return self._cut(context, request)

    def test_verify_class(self):
        self.failUnless(verifyClass(ITwoFactAuthHandler, self._cut))

    def test_verify_obj(self):
        self.failUnless(verifyObject(ITwoFactAuthHandler, self._mk_instance()))

    def test_create_token(self):
        obj = self._mk_instance()
        obj.create_token('admin', length = 1, charpool = 'a')
        self.assertIn('a', obj)

    def test_validate(self):
        obj = self._mk_instance()
        self.failIf(obj.validate('a'))
        obj.create_token('admin', length = 1, charpool = 'a')
        self.failUnless(obj.validate('a'))
        obj.create_token('admin', length = 1, charpool = 'b', minutes = 0)
        self.failIf(obj.validate('b'))

    def test_cleanup(self):
        obj = self._mk_instance()
        obj.create_token('admin', length = 1, charpool = 'a', minutes = 0)
        obj.cleanup()
        self.assertEqual(len(obj), 0)

    def test_has_valid_tokens(self):
        obj = self._mk_instance()
        self.failIf(obj.has_valid_tokens)
        obj.create_token('admin', length = 1, charpool = 'a')
        self.failUnless(obj.has_valid_tokens)

    def test_object_is_always_true(self):
        obj = self._mk_instance()
        self.assertEqual(len(obj), 0)
        self.assertTrue(obj)


class TwoFactAuthHandlerIntegrationTests(TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('arche')
        self.config.include('arche_2fa')
 
    def tearDown(self):
        testing.tearDown()

    @property
    def _cut(self):
        from arche_2fa.models import TwoFactAuthHandler
        return TwoFactAuthHandler

    def _mk_instance(self):
        context = barebone_fixture(self.config)
        request = testing.DummyRequest()
        return self._cut(context, request)

    def test_demo_registration(self):
        self.config.include('arche_2fa.app.demo')
        from arche_2fa.models import get_registered_2fas
        from arche.api import Root
        context = Root()
        request = testing.DummyRequest()
        res = dict(get_registered_2fas(context, request))
        self.assertIn('demo', res)

    def test_tokens_cleared_on_login(self):
        obj = self._mk_instance()
        obj.context['users']['admin'] = user = User()
        obj.create_token('admin', length = 1, charpool = 'a')
        self.assertEqual(len(obj), 1)
        event = WillLoginEvent(user, request = obj.request)
        self.config.registry.notify(event)
        self.assertEqual(len(obj), 0)

from unittest import TestCase
from aweber_api import AWeberAPI, AWeberCollection, AWeberEntry
from mock_adapter import MockAdapter
import re

class TestAWeberEntry(TestCase):

    def setUp(self):
        self.aweber = AWeberAPI('1', '2')
        self.aweber.adapter = MockAdapter()
        self.list = self.aweber.load_from_url('/accounts/1/lists/303449')

    def test_should_be_an_entry(self):
        self.assertEqual(type(self.list), AWeberEntry)
        self.assertEqual(self.list.type, 'list')

    def test_should_have_id(self):
        self.assertEqual(self.list.id, 303449)

    def test_should_have_other_properties(self):
        self.assertEqual(self.list.name, 'default303449')

    def test_should_have_child_collections(self):
        campaigns = self.list.campaigns
        self.assertEqual(type(campaigns), AWeberCollection)

class TestAWeberAccountEntry(TestCase):

    def setUp(self):
        self.aweber = AWeberAPI('1', '2')
        self.aweber.adapter = MockAdapter()
        self.account = self.aweber.load_from_url('/accounts/1')

    def test_should_be_an_entry(self):
        self.assertEqual(type(self.account), AWeberEntry)
        self.assertEqual(self.account.type, 'account')

    def test_should_be_able_get_web_forms(self):
        forms = self.account.get_web_forms()

class TestAccountGetWebForms(TestAWeberAccountEntry):

    def setUp(self):
        TestAWeberAccountEntry.setUp(self)
        self.forms = self.account.get_web_forms()

    def test_should_be_a_list(self):
        self.assertEqual(type(self.forms), list)

    def test_should_have_23_web_forms(self):
        self.assertEqual(len(self.forms), 23)

    def test_each_should_be_entry(self):
        for entry in self.forms:
            self.assertEqual(type(entry), AWeberEntry)
            self.assertEqual(entry.type, 'web_form')

    def test_each_should_have_correct_url(self):
        url_regex = '/accounts\/1\/lists\/\d*/web_forms/\d*'
        for entry in self.forms:
            self.assertTrue(re.match(url_regex, entry.url))



from unittest import TestCase
from mock_adapter import MockAdapter
from dingus import Dingus
from aweber_api import (AWeberAPI, AWeberUser, ACCESS_TOKEN_URL, AUTHORIZE_URL,
                        REQUEST_TOKEN_URL, AWeberEntry)

key = 'XXXXX'
secret = '3434534534534'
class AWeberAPITest(TestCase):

    def setUp(self):
        self.aweber = AWeberAPI(key, secret)

    def test_should_exist(self):
        self.assertTrue(self.aweber)

class WhenGettingARequestToken(AWeberAPITest):

    def setUp(self):
        AWeberAPITest.setUp(self)
        self.response = "oauth_token=1234&oauth_token_secret=abcd"
        self.aweber.adapter = Dingus()
        self.aweber.adapter.user = AWeberUser()
        self.aweber.adapter.request = Dingus(return_value=self.response)

    def test_should_get_request_token(self):
        token, secret = self.aweber.get_request_token('http://localhost/demo')
        self.assertEqual(token, '1234')
        self.assertEqual(secret, 'abcd')

    def test_should_pass_args_to_request(self):
        self.called = False
        def _request(method, url, params):
            self.assertEqual(url, REQUEST_TOKEN_URL)
            self.assertEqual(method, 'POST')
            self.assertEqual(params['oauth_callback'], 'http://localhost/demo')
            self.called = True
            return self.response
        self.aweber.adapter.request = _request
        token, secret = self.aweber.get_request_token('http://localhost/demo')
        self.assertTrue(self.called, 'Called _request')

    def test_should_set_up_user(self):
        token, secret = self.aweber.get_request_token('http://localhost/demo')

        self.assertEqual(self.aweber.user.request_token, token)
        self.assertEqual(self.aweber.user.token_secret, secret)

    def test_should_have_authorize_url(self):
        token, secret = self.aweber.get_request_token('http://localhost/demo')
        self.assertEqual(self.aweber.authorize_url,
                         "{0}?oauth_token={1}".format(AUTHORIZE_URL, token))


class WhenGettingAnAccessToken(AWeberAPITest):

    def setUp(self):
        AWeberAPITest.setUp(self)
        self.response = "oauth_token=cheeseburger&oauth_token_secret=hotdog"
        self.aweber.adapter = Dingus()
        self.aweber.adapter.user = AWeberUser()
        self.aweber.adapter.request = Dingus(return_value=self.response)

        self.aweber.user.request_token = '1234'
        self.aweber.user.token_secret = 'abcd'
        self.aweber.user.verifier = '234a35a1'


    def test_should_get_access_token(self):
        access_token, token_secret = self.aweber.get_access_token()
        self.assertEqual(access_token, 'cheeseburger')
        self.assertEqual(token_secret, 'hotdog')

    def test_should_pass_args_to_request(self):
        self.called = False
        def _request(method, url, params={}):
            self.assertEqual(url, ACCESS_TOKEN_URL)
            self.assertEqual(method, 'POST')
            self.assertEqual(params['oauth_verifier'], '234a35a1')
            self.called = True
            return self.response
        self.aweber.adapter.request = _request
        token, secret = self.aweber.get_access_token()
        self.assertTrue(self.called, 'Called _request')

    def test_should_set_up_user(self):
        token, secret = self.aweber.get_access_token()
        self.assertEqual(self.aweber.user.access_token, token)
        self.assertEqual(self.aweber.user.token_secret, secret)

class WhenGettingAnAccount(TestCase):

    def setUp(self):
        self.aweber = AWeberAPI(key, secret)
        self.aweber.adapter = MockAdapter()

        self.access_token = '1234'
        self.token_secret = 'abcd'

    def test_when_getting_an_account(self):
        account = self.aweber.get_account(self.access_token, self.token_secret)
        self.assertEqual(type(account), AWeberEntry)
        self.assertEqual(account.id, 910)
        self.assertEqual(account.type, 'account')


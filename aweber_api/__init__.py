from urlparse import parse_qs

from aweber_api.base import (AWeberBase, API_BASE, ACCESS_TOKEN_URL,
                            REQUEST_TOKEN_URL, AUTHORIZE_URL)
from aweber_api.collection import AWeberCollection
from aweber_api.entry import AWeberEntry
from aweber_api.oauth import OAuthAdapter
from aweber_api.response import AWeberResponse

class AWeberAPI(AWeberBase):
    """ Base class for connecting to the AWeberAPI. Created with a consumer key
    and secret, then used to either generate tokens for authorizing a user, or
    can be provided tokens and used to access that user's resources. """

    def __init__(self, consumer_key, consumer_secret):
        self.adapter = OAuthAdapter(consumer_key, consumer_secret, API_BASE)
        self.adapter.user = AWeberUser()

    @property
    def authorize_url(self):
        """
        Returns the authorize url, potentially containing the request token
        parameter
        """
        if self.user.request_token:
            return "{0}?oauth_token={1}".format(AUTHORIZE_URL,
                                                self.user.request_token)
        return AUTHORIZE_URL

    def get_request_token(self, callback_url):
        """
        Gets a new request token / token secret for the given callback URL
        and the current consumer.  Returns token / secret, and sets properties
        on the AWeberUser object (self.user)
        """
        data = { 'oauth_callback' : callback_url }
        response = self.adapter.request('POST',
                                        REQUEST_TOKEN_URL,
                                        data)
        self.user.request_token, self.user.token_secret = self.\
                _parse_token_response(response)
        return (self.user.request_token, self.user.token_secret)

    def get_access_token(self):
        """
        Gets an access token for the given request token / token secret /
        verifier combination in the AWeberUser object at self.user
        Updates the user object and returns the tokens
        """

        data = { 'oauth_verifier' : self.user.verifier }
        response = self.adapter.request('POST',
                                        ACCESS_TOKEN_URL,
                                        data)
        self.user.access_token, self.user.token_secret = self.\
                                    _parse_token_response(response)
        return (self.user.access_token, self.user.token_secret)

    def _parse_token_response(self, response):
        if not type(response) == str:
            raise TypeError('Expected response to be a string')

        data = parse_qs(response)

        if not 'oauth_token' in data and not 'oauth_token_secret' in data:
            raise ValueError('OAuth parameters not returned')
        return (data['oauth_token'][0], data['oauth_token_secret'][0])

    def get_account(self, access_token=False, token_secret=False):
        """
        Returns the AWeberEntry object for the account specified by the
        access_token and token_secret currently in the self.user object.
        Optionally, access_token and token_secret can be provided to replace
        the properties in self.user.access_token and self.user.token_secret,
        respectively.
        """
        if access_token:
            self.user.access_token = access_token
        if token_secret:
            self.user.token_secret = token_secret
        url = '/accounts'
        response = self.adapter.request('GET', url)
        accounts = self._read_response(url, response)
        return accounts[0]

class AWeberUser(object):
    """
    Simple data storage object representing the user in the OAuth model.  Has
    properties for request_token, token_secret, access_token, and verifier.
    """

    request_token = None
    token_secret = None
    access_token = None
    verifier = None

    def get_highest_priority_token(self):
        return self.access_token or self.request_token


API_BASE = 'https://api.aweber.com/1.0'
ACCESS_TOKEN_URL = 'https://auth.aweber.com/1.0/oauth/access_token'
REQUEST_TOKEN_URL = 'https://auth.aweber.com/1.0/oauth/request_token'
AUTHORIZE_URL = 'https://auth.aweber.com/1.0/oauth/authorize'

class AWeberBase(object):
    """
    Provides functionality shared accross all AWeber objects
    """

    collections_map = {
        'account' : ['lists', 'vendor_accounts'],
        'broadcast_campaign' : ['links', 'messages'],
        'followup_campaign' :  ['links', 'messages'],
        'link' : ['clicks'],
        'list' : ['campaigns', 'subscribers', 'web_forms',
                  'web_form_split_tests'],
        'message' : ['opens', 'tracked_events'],
        'subscriber' : [],
        'web_form': [],
        'web_form_split_test' : ['components']
    }

    @property
    def user(self):
        return self.adapter.user

    def load_from_url(self, url):
        """
        Gets an AWeberCollection or AWeberEntry from the given URL.
        """
        response = self.adapter.request('GET', url)
        return self._read_response(url, response)

    def _method_for(self, type):
        if not self.type == type:
            raise AttributeError('Method does not exist')

    def _read_response(self, url, response):
        if 'entries' in response:
            from aweber_api.collection import AWeberCollection
            return AWeberCollection(url, response, self.adapter)
        if 'id' in response:
            from aweber_api.entry import AWeberEntry
            return AWeberEntry(url, response, self.adapter)
        raise TypeError('Unknown value returned')

    def _parseNamedOperation(self, data):
        from aweber_api.entry import AWeberEntry
        entries = []
        for item in data:
            entries.append(AWeberEntry(item['self_link'].replace(API_BASE, ''),
                                       item, self.adapter))
        return entries

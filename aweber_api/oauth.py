import oauth2 as oauth
import json

class OAuthAdapter(object):

    def __init__(self, key, secret, base):
        self.key = key
        self.secret = secret
        self.consumer = oauth.Consumer(key=self.key, secret=self.secret)
        self.api_base = base

    def _parse(self, response):
        try:
            data = json.loads(response)
            if not data or data == '':
                return response
            return data
        except:
            pass
        return response

    def request(self, method, url, data={}):
        token = self.user.get_highest_priority_token()
        if token:
            token = oauth.Token(token, self.user.token_secret)
            client = oauth.Client(self.consumer, token=token)
        else:
            client = oauth.Client(self.consumer)

        if not url[:4] == 'http':
            url = '%s%s' % (self.api_base, url)

        if len(data.keys()) == 0:
            body = None
        else:
            body = '&'.join(map(lambda x: "{0}={1}".format(x, data[x]),
                            data.keys()))

        try:
            resp, content = client.request(url, method, body=body)
            if type(content) == str:
                return self._parse(content)
        except e:
            pass
        return None

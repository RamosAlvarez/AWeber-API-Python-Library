from aweber_api.response import AWeberResponse

class AWeberEntry(AWeberResponse):
    """
    Represents a single entry in the AWeber API data heirarchy, such as one
    specific account, list, web form, etc.  Built on data that is returned
    from an id-ed URI, such as:
        /accounts/XXXX
        /accounts/XXXX/lists/XXXX
    Can also be generated from the data in the entries array of a collection
    object, which is identical to the data return from the URI for that
    specific entry.

    Provides direct access to properties in the response, such as self.id
    """

    def __init__(self, url, data, adapter):
        AWeberResponse.__init__(self, url, data, adapter)
        self._child_collections = {}


    def get_web_forms(self):
        self._method_for('account')
        data = self.adapter.request('GET',
                                    "{0}?ws.op=getWebForms".format(self.url))
        return self._parseNamedOperation(data)

    def _child_collection(self, attr):
        if not attr in self._child_collections:
            url = "{0}/{1}".format(self.url, attr)
            self._child_collections[attr] = self.load_from_url(url)
        return self._child_collections[attr]

    def __getattr__(self, attr):
        if attr in self._data:
            return self._data[attr]
        elif attr in self.collections_map[self.type]:
            return self._child_collection(attr)
        else:
            raise AttributeError(attr)



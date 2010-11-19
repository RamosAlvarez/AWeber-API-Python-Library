from aweber_api import AWeberBase

class AWeberResponse(AWeberBase):

    def __init__(self, url, data, adapter):
        self._type = None
        self.adapter = adapter
        self.url = url
        self._data = data
        self._entries = {}

    def _generate_type(self):
        if 'resource_type_link' in self._data:
            type = self._data['resource_type_link']
            self._type = type.split('#').pop()
        return None

    @property
    def type(self):
        if not self._type:
            self._generate_type()
        return self._type

    def __getattr__(self, attr):
        if attr in self._data:
            return self._data[attr]
        else:
            raise AttributeError(attr)


class Resource:
    def __init__(self, resource, resource_name):
        self._resource_name = resource_name
        self._resource = resource

    @property
    def resource(self):
        return self._resource

    @property
    def resource_name(self):
        return self._resource_name

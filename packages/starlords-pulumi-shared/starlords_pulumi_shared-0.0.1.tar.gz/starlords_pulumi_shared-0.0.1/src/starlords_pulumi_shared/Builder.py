from multipledispatch import dispatch

from starlords_pulumi_shared.resources.Resource import Resource


class Builder:

    def __init__(self, environment):
        self._dependencies = []
        self._environment = environment
        self._parent = None

    @dispatch(Resource)
    def parent(self, resource):
        self._parent = resource
        return self

    @dispatch(Resource)
    def depends_on(self, resource):
        self._dependencies.append(resource.resource)
        return self

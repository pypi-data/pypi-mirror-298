class AzureK8sConfig:
    def __init__(self):
        self._resource_name = None
        self._node_resource_group_name = None
        self._resource_group_name = None

    @property
    def resource_name(self):
        return self._resource_name

    @resource_name.setter
    def resource_name(self, value):
        self._resource_name = value

    @property
    def resource_group_name(self):
        return self._resource_group_name

    @resource_group_name.setter
    def resource_group_name(self, value):
        self._resource_group_name = value

    @property
    def node_resource_group_name(self):
        return self._node_resource_group_name

    @node_resource_group_name.setter
    def node_resource_group_name(self, value):
        self._node_resource_group_name = value

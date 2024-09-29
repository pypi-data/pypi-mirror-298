class AzureK8sConfig:
    def __init__(self):
        self._node_resource_group_name = None
        self._domains_resource_group_name = None

    @property
    def node_resource_group_name(self):
        return self._node_resource_group_name

    @node_resource_group_name.setter
    def node_resource_group_name(self, value):
        self._node_resource_group_name = value

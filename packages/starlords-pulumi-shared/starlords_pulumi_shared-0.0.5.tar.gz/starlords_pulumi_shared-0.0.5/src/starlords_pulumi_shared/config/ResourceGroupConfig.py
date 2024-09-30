class ResourceGroupConfig:
    def __init__(self, resource_group_name=None):
        self._resource_group_name = resource_group_name

    @property
    def name(self):
        return self._resource_group_name

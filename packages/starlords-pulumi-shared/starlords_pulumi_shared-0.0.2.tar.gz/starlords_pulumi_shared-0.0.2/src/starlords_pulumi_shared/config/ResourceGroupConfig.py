class ResourceGroupConfig:
    def __init__(self, resource_group_name=None):
        self._rg_name = resource_group_name

    @property
    def name(self):
        return self._rg_name

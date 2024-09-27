import pulumi_azure_native

from starlords_pulumi_shared.resources.Resource import Resource


class ResourceGroup(Resource):
    resource: pulumi_azure_native.resources.ResourceGroup

    def __init__(self, id_, resource, name):
        super().__init__(resource, name)
        self.resource_group_id = id_

    @property
    def resource_group_name(self):
        return super().resource_name

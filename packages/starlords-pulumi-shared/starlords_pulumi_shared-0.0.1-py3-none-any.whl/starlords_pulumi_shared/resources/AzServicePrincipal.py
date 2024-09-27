import pulumi_azuread
from multipledispatch import dispatch
from pulumi_azuread import ServicePrincipal, Application

from starlords_pulumi_shared.resources.Resource import Resource


class AzServicePrincipal(Resource):
    service_principal: pulumi_azuread.ServicePrincipal

    @dispatch(pulumi_azuread.ServicePrincipal, str)
    def __init__(self, service_principal, service_principal_name):
        super().__init__(service_principal, service_principal_name)

    @dispatch(pulumi_azuread.ServicePrincipal, str, pulumi_azuread.Application, pulumi_azuread.ServicePrincipalPassword)
    def __init__(self, service_principal, sp_name, ad_application, service_principal_password):
        service_principal: pulumi_azuread.ServicePrincipal
        super().__init__(service_principal, sp_name)
        self._ad_application = ad_application
        self._service_principal_password = service_principal_password

    @property
    def service_principal(self) -> ServicePrincipal:
        return super().resource

    @property
    def application(self) -> Application:
        return self._ad_application

    @property
    def service_principal_name(self):
        return super().resource_name

    @property
    def service_principal_password(self):
        return self._service_principal_password

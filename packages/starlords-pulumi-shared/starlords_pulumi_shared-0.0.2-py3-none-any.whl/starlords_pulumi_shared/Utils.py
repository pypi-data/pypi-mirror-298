import hashlib
import os
import traceback
from functools import wraps

import pulumi
import pulumi_azuread
from pulumi import InvokeOptions
from pulumi_azure_native.authorization import get_client_config
from pulumi_azure_native.resources import get_resource, get_resource_group

from starlords_pulumi_shared import AzureServicePrincipal
from starlords_pulumi_shared import ClientConfig


def env(config):
    return config.require('environment')


def is_dev(environment):
    return environment == 'dev'


def is_prod(environment):
    return environment == 'prod'


def tags(config):
    return {config.require('environment'),
            config.require('azure-native:location'),
            config.require('resource_group_name')}


def get_azure_resource(resource_group_name=None, resource_name=None, resource_type=None):
    from starlords_pulumi_shared.resources.Resource import Resource
    return Resource(get_resource(resource_group_name=resource_group_name, resource_name=resource_name,
                                 resource_type=resource_type), resource_group_name)


def get_azure_resource_group(name, parent=None):
    from starlords_pulumi_shared.resources.ResourceGroup import ResourceGroup
    result = get_resource_group(resource_group_name=name, opts=InvokeOptions(parent=parent))
    return ResourceGroup(id_=result.id, resource=result, name=result.name)


def get_service_principal(sp_name, sp_object_id):
    pulumi_sp = pulumi_azuread.ServicePrincipal.get(sp_name, sp_object_id)
    return AzureServicePrincipal(pulumi_sp, sp_name)


def create_azure_resource_id(subscription_id: str,
                             resource_group_name: str,
                             resource_provider_namespace: str,
                             resource_type: str,
                             resource_name: str) -> str:
    return f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/{resource_provider_namespace}/{resource_type}/{resource_name}"


def get_pulumi_client_config():
    client_config = get_client_config()
    return ClientConfig(client_config.tenant_id, client_config.subscription_id)


def unique_id(input_str, length=6) -> str:
    base64_str = hashlib.sha256(input_str.encode()).hexdigest()[:length]
    return base64_str


def read_public_key(k8s_ssh_public_key):
    with (open(k8s_ssh_public_key)) as f:
        return f.read()


def export_kube_config(kubeconfig):
    user_dir = os.path.expanduser('~')
    file = f'{user_dir}/.kube/config'

    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as f:
        f.write(kubeconfig)


def log_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            stack_trace = traceback.format_exc()
            pulumi.log.error(f"An error occurred in {func.__name__}: {e}\n{stack_trace}")
            raise

    return wrapper

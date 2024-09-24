# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._operations import Operations
from ._web_pub_sub_operations import WebPubSubOperations
from ._usages_operations import UsagesOperations
from ._web_pub_sub_custom_certificates_operations import WebPubSubCustomCertificatesOperations
from ._web_pub_sub_custom_domains_operations import WebPubSubCustomDomainsOperations
from ._web_pub_sub_hubs_operations import WebPubSubHubsOperations
from ._web_pub_sub_private_endpoint_connections_operations import WebPubSubPrivateEndpointConnectionsOperations
from ._web_pub_sub_private_link_resources_operations import WebPubSubPrivateLinkResourcesOperations
from ._web_pub_sub_replicas_operations import WebPubSubReplicasOperations
from ._web_pub_sub_replica_shared_private_link_resources_operations import (
    WebPubSubReplicaSharedPrivateLinkResourcesOperations,
)
from ._web_pub_sub_shared_private_link_resources_operations import WebPubSubSharedPrivateLinkResourcesOperations

from ._patch import __all__ as _patch_all
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "Operations",
    "WebPubSubOperations",
    "UsagesOperations",
    "WebPubSubCustomCertificatesOperations",
    "WebPubSubCustomDomainsOperations",
    "WebPubSubHubsOperations",
    "WebPubSubPrivateEndpointConnectionsOperations",
    "WebPubSubPrivateLinkResourcesOperations",
    "WebPubSubReplicasOperations",
    "WebPubSubReplicaSharedPrivateLinkResourcesOperations",
    "WebPubSubSharedPrivateLinkResourcesOperations",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()

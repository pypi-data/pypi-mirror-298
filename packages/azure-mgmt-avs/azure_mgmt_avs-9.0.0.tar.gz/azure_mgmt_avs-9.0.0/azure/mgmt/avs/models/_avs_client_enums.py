# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class ActionType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum. Indicates the action type. "Internal" refers to actions that are for internal only APIs."""

    INTERNAL = "Internal"


class AddonProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Addon provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    CANCELLED = "Cancelled"
    """is cancelled"""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class AddonType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Addon type."""

    SRM = "SRM"
    VR = "VR"
    HCX = "HCX"
    ARC = "Arc"


class AffinityStrength(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Affinity Strength."""

    SHOULD = "Should"
    """is should"""
    MUST = "Must"
    """is must"""


class AffinityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Affinity type."""

    AFFINITY = "Affinity"
    """is affinity"""
    ANTI_AFFINITY = "AntiAffinity"
    """is anti-affinity"""


class AvailabilityStrategy(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Whether the private clouds is available in a single zone or two zones."""

    SINGLE_ZONE = "SingleZone"
    """in single zone"""
    DUAL_ZONE = "DualZone"
    """in two zones"""


class AzureHybridBenefitType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Azure Hybrid Benefit type."""

    SQL_HOST = "SqlHost"
    """is SqlHost"""
    NONE = "None"
    """is None"""


class CloudLinkProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """cloud link provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""


class CloudLinkStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Cloud Link status."""

    ACTIVE = "Active"
    """is active"""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    FAILED = "Failed"
    """is failed"""
    DISCONNECTED = "Disconnected"
    """is disconnected"""


class ClusterProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Cluster provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    CANCELLED = "Cancelled"
    """is cancelled"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class CreatedByType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of identity that created the resource."""

    USER = "User"
    APPLICATION = "Application"
    MANAGED_IDENTITY = "ManagedIdentity"
    KEY = "Key"


class DatastoreProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """datastore provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    CANCELLED = "Cancelled"
    """is cancelled"""
    PENDING = "Pending"
    """is pending"""
    CREATING = "Creating"
    """is creating"""
    UPDATING = "Updating"
    """is updating"""
    DELETING = "Deleting"
    """is deleting"""


class DatastoreStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """datastore status."""

    UNKNOWN = "Unknown"
    """is unknown"""
    ACCESSIBLE = "Accessible"
    """is accessible"""
    INACCESSIBLE = "Inaccessible"
    """is inaccessible"""
    ATTACHED = "Attached"
    """is attached"""
    DETACHED = "Detached"
    """is detached"""
    LOST_COMMUNICATION = "LostCommunication"
    """is lost communication"""
    DEAD_OR_ERROR = "DeadOrError"
    """is dead or error"""


class DhcpTypeEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of DHCP: SERVER or RELAY."""

    SERVER = "SERVER"
    RELAY = "RELAY"


class DnsServiceLogLevelEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """DNS service log level."""

    DEBUG = "DEBUG"
    """is debug"""
    INFO = "INFO"
    """is info"""
    WARNING = "WARNING"
    """is warning"""
    ERROR = "ERROR"
    """is error"""
    FATAL = "FATAL"
    """is fatal"""


class DnsServiceStatusEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """DNS service status."""

    SUCCESS = "SUCCESS"
    """is success"""
    FAILURE = "FAILURE"
    """is failure"""


class DnsZoneType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of DNS zone."""

    PUBLIC = "Public"
    """Primary DNS zone."""
    PRIVATE = "Private"
    """Private DNS zone."""


class EncryptionKeyStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Whether the the encryption key is connected or access denied."""

    CONNECTED = "Connected"
    """is connected"""
    ACCESS_DENIED = "AccessDenied"
    """is access denied"""


class EncryptionState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Whether encryption is enabled or disabled."""

    ENABLED = "Enabled"
    """is enabled"""
    DISABLED = "Disabled"
    """is disabled"""


class EncryptionVersionType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Whether the encryption version is fixed or auto-detected."""

    FIXED = "Fixed"
    """is fixed"""
    AUTO_DETECTED = "AutoDetected"
    """is auto-detected"""


class ExpressRouteAuthorizationProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Express Route Circuit Authorization provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    UPDATING = "Updating"
    """is updating"""


class GlobalReachConnectionProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Global Reach Connection provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    UPDATING = "Updating"
    """is updating"""


class GlobalReachConnectionStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Global Reach Connection status."""

    CONNECTED = "Connected"
    """is connected"""
    CONNECTING = "Connecting"
    """is connecting"""
    DISCONNECTED = "Disconnected"
    """is disconnected"""


class HcxEnterpriseSiteProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """HCX Enterprise Site provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""


class HcxEnterpriseSiteStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """HCX Enterprise Site status."""

    AVAILABLE = "Available"
    """is available"""
    CONSUMED = "Consumed"
    """is consumed"""
    DEACTIVATED = "Deactivated"
    """is deactivated"""
    DELETED = "Deleted"
    """is deleted"""


class InternetEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Whether internet is enabled or disabled."""

    ENABLED = "Enabled"
    """is enabled"""
    DISABLED = "Disabled"
    """is disabled"""


class IscsiPathProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """private cloud provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    PENDING = "Pending"
    """is pending"""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class MountOptionEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Mode that describes whether the LUN has to be mounted as a datastore or
    attached as a LUN.
    """

    MOUNT = "MOUNT"
    """is mount"""
    ATTACH = "ATTACH"
    """is attach"""


class NsxPublicIpQuotaRaisedEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """NSX public IP quota raised."""

    ENABLED = "Enabled"
    """is enabled"""
    DISABLED = "Disabled"
    """is disabled"""


class OptionalParamEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Optional Param."""

    OPTIONAL = "Optional"
    """is optional"""
    REQUIRED = "Required"
    """is required"""


class Origin(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The intended executor of the operation; as in Resource Based Access Control (RBAC) and audit
    logs UX. Default value is "user,system".
    """

    USER = "user"
    SYSTEM = "system"
    USER_SYSTEM = "user,system"


class PlacementPolicyProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Placement Policy provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class PlacementPolicyState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Placement Policy state."""

    ENABLED = "Enabled"
    """is enabled"""
    DISABLED = "Disabled"
    """is disabled"""


class PlacementPolicyType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Placement Policy type."""

    VM_VM = "VmVm"
    VM_HOST = "VmHost"


class PortMirroringDirectionEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Port Mirroring Direction."""

    INGRESS = "INGRESS"
    """is ingress"""
    EGRESS = "EGRESS"
    """is egress"""
    BIDIRECTIONAL = "BIDIRECTIONAL"
    """is bidirectional"""


class PortMirroringStatusEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Port Mirroring status."""

    SUCCESS = "SUCCESS"
    """is success"""
    FAILURE = "FAILURE"
    """is failure"""


class PrivateCloudProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """private cloud provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    CANCELLED = "Cancelled"
    """is cancelled"""
    PENDING = "Pending"
    """is pending"""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class QuotaEnabled(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """quota enabled."""

    ENABLED = "Enabled"
    """is enabled"""
    DISABLED = "Disabled"
    """is disabled"""


class ResourceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of managed service identity (either system assigned, or none)."""

    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"


class ScriptCmdletAudience(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Specifies whether a script cmdlet is intended to be invoked only through automation or visible
    to customers.
    """

    AUTOMATION = "Automation"
    """is automation"""
    ANY = "Any"
    """is any"""


class ScriptCmdletProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """A script cmdlet provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""


class ScriptExecutionParameterType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """script execution parameter type."""

    VALUE = "Value"
    SECURE_VALUE = "SecureValue"
    CREDENTIAL = "Credential"


class ScriptExecutionProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Script Execution provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    PENDING = "Pending"
    """is pending"""
    RUNNING = "Running"
    """is running"""
    CANCELLING = "Cancelling"
    """is cancelling"""
    CANCELLED = "Cancelled"
    """is cancelled"""
    DELETING = "Deleting"
    """is deleting"""


class ScriptOutputStreamType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Script Output Stream type."""

    INFORMATION = "Information"
    """is information"""
    WARNING = "Warning"
    """is warning"""
    OUTPUT = "Output"
    """is output"""
    ERROR = "Error"
    """is error"""


class ScriptPackageProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Script Package provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""


class ScriptParameterTypes(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Script Parameter types."""

    STRING = "String"
    """is string"""
    SECURE_STRING = "SecureString"
    """is secure string"""
    CREDENTIAL = "Credential"
    """is credential"""
    INT = "Int"
    """is int"""
    BOOL = "Bool"
    """is bool"""
    FLOAT = "Float"
    """is float"""
    INT_ENUM = "Int"
    """is int"""


class SegmentStatusEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Segment status."""

    SUCCESS = "SUCCESS"
    """is success"""
    FAILURE = "FAILURE"
    """is failure"""


class SkuTier(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """This field is required to be implemented by the Resource Provider if the service has more than
    one tier, but is not required on a PUT.
    """

    FREE = "Free"
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"


class SslEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Whether SSL is enabled or disabled."""

    ENABLED = "Enabled"
    """is enabled"""
    DISABLED = "Disabled"
    """is disabled"""


class TrialStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """trial status."""

    TRIAL_AVAILABLE = "TrialAvailable"
    """is available"""
    TRIAL_USED = "TrialUsed"
    """is used"""
    TRIAL_DISABLED = "TrialDisabled"
    """is disabled"""


class VirtualMachineProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Virtual Machine provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""


class VirtualMachineRestrictMovementState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Virtual Machine Restrict Movement state."""

    ENABLED = "Enabled"
    """is enabled"""
    DISABLED = "Disabled"
    """is disabled"""


class VisibilityParameterEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Visibility Parameter."""

    VISIBLE = "Visible"
    """is visible"""
    HIDDEN = "Hidden"
    """is hidden"""


class VMGroupStatusEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """VM group status."""

    SUCCESS = "SUCCESS"
    """is success"""
    FAILURE = "FAILURE"
    """is failure"""


class VMTypeEnum(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """VM type."""

    REGULAR = "REGULAR"
    """is regular"""
    EDGE = "EDGE"
    """is edge"""
    SERVICE = "SERVICE"
    """is service"""


class WorkloadNetworkDhcpProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Workload Network DHCP provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class WorkloadNetworkDnsServiceProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Workload Network DNS Service provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class WorkloadNetworkDnsZoneProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Workload Network DNS Zone provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class WorkloadNetworkPortMirroringProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Workload Network Port Mirroring provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class WorkloadNetworkProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """base Workload Network provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class WorkloadNetworkPublicIPProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Workload Network Public IP provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class WorkloadNetworkSegmentProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Workload Network Segment provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""


class WorkloadNetworkVMGroupProvisioningState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Workload Network VM Group provisioning state."""

    SUCCEEDED = "Succeeded"
    """Resource has been created."""
    FAILED = "Failed"
    """Resource creation failed."""
    CANCELED = "Canceled"
    """Resource creation was canceled."""
    BUILDING = "Building"
    """is building"""
    DELETING = "Deleting"
    """is deleting"""
    UPDATING = "Updating"
    """is updating"""

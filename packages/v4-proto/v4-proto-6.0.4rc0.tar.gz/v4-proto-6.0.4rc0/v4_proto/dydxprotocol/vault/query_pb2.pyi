from v4_proto.gogoproto import gogo_pb2 as _gogo_pb2
from v4_proto.google.api import annotations_pb2 as _annotations_pb2
from v4_proto.cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from v4_proto.dydxprotocol.subaccounts import subaccount_pb2 as _subaccount_pb2
from v4_proto.dydxprotocol.vault import params_pb2 as _params_pb2
from v4_proto.dydxprotocol.vault import share_pb2 as _share_pb2
from v4_proto.dydxprotocol.vault import vault_pb2 as _vault_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryParamsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryParamsResponse(_message.Message):
    __slots__ = ("params", "default_quoting_params", "operator_params")
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_QUOTING_PARAMS_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    default_quoting_params: _params_pb2.QuotingParams
    operator_params: _params_pb2.OperatorParams
    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]] = ..., default_quoting_params: _Optional[_Union[_params_pb2.QuotingParams, _Mapping]] = ..., operator_params: _Optional[_Union[_params_pb2.OperatorParams, _Mapping]] = ...) -> None: ...

class QueryVaultRequest(_message.Message):
    __slots__ = ("type", "number")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    type: _vault_pb2.VaultType
    number: int
    def __init__(self, type: _Optional[_Union[_vault_pb2.VaultType, str]] = ..., number: _Optional[int] = ...) -> None: ...

class QueryVaultResponse(_message.Message):
    __slots__ = ("vault_id", "subaccount_id", "equity", "inventory", "vault_params")
    VAULT_ID_FIELD_NUMBER: _ClassVar[int]
    SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EQUITY_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    VAULT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    vault_id: _vault_pb2.VaultId
    subaccount_id: _subaccount_pb2.SubaccountId
    equity: bytes
    inventory: bytes
    vault_params: _params_pb2.VaultParams
    def __init__(self, vault_id: _Optional[_Union[_vault_pb2.VaultId, _Mapping]] = ..., subaccount_id: _Optional[_Union[_subaccount_pb2.SubaccountId, _Mapping]] = ..., equity: _Optional[bytes] = ..., inventory: _Optional[bytes] = ..., vault_params: _Optional[_Union[_params_pb2.VaultParams, _Mapping]] = ...) -> None: ...

class QueryAllVaultsRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryAllVaultsResponse(_message.Message):
    __slots__ = ("vaults", "pagination")
    VAULTS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    vaults: _containers.RepeatedCompositeFieldContainer[QueryVaultResponse]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, vaults: _Optional[_Iterable[_Union[QueryVaultResponse, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryMegavaultTotalSharesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryMegavaultTotalSharesResponse(_message.Message):
    __slots__ = ("total_shares",)
    TOTAL_SHARES_FIELD_NUMBER: _ClassVar[int]
    total_shares: _share_pb2.NumShares
    def __init__(self, total_shares: _Optional[_Union[_share_pb2.NumShares, _Mapping]] = ...) -> None: ...

class QueryMegavaultOwnerSharesRequest(_message.Message):
    __slots__ = ("pagination",)
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest
    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]] = ...) -> None: ...

class QueryMegavaultOwnerSharesResponse(_message.Message):
    __slots__ = ("owner_shares", "pagination")
    OWNER_SHARES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    owner_shares: _containers.RepeatedCompositeFieldContainer[_share_pb2.OwnerShare]
    pagination: _pagination_pb2.PageResponse
    def __init__(self, owner_shares: _Optional[_Iterable[_Union[_share_pb2.OwnerShare, _Mapping]]] = ..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]] = ...) -> None: ...

class QueryVaultParamsRequest(_message.Message):
    __slots__ = ("type", "number")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    type: _vault_pb2.VaultType
    number: int
    def __init__(self, type: _Optional[_Union[_vault_pb2.VaultType, str]] = ..., number: _Optional[int] = ...) -> None: ...

class QueryVaultParamsResponse(_message.Message):
    __slots__ = ("vault_id", "vault_params")
    VAULT_ID_FIELD_NUMBER: _ClassVar[int]
    VAULT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    vault_id: _vault_pb2.VaultId
    vault_params: _params_pb2.VaultParams
    def __init__(self, vault_id: _Optional[_Union[_vault_pb2.VaultId, _Mapping]] = ..., vault_params: _Optional[_Union[_params_pb2.VaultParams, _Mapping]] = ...) -> None: ...

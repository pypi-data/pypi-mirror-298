# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/role/v1/role/role_service.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.role.v1.role import check_permissions_pb2 as com_dot_terraquantum_dot_role_dot_v1_dot_role_dot_check__permissions__pb2
from com.terraquantum.role.v1.role import get_organization_member_role_request_pb2 as com_dot_terraquantum_dot_role_dot_v1_dot_role_dot_get__organization__member__role__request__pb2
from com.terraquantum.role.v1.role import organization_member_role_pb2 as com_dot_terraquantum_dot_role_dot_v1_dot_role_dot_organization__member__role__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0com/terraquantum/role/v1/role/role_service.proto\x12\x1d\x63om.terraquantum.role.v1.role\x1a\x35\x63om/terraquantum/role/v1/role/check_permissions.proto\x1aHcom/terraquantum/role/v1/role/get_organization_member_role_request.proto\x1a<com/terraquantum/role/v1/role/organization_member_role.proto2\xad\x02\n\x0bRoleService\x12\x82\x01\n\x10\x43heckPermissions\x12\x36.com.terraquantum.role.v1.role.CheckPermissionsRequest\x1a\x36.com.terraquantum.role.v1.role.CheckPermissionResponse\x12\x98\x01\n\x19GetOrganizationMemberRole\x12?.com.terraquantum.role.v1.role.GetOrganizationMemberRoleRequest\x1a:.com.terraquantum.role.v1.role.OrganizationMemberRoleProtoB\x92\x02\n!com.com.terraquantum.role.v1.roleB\x10RoleServiceProtoP\x01ZAterraquantum.swiss/tq42_grpc_client/com/terraquantum/role/v1/role\xa2\x02\x05\x43TRVR\xaa\x02\x1d\x43om.Terraquantum.Role.V1.Role\xca\x02\x1d\x43om\\Terraquantum\\Role\\V1\\Role\xe2\x02)Com\\Terraquantum\\Role\\V1\\Role\\GPBMetadata\xea\x02!Com::Terraquantum::Role::V1::Roleb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.role.v1.role.role_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n!com.com.terraquantum.role.v1.roleB\020RoleServiceProtoP\001ZAterraquantum.swiss/tq42_grpc_client/com/terraquantum/role/v1/role\242\002\005CTRVR\252\002\035Com.Terraquantum.Role.V1.Role\312\002\035Com\\Terraquantum\\Role\\V1\\Role\342\002)Com\\Terraquantum\\Role\\V1\\Role\\GPBMetadata\352\002!Com::Terraquantum::Role::V1::Role'
  _globals['_ROLESERVICE']._serialized_start=275
  _globals['_ROLESERVICE']._serialized_end=576
# @@protoc_insertion_point(module_scope)

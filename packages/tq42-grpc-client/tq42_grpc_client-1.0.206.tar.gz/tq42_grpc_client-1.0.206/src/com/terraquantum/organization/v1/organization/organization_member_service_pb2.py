# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/organization/v1/organization/organization_member_service.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.organization.v1.organization import organization_member_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_organization__member__pb2
from com.terraquantum.organization.v1.organization import create_organization_member_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_create__organization__member__request__pb2
from com.terraquantum.organization.v1.organization import reactivate_organization_member_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_reactivate__organization__member__request__pb2
from com.terraquantum.organization.v1.organization import inactivate_organization_member_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_inactivate__organization__member__request__pb2
from com.terraquantum.organization.v1.organization import update_organization_member_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_update__organization__member__request__pb2
from com.terraquantum.organization.v1.organization import get_organization_member_by_id_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_get__organization__member__by__id__request__pb2
from com.terraquantum.organization.v1.organization import list_organization_members_by_organization_id_request_pb2 as com_dot_terraquantum_dot_organization_dot_v1_dot_organization_dot_list__organization__members__by__organization__id__request__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nOcom/terraquantum/organization/v1/organization/organization_member_service.proto\x12-com.terraquantum.organization.v1.organization\x1aGcom/terraquantum/organization/v1/organization/organization_member.proto\x1aVcom/terraquantum/organization/v1/organization/create_organization_member_request.proto\x1aZcom/terraquantum/organization/v1/organization/reactivate_organization_member_request.proto\x1aZcom/terraquantum/organization/v1/organization/inactivate_organization_member_request.proto\x1aVcom/terraquantum/organization/v1/organization/update_organization_member_request.proto\x1aYcom/terraquantum/organization/v1/organization/get_organization_member_by_id_request.proto\x1ahcom/terraquantum/organization/v1/organization/list_organization_members_by_organization_id_request.proto2\x91\t\n\x19OrganizationMemberService\x12\xb2\x01\n\x18\x43reateOrganizationMember\x12N.com.terraquantum.organization.v1.organization.CreateOrganizationMemberRequest\x1a\x46.com.terraquantum.organization.v1.organization.OrganizationMemberProto\x12\xba\x01\n\x1cReactivateOrganizationMember\x12R.com.terraquantum.organization.v1.organization.ReactivateOrganizationMemberRequest\x1a\x46.com.terraquantum.organization.v1.organization.OrganizationMemberProto\x12\xba\x01\n\x1cInactivateOrganizationMember\x12R.com.terraquantum.organization.v1.organization.InactivateOrganizationMemberRequest\x1a\x46.com.terraquantum.organization.v1.organization.OrganizationMemberProto\x12\xb2\x01\n\x18UpdateOrganizationMember\x12N.com.terraquantum.organization.v1.organization.UpdateOrganizationMemberRequest\x1a\x46.com.terraquantum.organization.v1.organization.OrganizationMemberProto\x12\xb4\x01\n\x19GetOrganizationMemberById\x12O.com.terraquantum.organization.v1.organization.GetOrganizationMemberByIdRequest\x1a\x46.com.terraquantum.organization.v1.organization.OrganizationMemberProto\x12\xd8\x01\n\'ListOrganizationMembersByOrganizationId\x12].com.terraquantum.organization.v1.organization.ListOrganizationMembersByOrganizationIdRequest\x1aN.com.terraquantum.organization.v1.organization.ListOrganizationMembersResponseB\x80\x03\n1com.com.terraquantum.organization.v1.organizationB\x1eOrganizationMemberServiceProtoP\x01ZQterraquantum.swiss/tq42_grpc_client/com/terraquantum/organization/v1/organization\xa2\x02\x05\x43TOVO\xaa\x02-Com.Terraquantum.Organization.V1.Organization\xca\x02-Com\\Terraquantum\\Organization\\V1\\Organization\xe2\x02\x39\x43om\\Terraquantum\\Organization\\V1\\Organization\\GPBMetadata\xea\x02\x31\x43om::Terraquantum::Organization::V1::Organizationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.organization.v1.organization.organization_member_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n1com.com.terraquantum.organization.v1.organizationB\036OrganizationMemberServiceProtoP\001ZQterraquantum.swiss/tq42_grpc_client/com/terraquantum/organization/v1/organization\242\002\005CTOVO\252\002-Com.Terraquantum.Organization.V1.Organization\312\002-Com\\Terraquantum\\Organization\\V1\\Organization\342\0029Com\\Terraquantum\\Organization\\V1\\Organization\\GPBMetadata\352\0021Com::Terraquantum::Organization::V1::Organization'
  _globals['_ORGANIZATIONMEMBERSERVICE']._serialized_start=761
  _globals['_ORGANIZATIONMEMBERSERVICE']._serialized_end=1930
# @@protoc_insertion_point(module_scope)

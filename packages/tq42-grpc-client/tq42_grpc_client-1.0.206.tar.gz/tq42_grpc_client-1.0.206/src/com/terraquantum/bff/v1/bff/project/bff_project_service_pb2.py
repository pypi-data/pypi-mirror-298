# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/bff/v1/bff/project/bff_project_service.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.bff.v1.bff.project import project_data_pb2 as com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_project_dot_project__data__pb2
from com.terraquantum.bff.v1.bff.project import get_project_data_request_pb2 as com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_project_dot_get__project__data__request__pb2
from com.terraquantum.bff.v1.bff.project import list_projects_data_response_pb2 as com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_project_dot_list__projects__data__response__pb2
from com.terraquantum.bff.v1.bff.project import list_projects_data_by_organization_id_request_pb2 as com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_project_dot_list__projects__data__by__organization__id__request__pb2
from com.terraquantum.bff.v1.bff.project import list_projects_pb2 as com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_project_dot_list__projects__pb2
from com.terraquantum.project.v1.project import list_projects_response_pb2 as com_dot_terraquantum_dot_project_dot_v1_dot_project_dot_list__projects__response__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=com/terraquantum/bff/v1/bff/project/bff_project_service.proto\x12#com.terraquantum.bff.v1.bff.project\x1a\x36\x63om/terraquantum/bff/v1/bff/project/project_data.proto\x1a\x42\x63om/terraquantum/bff/v1/bff/project/get_project_data_request.proto\x1a\x45\x63om/terraquantum/bff/v1/bff/project/list_projects_data_response.proto\x1aWcom/terraquantum/bff/v1/bff/project/list_projects_data_by_organization_id_request.proto\x1a\x37\x63om/terraquantum/bff/v1/bff/project/list_projects.proto\x1a@com/terraquantum/project/v1/project/list_projects_response.proto2\xf5\x04\n\x11\x42\x66\x66ProjectService\x12\x91\x01\n\x13ListProjectsForUser\x12?.com.terraquantum.bff.v1.bff.project.ListProjectsForUserRequest\x1a\x39.com.terraquantum.project.v1.project.ListProjectsResponse\x12\x93\x01\n\x14ListProjectsForGroup\x12@.com.terraquantum.bff.v1.bff.project.ListProjectsForGroupRequest\x1a\x39.com.terraquantum.project.v1.project.ListProjectsResponse\x12\x83\x01\n\x0eGetProjectData\x12:.com.terraquantum.bff.v1.bff.project.GetProjectDataRequest\x1a\x35.com.terraquantum.bff.v1.bff.project.ProjectDataProto\x12\xaf\x01\n ListProjectsDataByOrganizationId\x12L.com.terraquantum.bff.v1.bff.project.ListProjectsDataByOrganizationIdRequest\x1a=.com.terraquantum.bff.v1.bff.project.ListProjectsDataResponseB\xbe\x02\n\'com.com.terraquantum.bff.v1.bff.projectB\x16\x42\x66\x66ProjectServiceProtoP\x01ZGterraquantum.swiss/tq42_grpc_client/com/terraquantum/bff/v1/bff/project\xa2\x02\x06\x43TBVBP\xaa\x02#Com.Terraquantum.Bff.V1.Bff.Project\xca\x02#Com\\Terraquantum\\Bff\\V1\\Bff\\Project\xe2\x02/Com\\Terraquantum\\Bff\\V1\\Bff\\Project\\GPBMetadata\xea\x02(Com::Terraquantum::Bff::V1::Bff::Projectb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.bff.v1.bff.project.bff_project_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\'com.com.terraquantum.bff.v1.bff.projectB\026BffProjectServiceProtoP\001ZGterraquantum.swiss/tq42_grpc_client/com/terraquantum/bff/v1/bff/project\242\002\006CTBVBP\252\002#Com.Terraquantum.Bff.V1.Bff.Project\312\002#Com\\Terraquantum\\Bff\\V1\\Bff\\Project\342\002/Com\\Terraquantum\\Bff\\V1\\Bff\\Project\\GPBMetadata\352\002(Com::Terraquantum::Bff::V1::Bff::Project'
  _globals['_BFFPROJECTSERVICE']._serialized_start=510
  _globals['_BFFPROJECTSERVICE']._serialized_end=1139
# @@protoc_insertion_point(module_scope)

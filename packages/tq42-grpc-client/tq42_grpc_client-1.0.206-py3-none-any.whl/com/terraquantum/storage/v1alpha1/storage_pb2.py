# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/storage/v1alpha1/storage.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/com/terraquantum/storage/v1alpha1/storage.proto\x12!com.terraquantum.storage.v1alpha1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1b\x62uf/validate/validate.proto\"\xb5\x05\n\x0cStorageProto\x12\x18\n\x02id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\x02id\x12\x1e\n\x04name\x18\x02 \x01(\tB\n\xbaH\x07r\x05\x10\x02\x18\x80\x01R\x04name\x12*\n\x0b\x64\x65scription\x18\x03 \x01(\tB\x08\xbaH\x05r\x03\x18\x80\x04R\x0b\x64\x65scription\x12L\n\x04type\x18\x04 \x01(\x0e\x32..com.terraquantum.storage.v1alpha1.StorageTypeB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x04type\x12\'\n\nproject_id\x18\x05 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tprojectId\x12\'\n\ncreated_by\x18\x06 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\tcreatedBy\x12W\n\x06status\x18\x07 \x01(\x0e\x32\x35.com.terraquantum.storage.v1alpha1.StorageStatusProtoB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x06status\x12\x39\n\ncreated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x39\n\ndeleted_at\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tdeletedAt\x12\x64\n\x10\x64\x61taset_metadata\x18\x14 \x01(\x0b\x32\x37.com.terraquantum.storage.v1alpha1.DatasetMetadataProtoH\x00R\x0f\x64\x61tasetMetadata\x12^\n\x0emodel_metadata\x18\x15 \x01(\x0b\x32\x35.com.terraquantum.storage.v1alpha1.ModelMetadataProtoH\x00R\rmodelMetadataB\n\n\x08metadata\"t\n\x14\x44\x61tasetMetadataProto\x12\\\n\x0bsensitivity\x18\x01 \x01(\x0e\x32:.com.terraquantum.storage.v1alpha1.DatasetSensitivityProtoR\x0bsensitivity\"@\n\x12ModelMetadataProto\x12*\n\x11\x65xperiment_run_id\x18\x01 \x01(\tR\x0f\x65xperimentRunId*C\n\x0bStorageType\x12\x1c\n\x18STORAGE_TYPE_UNSPECIFIED\x10\x00\x12\x0b\n\x07\x44\x41TASET\x10\x01\x12\t\n\x05MODEL\x10\x02*\xad\x01\n\x12StorageStatusProto\x12\x1e\n\x1aSTORAGE_STATUS_UNSPECIFIED\x10\x00\x12\x0b\n\x07PENDING\x10\x01\x12\x0f\n\x0bINITIALIZED\x10\x02\x12\x10\n\x0cTRANSFERRING\x10\x03\x12\n\n\x06\x46\x41ILED\x10\x04\x12\r\n\tCOMPLETED\x10\x05\x12\x14\n\x10PENDING_DELETION\x10\x06\x12\x0b\n\x07\x44\x45LETED\x10\x07\x12\t\n\x05\x45MPTY\x10\x08*x\n\x17\x44\x61tasetSensitivityProto\x12#\n\x1f\x44\x41TASET_SENSITIVITY_UNSPECIFIED\x10\x00\x12\n\n\x06PUBLIC\x10\x01\x12\x0b\n\x07GENERAL\x10\x02\x12\r\n\tSENSITIVE\x10\x03\x12\x10\n\x0c\x43ONFIDENTIAL\x10\x04\x42\xb3\x02\n%com.com.terraquantum.storage.v1alpha1B\x0cStorageProtoP\x01ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/storage/v1alpha1;storagev1alpha1\xa2\x02\x03\x43TS\xaa\x02!Com.Terraquantum.Storage.V1alpha1\xca\x02!Com\\Terraquantum\\Storage\\V1alpha1\xe2\x02-Com\\Terraquantum\\Storage\\V1alpha1\\GPBMetadata\xea\x02$Com::Terraquantum::Storage::V1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.storage.v1alpha1.storage_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.com.terraquantum.storage.v1alpha1B\014StorageProtoP\001ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/storage/v1alpha1;storagev1alpha1\242\002\003CTS\252\002!Com.Terraquantum.Storage.V1alpha1\312\002!Com\\Terraquantum\\Storage\\V1alpha1\342\002-Com\\Terraquantum\\Storage\\V1alpha1\\GPBMetadata\352\002$Com::Terraquantum::Storage::V1alpha1'
  _globals['_STORAGEPROTO'].fields_by_name['id']._options = None
  _globals['_STORAGEPROTO'].fields_by_name['id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGEPROTO'].fields_by_name['name']._options = None
  _globals['_STORAGEPROTO'].fields_by_name['name']._serialized_options = b'\272H\007r\005\020\002\030\200\001'
  _globals['_STORAGEPROTO'].fields_by_name['description']._options = None
  _globals['_STORAGEPROTO'].fields_by_name['description']._serialized_options = b'\272H\005r\003\030\200\004'
  _globals['_STORAGEPROTO'].fields_by_name['type']._options = None
  _globals['_STORAGEPROTO'].fields_by_name['type']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_STORAGEPROTO'].fields_by_name['project_id']._options = None
  _globals['_STORAGEPROTO'].fields_by_name['project_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGEPROTO'].fields_by_name['created_by']._options = None
  _globals['_STORAGEPROTO'].fields_by_name['created_by']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_STORAGEPROTO'].fields_by_name['status']._options = None
  _globals['_STORAGEPROTO'].fields_by_name['status']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_STORAGETYPE']._serialized_start=1028
  _globals['_STORAGETYPE']._serialized_end=1095
  _globals['_STORAGESTATUSPROTO']._serialized_start=1098
  _globals['_STORAGESTATUSPROTO']._serialized_end=1271
  _globals['_DATASETSENSITIVITYPROTO']._serialized_start=1273
  _globals['_DATASETSENSITIVITYPROTO']._serialized_end=1393
  _globals['_STORAGEPROTO']._serialized_start=149
  _globals['_STORAGEPROTO']._serialized_end=842
  _globals['_DATASETMETADATAPROTO']._serialized_start=844
  _globals['_DATASETMETADATAPROTO']._serialized_end=960
  _globals['_MODELMETADATAPROTO']._serialized_start=962
  _globals['_MODELMETADATAPROTO']._serialized_end=1026
# @@protoc_insertion_point(module_scope)

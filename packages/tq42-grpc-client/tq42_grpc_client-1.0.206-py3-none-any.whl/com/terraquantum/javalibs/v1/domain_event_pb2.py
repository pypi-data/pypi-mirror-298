# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/javalibs/v1/domain_event.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/com/terraquantum/javalibs/v1/domain_event.proto\x12\x1c\x63om.terraquantum.javalibs.v1\x1a\x19google/protobuf/any.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x80\x02\n\x10\x44omainEventProto\x12\x1d\n\nevent_type\x18\x01 \x01(\tR\teventType\x12,\n\x06\x65ntity\x18\x02 \x01(\x0b\x32\x14.google.protobuf.AnyR\x06\x65ntity\x12!\n\x0c\x65ntity_class\x18\x03 \x01(\tR\x0b\x65ntityClass\x12\x19\n\x08trace_id\x18\x04 \x01(\tR\x07traceId\x12\x17\n\x07span_id\x18\x05 \x01(\tR\x06spanId\x12\x38\n\ttimestamp\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ttimestamp\x12\x0e\n\x02id\x18\x07 \x01(\tR\x02idB\x94\x02\n com.com.terraquantum.javalibs.v1B\x10\x44omainEventProtoP\x01ZKterraquantum.swiss/tq42_grpc_client/com/terraquantum/javalibs/v1;javalibsv1\xa2\x02\x03\x43TJ\xaa\x02\x1c\x43om.Terraquantum.Javalibs.V1\xca\x02\x1c\x43om\\Terraquantum\\Javalibs\\V1\xe2\x02(Com\\Terraquantum\\Javalibs\\V1\\GPBMetadata\xea\x02\x1f\x43om::Terraquantum::Javalibs::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.javalibs.v1.domain_event_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n com.com.terraquantum.javalibs.v1B\020DomainEventProtoP\001ZKterraquantum.swiss/tq42_grpc_client/com/terraquantum/javalibs/v1;javalibsv1\242\002\003CTJ\252\002\034Com.Terraquantum.Javalibs.V1\312\002\034Com\\Terraquantum\\Javalibs\\V1\342\002(Com\\Terraquantum\\Javalibs\\V1\\GPBMetadata\352\002\037Com::Terraquantum::Javalibs::V1'
  _globals['_DOMAINEVENTPROTO']._serialized_start=142
  _globals['_DOMAINEVENTPROTO']._serialized_end=398
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/credits/v1alpha1/consumption_service.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.credits.v1alpha1 import check_experiment_run_pb2 as com_dot_terraquantum_dot_credits_dot_v1alpha1_dot_check__experiment__run__pb2
from com.terraquantum.credits.v1alpha1 import list_transactions_by_org_pb2 as com_dot_terraquantum_dot_credits_dot_v1alpha1_dot_list__transactions__by__org__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;com/terraquantum/credits/v1alpha1/consumption_service.proto\x12!com.terraquantum.credits.v1alpha1\x1a<com/terraquantum/credits/v1alpha1/check_experiment_run.proto\x1a@com/terraquantum/credits/v1alpha1/list_transactions_by_org.proto\x1a\x1bgoogle/protobuf/empty.proto2\xba\x02\n\x12\x43onsumptionService\x12\x86\x01\n CheckExperimentRunAgainstCredits\x12J.com.terraquantum.credits.v1alpha1.CheckExperimentRunAgainstCreditsRequest\x1a\x16.google.protobuf.Empty\x12\x9a\x01\n\x15ListTransactionsByOrg\x12?.com.terraquantum.credits.v1alpha1.ListTransactionsByOrgRequest\x1a@.com.terraquantum.credits.v1alpha1.ListTransactionsByOrgResponseB\xbe\x02\n%com.com.terraquantum.credits.v1alpha1B\x17\x43onsumptionServiceProtoP\x01ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/credits/v1alpha1;creditsv1alpha1\xa2\x02\x03\x43TC\xaa\x02!Com.Terraquantum.Credits.V1alpha1\xca\x02!Com\\Terraquantum\\Credits\\V1alpha1\xe2\x02-Com\\Terraquantum\\Credits\\V1alpha1\\GPBMetadata\xea\x02$Com::Terraquantum::Credits::V1alpha1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.credits.v1alpha1.consumption_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.com.terraquantum.credits.v1alpha1B\027ConsumptionServiceProtoP\001ZUterraquantum.swiss/tq42_grpc_client/com/terraquantum/credits/v1alpha1;creditsv1alpha1\242\002\003CTC\252\002!Com.Terraquantum.Credits.V1alpha1\312\002!Com\\Terraquantum\\Credits\\V1alpha1\342\002-Com\\Terraquantum\\Credits\\V1alpha1\\GPBMetadata\352\002$Com::Terraquantum::Credits::V1alpha1'
  _globals['_CONSUMPTIONSERVICE']._serialized_start=256
  _globals['_CONSUMPTIONSERVICE']._serialized_end=570
# @@protoc_insertion_point(module_scope)

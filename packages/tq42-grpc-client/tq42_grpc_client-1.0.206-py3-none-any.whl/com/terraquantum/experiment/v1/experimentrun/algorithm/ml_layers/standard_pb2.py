# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/standard.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers import shared_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ml__layers_dot_shared__pb2
from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from com.terraquantum import default_value_pb2 as com_dot_terraquantum_dot_default__value__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nOcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/standard.proto\x12@com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers\x1aMcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/shared.proto\x1a\x1b\x62uf/validate/validate.proto\x1a$com/terraquantum/default_value.proto\"\x99\x01\n\x17\x41\x63tivationFunctionLayer\x12~\n\x08\x66unction\x18\x01 \x01(\x0e\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.ActFuncProtoB\x12\xbaH\x08\x82\x01\x02\x10\x01\xc8\x01\x01\x82\xa6\x1d\x03z\x01\x01R\x08\x66unction\"B\n\x0c\x44ropoutLayer\x12\x32\n\x05value\x18\x01 \x01(\x02\x42\x1c\xbaH\x0f\n\n\x1d\x00\x00\x80?%\x00\x00\x00\x00\xc8\x01\x01\x82\xa6\x1d\x06\n\x04\x00\x00\x00?R\x05value\"\x19\n\x17\x42\x61tchNormalizationLayerB\xe1\x03\nDcom.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layersB\rStandardProtoP\x01Zdterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers\xa2\x02\x07\x43TEVEAM\xaa\x02?Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm.MlLayers\xca\x02?Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\xe2\x02KCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\\GPBMetadata\xea\x02\x45\x43om::Terraquantum::Experiment::V1::Experimentrun::Algorithm::MlLayersb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.standard_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\nDcom.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layersB\rStandardProtoP\001Zdterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers\242\002\007CTEVEAM\252\002?Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm.MlLayers\312\002?Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\342\002KCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\\GPBMetadata\352\002ECom::Terraquantum::Experiment::V1::Experimentrun::Algorithm::MlLayers'
  _globals['_ACTIVATIONFUNCTIONLAYER'].fields_by_name['function']._options = None
  _globals['_ACTIVATIONFUNCTIONLAYER'].fields_by_name['function']._serialized_options = b'\272H\010\202\001\002\020\001\310\001\001\202\246\035\003z\001\001'
  _globals['_DROPOUTLAYER'].fields_by_name['value']._options = None
  _globals['_DROPOUTLAYER'].fields_by_name['value']._serialized_options = b'\272H\017\n\n\035\000\000\200?%\000\000\000\000\310\001\001\202\246\035\006\n\004\000\000\000?'
  _globals['_ACTIVATIONFUNCTIONLAYER']._serialized_start=296
  _globals['_ACTIVATIONFUNCTIONLAYER']._serialized_end=449
  _globals['_DROPOUTLAYER']._serialized_start=451
  _globals['_DROPOUTLAYER']._serialized_end=517
  _globals['_BATCHNORMALIZATIONLAYER']._serialized_start=519
  _globals['_BATCHNORMALIZATIONLAYER']._serialized_end=544
# @@protoc_insertion_point(module_scope)

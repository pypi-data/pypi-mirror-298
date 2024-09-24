# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/custom_quantum_layer.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from com.terraquantum import default_value_pb2 as com_dot_terraquantum_dot_default__value__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers import gate_cnot_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ml__layers_dot_gate__cnot__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers import gate_encoding_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ml__layers_dot_gate__encoding__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers import gate_hadamard_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ml__layers_dot_gate__hadamard__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers import gate_variational_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ml__layers_dot_gate__variational__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers import gate_measurement_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ml__layers_dot_gate__measurement__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n[com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/custom_quantum_layer.proto\x12@com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers\x1a\x1b\x62uf/validate/validate.proto\x1a$com/terraquantum/default_value.proto\x1aPcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/gate_cnot.proto\x1aTcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/gate_encoding.proto\x1aTcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/gate_hadamard.proto\x1aWcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/gate_variational.proto\x1aWcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers/gate_measurement.proto\"\xc1\x04\n\x04Gate\x12u\n\x0bvariational\x18\x01 \x01(\x0b\x32Q.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.VariationalGateH\x00R\x0bvariational\x12l\n\x08\x65ncoding\x18\x02 \x01(\x0b\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.EncodingGateH\x00R\x08\x65ncoding\x12`\n\x04\x63not\x18\x03 \x01(\x0b\x32J.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.CnotGateH\x00R\x04\x63not\x12l\n\x08hadamard\x18\x04 \x01(\x0b\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.HadamardGateH\x00R\x08hadamard\x12u\n\x0bmeasurement\x18\x05 \x01(\x0b\x32Q.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.MeasurementGateH\x00R\x0bmeasurementB\r\n\x04gate\x12\x05\xbaH\x02\x08\x01\"\xad\x01\n\x12\x43ustomQuantumLayer\x12/\n\nnum_qubits\x18\x01 \x01(\x05\x42\x10\xbaH\x06\x1a\x04\x18\x19(\x01\x82\xa6\x1d\x03\x1a\x01\x04R\tnumQubits\x12\x66\n\x05gates\x18\x02 \x03(\x0b\x32\x46.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.GateB\x08\xbaH\x05\x92\x01\x02\x08\x01R\x05gatesB\xeb\x03\nDcom.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layersB\x17\x43ustomQuantumLayerProtoP\x01Zdterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers\xa2\x02\x07\x43TEVEAM\xaa\x02?Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm.MlLayers\xca\x02?Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\xe2\x02KCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\\GPBMetadata\xea\x02\x45\x43om::Terraquantum::Experiment::V1::Experimentrun::Algorithm::MlLayersb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layers.custom_quantum_layer_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\nDcom.com.terraquantum.experiment.v1.experimentrun.algorithm.ml_layersB\027CustomQuantumLayerProtoP\001Zdterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm/ml_layers\242\002\007CTEVEAM\252\002?Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm.MlLayers\312\002?Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\342\002KCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\MlLayers\\GPBMetadata\352\002ECom::Terraquantum::Experiment::V1::Experimentrun::Algorithm::MlLayers'
  _globals['_GATE'].oneofs_by_name['gate']._options = None
  _globals['_GATE'].oneofs_by_name['gate']._serialized_options = b'\272H\002\010\001'
  _globals['_CUSTOMQUANTUMLAYER'].fields_by_name['num_qubits']._options = None
  _globals['_CUSTOMQUANTUMLAYER'].fields_by_name['num_qubits']._serialized_options = b'\272H\006\032\004\030\031(\001\202\246\035\003\032\001\004'
  _globals['_CUSTOMQUANTUMLAYER'].fields_by_name['gates']._options = None
  _globals['_CUSTOMQUANTUMLAYER'].fields_by_name['gates']._serialized_options = b'\272H\005\222\001\002\010\001'
  _globals['_GATE']._serialized_start=661
  _globals['_GATE']._serialized_end=1238
  _globals['_CUSTOMQUANTUMLAYER']._serialized_start=1241
  _globals['_CUSTOMQUANTUMLAYER']._serialized_end=1414
# @@protoc_insertion_point(module_scope)

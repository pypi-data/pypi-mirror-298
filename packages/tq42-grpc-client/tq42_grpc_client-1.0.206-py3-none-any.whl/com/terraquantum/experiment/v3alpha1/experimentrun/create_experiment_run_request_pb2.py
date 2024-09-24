# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/experiment/v3alpha1/experimentrun/create_experiment_run_request.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.experiment.v1.experimentrun.algorithm import circuit_run_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_circuit__run__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import cva_opt_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_cva__opt__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import shared_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_shared__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import tetra_opt_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_tetra__opt__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import tetra_quenc_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_tetra__quenc__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import toy_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_toy__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import ts_hqlstm_eval_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ts__hqlstm__eval__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import ts_hqlstm_train_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ts__hqlstm__train__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import ts_hqmlp_eval_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ts__hqmlp__eval__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import ts_hqmlp_train_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ts__hqmlp__train__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import ts_lstm_eval_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ts__lstm__eval__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import ts_lstm_train_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ts__lstm__train__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import ts_mlp_eval_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ts__mlp__eval__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import ts_mlp_train_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_ts__mlp__train__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import generic_ml_train_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_generic__ml__train__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import generic_ml_infer_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_generic__ml__infer__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import routing_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_routing__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import tq42_tqml_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_tq42__tqml__pb2
from com.terraquantum.experiment.v1.experimentrun.algorithm import optimax_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_optimax__pb2
from com.terraquantum.experiment.v1.experimentrun import experiment_run_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_experiment__run__pb2
from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nVcom/terraquantum/experiment/v3alpha1/experimentrun/create_experiment_run_request.proto\x12\x32\x63om.terraquantum.experiment.v3alpha1.experimentrun\x1aHcom/terraquantum/experiment/v1/experimentrun/algorithm/circuit_run.proto\x1a\x44\x63om/terraquantum/experiment/v1/experimentrun/algorithm/cva_opt.proto\x1a\x43\x63om/terraquantum/experiment/v1/experimentrun/algorithm/shared.proto\x1a\x46\x63om/terraquantum/experiment/v1/experimentrun/algorithm/tetra_opt.proto\x1aHcom/terraquantum/experiment/v1/experimentrun/algorithm/tetra_quenc.proto\x1a@com/terraquantum/experiment/v1/experimentrun/algorithm/toy.proto\x1aKcom/terraquantum/experiment/v1/experimentrun/algorithm/ts_hqlstm_eval.proto\x1aLcom/terraquantum/experiment/v1/experimentrun/algorithm/ts_hqlstm_train.proto\x1aJcom/terraquantum/experiment/v1/experimentrun/algorithm/ts_hqmlp_eval.proto\x1aKcom/terraquantum/experiment/v1/experimentrun/algorithm/ts_hqmlp_train.proto\x1aIcom/terraquantum/experiment/v1/experimentrun/algorithm/ts_lstm_eval.proto\x1aJcom/terraquantum/experiment/v1/experimentrun/algorithm/ts_lstm_train.proto\x1aHcom/terraquantum/experiment/v1/experimentrun/algorithm/ts_mlp_eval.proto\x1aIcom/terraquantum/experiment/v1/experimentrun/algorithm/ts_mlp_train.proto\x1aMcom/terraquantum/experiment/v1/experimentrun/algorithm/generic_ml_train.proto\x1aMcom/terraquantum/experiment/v1/experimentrun/algorithm/generic_ml_infer.proto\x1a\x44\x63om/terraquantum/experiment/v1/experimentrun/algorithm/routing.proto\x1a\x46\x63om/terraquantum/experiment/v1/experimentrun/algorithm/tq42_tqml.proto\x1a\x44\x63om/terraquantum/experiment/v1/experimentrun/algorithm/optimax.proto\x1a\x41\x63om/terraquantum/experiment/v1/experimentrun/experiment_run.proto\x1a\x1b\x62uf/validate/validate.proto\"\xc2\x15\n\x1a\x43reateExperimentRunRequest\x12-\n\rexperiment_id\x18\x01 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01R\x0c\x65xperimentId\x12\x61\n\x08hardware\x18\x02 \x01(\x0e\x32;.com.terraquantum.experiment.v1.experimentrun.HardwareProtoB\x08\xbaH\x05\x82\x01\x02\x10\x01R\x08hardware\x12n\n\talgorithm\x18\x03 \x01(\x0e\x32\x46.com.terraquantum.experiment.v1.experimentrun.algorithm.AlgorithmProtoB\x08\xbaH\x05\x82\x01\x02\x10\x01R\talgorithm\x12*\n\tparent_id\x18\x04 \x01(\tB\x08\xbaH\x05r\x03\xb0\x01\x01H\x01R\x08parentId\x88\x01\x01\x12\x83\x01\n\x14\x63ircuit_run_metadata\x18\x64 \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.CircuitRunMetadataProtoH\x00R\x12\x63ircuitRunMetadata\x12w\n\x10\x63va_opt_metadata\x18\x65 \x01(\x0b\x32K.com.terraquantum.experiment.v1.experimentrun.algorithm.CvaOptMetadataProtoH\x00R\x0e\x63vaOptMetadata\x12m\n\x0ctoy_metadata\x18\x66 \x01(\x0b\x32H.com.terraquantum.experiment.v1.experimentrun.algorithm.ToyMetadataProtoH\x00R\x0btoyMetadata\x12}\n\x12tetra_opt_metadata\x18g \x01(\x0b\x32M.com.terraquantum.experiment.v1.experimentrun.algorithm.TetraOptMetadataProtoH\x00R\x10tetraOptMetadata\x12\x83\x01\n\x14tetra_quenc_metadata\x18h \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.TetraQuEncMetadataProtoH\x00R\x12tetraQuencMetadata\x12\x8a\x01\n\x17ts_hqmlp_train_metadata\x18i \x01(\x0b\x32Q.com.terraquantum.experiment.v1.experimentrun.algorithm.TSHQMLPTrainMetadataProtoH\x00R\x14tsHqmlpTrainMetadata\x12\x87\x01\n\x16ts_hqmlp_eval_metadata\x18j \x01(\x0b\x32P.com.terraquantum.experiment.v1.experimentrun.algorithm.TSHQMLPEvalMetadataProtoH\x00R\x13tsHqmlpEvalMetadata\x12\x8d\x01\n\x18ts_hqlstm_train_metadata\x18k \x01(\x0b\x32R.com.terraquantum.experiment.v1.experimentrun.algorithm.TSHQLSTMTrainMetadataProtoH\x00R\x15tsHqlstmTrainMetadata\x12\x8a\x01\n\x17ts_hqlstm_eval_metadata\x18l \x01(\x0b\x32Q.com.terraquantum.experiment.v1.experimentrun.algorithm.TSHQLSTMEvalMetadataProtoH\x00R\x14tsHqlstmEvalMetadata\x12\x84\x01\n\x15ts_mlp_train_metadata\x18m \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.TSMLPTrainMetadataProtoH\x00R\x12tsMlpTrainMetadata\x12\x81\x01\n\x14ts_mlp_eval_metadata\x18n \x01(\x0b\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.TSMLPEvalMetadataProtoH\x00R\x11tsMlpEvalMetadata\x12\x87\x01\n\x16ts_lstm_train_metadata\x18o \x01(\x0b\x32P.com.terraquantum.experiment.v1.experimentrun.algorithm.TSLSTMTrainMetadataProtoH\x00R\x13tsLstmTrainMetadata\x12\x84\x01\n\x15ts_lstm_eval_metadata\x18p \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.TSLSTMEvalMetadataProtoH\x00R\x12tsLstmEvalMetadata\x12\x90\x01\n\x19generic_ml_train_metadata\x18q \x01(\x0b\x32S.com.terraquantum.experiment.v1.experimentrun.algorithm.GenericMLTrainMetadataProtoH\x00R\x16genericMlTrainMetadata\x12\x90\x01\n\x19generic_ml_infer_metadata\x18r \x01(\x0b\x32S.com.terraquantum.experiment.v1.experimentrun.algorithm.GenericMLInferMetadataProtoH\x00R\x16genericMlInferMetadata\x12y\n\x10routing_metadata\x18s \x01(\x0b\x32L.com.terraquantum.experiment.v1.experimentrun.algorithm.RoutingMetadataProtoH\x00R\x0froutingMetadata\x12p\n\rtqml_metadata\x18t \x01(\x0b\x32I.com.terraquantum.experiment.v1.experimentrun.algorithm.TQmlMetadataProtoH\x00R\x0ctqmlMetadata\x12y\n\x10optimax_metadata\x18u \x01(\x0b\x32L.com.terraquantum.experiment.v1.experimentrun.algorithm.OptimaxMetadataProtoH\x00R\x0foptimaxMetadataB\x11\n\x08metadata\x12\x05\xbaH\x02\x08\x01\x42\x0c\n\n_parent_idJ\x04\x08\x05\x10\x64\x42\x9f\x03\n6com.com.terraquantum.experiment.v3alpha1.experimentrunB\x1f\x43reateExperimentRunRequestProtoP\x01ZVterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v3alpha1/experimentrun\xa2\x02\x05\x43TEVE\xaa\x02\x32\x43om.Terraquantum.Experiment.V3alpha1.Experimentrun\xca\x02\x32\x43om\\Terraquantum\\Experiment\\V3alpha1\\Experimentrun\xe2\x02>Com\\Terraquantum\\Experiment\\V3alpha1\\Experimentrun\\GPBMetadata\xea\x02\x36\x43om::Terraquantum::Experiment::V3alpha1::Experimentrunb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v3alpha1.experimentrun.create_experiment_run_request_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n6com.com.terraquantum.experiment.v3alpha1.experimentrunB\037CreateExperimentRunRequestProtoP\001ZVterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v3alpha1/experimentrun\242\002\005CTEVE\252\0022Com.Terraquantum.Experiment.V3alpha1.Experimentrun\312\0022Com\\Terraquantum\\Experiment\\V3alpha1\\Experimentrun\342\002>Com\\Terraquantum\\Experiment\\V3alpha1\\Experimentrun\\GPBMetadata\352\0026Com::Terraquantum::Experiment::V3alpha1::Experimentrun'
  _globals['_CREATEEXPERIMENTRUNREQUEST'].oneofs_by_name['metadata']._options = None
  _globals['_CREATEEXPERIMENTRUNREQUEST'].oneofs_by_name['metadata']._serialized_options = b'\272H\002\010\001'
  _globals['_CREATEEXPERIMENTRUNREQUEST'].fields_by_name['experiment_id']._options = None
  _globals['_CREATEEXPERIMENTRUNREQUEST'].fields_by_name['experiment_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_CREATEEXPERIMENTRUNREQUEST'].fields_by_name['hardware']._options = None
  _globals['_CREATEEXPERIMENTRUNREQUEST'].fields_by_name['hardware']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_CREATEEXPERIMENTRUNREQUEST'].fields_by_name['algorithm']._options = None
  _globals['_CREATEEXPERIMENTRUNREQUEST'].fields_by_name['algorithm']._serialized_options = b'\272H\005\202\001\002\020\001'
  _globals['_CREATEEXPERIMENTRUNREQUEST'].fields_by_name['parent_id']._options = None
  _globals['_CREATEEXPERIMENTRUNREQUEST'].fields_by_name['parent_id']._serialized_options = b'\272H\005r\003\260\001\001'
  _globals['_CREATEEXPERIMENTRUNREQUEST']._serialized_start=1642
  _globals['_CREATEEXPERIMENTRUNREQUEST']._serialized_end=4396
# @@protoc_insertion_point(module_scope)

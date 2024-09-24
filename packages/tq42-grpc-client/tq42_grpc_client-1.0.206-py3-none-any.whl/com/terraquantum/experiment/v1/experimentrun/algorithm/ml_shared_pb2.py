# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/terraquantum/experiment/v1/experimentrun/algorithm/ml_shared.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from com.terraquantum.experiment.v1.experimentrun.algorithm import shared_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_experimentrun_dot_algorithm_dot_shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nFcom/terraquantum/experiment/v1/experimentrun/algorithm/ml_shared.proto\x12\x36\x63om.terraquantum.experiment.v1.experimentrun.algorithm\x1a\x43\x63om/terraquantum/experiment/v1/experimentrun/algorithm/shared.proto\"y\n\x12MLTrainInputsProto\x12\x63\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.DatasetStorageInfoProtoR\x04\x64\x61ta\"\x86\x02\n\x13MLTrainOutputsProto\x12\x63\n\x05model\x18\x01 \x01(\x0b\x32M.com.terraquantum.experiment.v1.experimentrun.algorithm.ModelStorageInfoProtoR\x05model\x12\x89\x01\n\x18inferred_evaluation_data\x18\x02 \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.DatasetStorageInfoProtoR\x16inferredEvaluationData\"\xa9\x01\n\x0f\x43onfusionMatrix\x12#\n\rtrue_positive\x18\x01 \x01(\x05R\x0ctruePositive\x12%\n\x0e\x66\x61lse_positive\x18\x02 \x01(\x05R\rfalsePositive\x12#\n\rtrue_negative\x18\x03 \x01(\x05R\x0ctrueNegative\x12%\n\x0e\x66\x61lse_negative\x18\x04 \x01(\x05R\rfalseNegative\"\xf4\x08\n\x07Metrics\x12\x10\n\x03mse\x18\x01 \x01(\x02R\x03mse\x12\x10\n\x03mae\x18\x02 \x01(\x02R\x03mae\x12i\n\x08\x61\x63\x63uracy\x18\x03 \x03(\x0b\x32M.com.terraquantum.experiment.v1.experimentrun.algorithm.Metrics.AccuracyEntryR\x08\x61\x63\x63uracy\x12l\n\tprecision\x18\x04 \x03(\x0b\x32N.com.terraquantum.experiment.v1.experimentrun.algorithm.Metrics.PrecisionEntryR\tprecision\x12\x63\n\x06recall\x18\x05 \x03(\x0b\x32K.com.terraquantum.experiment.v1.experimentrun.algorithm.Metrics.RecallEntryR\x06recall\x12W\n\x02\x66\x31\x18\x06 \x03(\x0b\x32G.com.terraquantum.experiment.v1.experimentrun.algorithm.Metrics.F1EntryR\x02\x66\x31\x12r\n\x0bspecificity\x18\x07 \x03(\x0b\x32P.com.terraquantum.experiment.v1.experimentrun.algorithm.Metrics.SpecificityEntryR\x0bspecificity\x12\x7f\n\x10\x63onfusion_matrix\x18\x08 \x03(\x0b\x32T.com.terraquantum.experiment.v1.experimentrun.algorithm.Metrics.ConfusionMatrixEntryR\x0f\x63onfusionMatrix\x1a;\n\rAccuracyEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x02R\x05value:\x02\x38\x01\x1a<\n\x0ePrecisionEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x02R\x05value:\x02\x38\x01\x1a\x39\n\x0bRecallEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x02R\x05value:\x02\x38\x01\x1a\x35\n\x07\x46\x31\x45ntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x02R\x05value:\x02\x38\x01\x1a>\n\x10SpecificityEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x02R\x05value:\x02\x38\x01\x1a\x8b\x01\n\x14\x43onfusionMatrixEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12]\n\x05value\x18\x02 \x01(\x0b\x32G.com.terraquantum.experiment.v1.experimentrun.algorithm.ConfusionMatrixR\x05value:\x02\x38\x01\"\xe4\x03\n\x12TSTrainResultProto\x12!\n\x0ctrain_losses\x18\x01 \x03(\x02R\x0btrainLosses\x12\x1f\n\x0btest_losses\x18\x02 \x03(\x02R\ntestLosses\x12\x18\n\x07version\x18\x03 \x01(\tR\x07version\x12\x64\n\rtrain_metrics\x18\x05 \x01(\x0b\x32?.com.terraquantum.experiment.v1.experimentrun.algorithm.MetricsR\x0ctrainMetrics\x12\x62\n\x0ctest_metrics\x18\x06 \x01(\x0b\x32?.com.terraquantum.experiment.v1.experimentrun.algorithm.MetricsR\x0btestMetrics\x12\x1d\n\ntime_label\x18\t \x01(\tR\ttimeLabel\x12!\n\x0coutput_label\x18\n \x01(\tR\x0boutputLabel\x12!\n\x0coutput_scale\x18\x0b \x01(\x02R\x0boutputScaleJ\x04\x08\x04\x10\x05J\x04\x08\x07\x10\x08J\x04\x08\x08\x10\tR\x10original_outputsR\ttimestampR\x12\x65valuation_outputs\"\xdd\x01\n\x11TSEvalInputsProto\x12\x63\n\x05model\x18\x01 \x01(\x0b\x32M.com.terraquantum.experiment.v1.experimentrun.algorithm.ModelStorageInfoProtoR\x05model\x12\x63\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.DatasetStorageInfoProtoR\x04\x64\x61ta\"\x8a\x01\n\x12TSEvalOutputsProto\x12t\n\rinferred_data\x18\x01 \x01(\x0b\x32O.com.terraquantum.experiment.v1.experimentrun.algorithm.DatasetStorageInfoProtoR\x0cinferredData\"\xbd\x01\n\x11TSEvalResultProto\x12\x18\n\x07version\x18\x02 \x01(\tR\x07version\x12\x1d\n\ntime_label\x18\x04 \x01(\tR\ttimeLabel\x12!\n\x0coutput_label\x18\x05 \x01(\tR\x0boutputLabel\x12!\n\x0coutput_scale\x18\x06 \x01(\x02R\x0boutputScaleJ\x04\x08\x01\x10\x02J\x04\x08\x03\x10\x04R\x12\x65valuation_outputsR\ttimestamp\"K\n\x13TrainModelInfoProto\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x02 \x01(\tR\x0b\x64\x65scription*A\n\nOptimProto\x12\x15\n\x11OPTIM_UNSPECIFIED\x10\x00\x12\x08\n\x04\x41\x44\x41M\x10\x01\x12\t\n\x05\x41\x44\x41MW\x10\x02\x12\x07\n\x03SGD\x10\x03*W\n\rLossFuncProto\x12\x19\n\x15LOSS_FUNC_UNSPECIFIED\x10\x00\x12\x07\n\x03MSE\x10\x01\x12\x07\n\x03MAE\x10\x02\x12\x07\n\x03\x42\x43\x45\x10\x03\x12\x10\n\x0c\x43ROSSENTROPY\x10\x04\x42\xa7\x03\n:com.com.terraquantum.experiment.v1.experimentrun.algorithmB\rMlSharedProtoP\x01ZZterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm\xa2\x02\x06\x43TEVEA\xaa\x02\x36\x43om.Terraquantum.Experiment.V1.Experimentrun.Algorithm\xca\x02\x36\x43om\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\xe2\x02\x42\x43om\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\GPBMetadata\xea\x02;Com::Terraquantum::Experiment::V1::Experimentrun::Algorithmb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'com.terraquantum.experiment.v1.experimentrun.algorithm.ml_shared_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n:com.com.terraquantum.experiment.v1.experimentrun.algorithmB\rMlSharedProtoP\001ZZterraquantum.swiss/tq42_grpc_client/com/terraquantum/experiment/v1/experimentrun/algorithm\242\002\006CTEVEA\252\0026Com.Terraquantum.Experiment.V1.Experimentrun.Algorithm\312\0026Com\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\342\002BCom\\Terraquantum\\Experiment\\V1\\Experimentrun\\Algorithm\\GPBMetadata\352\002;Com::Terraquantum::Experiment::V1::Experimentrun::Algorithm'
  _globals['_METRICS_ACCURACYENTRY']._options = None
  _globals['_METRICS_ACCURACYENTRY']._serialized_options = b'8\001'
  _globals['_METRICS_PRECISIONENTRY']._options = None
  _globals['_METRICS_PRECISIONENTRY']._serialized_options = b'8\001'
  _globals['_METRICS_RECALLENTRY']._options = None
  _globals['_METRICS_RECALLENTRY']._serialized_options = b'8\001'
  _globals['_METRICS_F1ENTRY']._options = None
  _globals['_METRICS_F1ENTRY']._serialized_options = b'8\001'
  _globals['_METRICS_SPECIFICITYENTRY']._options = None
  _globals['_METRICS_SPECIFICITYENTRY']._serialized_options = b'8\001'
  _globals['_METRICS_CONFUSIONMATRIXENTRY']._options = None
  _globals['_METRICS_CONFUSIONMATRIXENTRY']._serialized_options = b'8\001'
  _globals['_OPTIMPROTO']._serialized_start=3023
  _globals['_OPTIMPROTO']._serialized_end=3088
  _globals['_LOSSFUNCPROTO']._serialized_start=3090
  _globals['_LOSSFUNCPROTO']._serialized_end=3177
  _globals['_MLTRAININPUTSPROTO']._serialized_start=199
  _globals['_MLTRAININPUTSPROTO']._serialized_end=320
  _globals['_MLTRAINOUTPUTSPROTO']._serialized_start=323
  _globals['_MLTRAINOUTPUTSPROTO']._serialized_end=585
  _globals['_CONFUSIONMATRIX']._serialized_start=588
  _globals['_CONFUSIONMATRIX']._serialized_end=757
  _globals['_METRICS']._serialized_start=760
  _globals['_METRICS']._serialized_end=1900
  _globals['_METRICS_ACCURACYENTRY']._serialized_start=1459
  _globals['_METRICS_ACCURACYENTRY']._serialized_end=1518
  _globals['_METRICS_PRECISIONENTRY']._serialized_start=1520
  _globals['_METRICS_PRECISIONENTRY']._serialized_end=1580
  _globals['_METRICS_RECALLENTRY']._serialized_start=1582
  _globals['_METRICS_RECALLENTRY']._serialized_end=1639
  _globals['_METRICS_F1ENTRY']._serialized_start=1641
  _globals['_METRICS_F1ENTRY']._serialized_end=1694
  _globals['_METRICS_SPECIFICITYENTRY']._serialized_start=1696
  _globals['_METRICS_SPECIFICITYENTRY']._serialized_end=1758
  _globals['_METRICS_CONFUSIONMATRIXENTRY']._serialized_start=1761
  _globals['_METRICS_CONFUSIONMATRIXENTRY']._serialized_end=1900
  _globals['_TSTRAINRESULTPROTO']._serialized_start=1903
  _globals['_TSTRAINRESULTPROTO']._serialized_end=2387
  _globals['_TSEVALINPUTSPROTO']._serialized_start=2390
  _globals['_TSEVALINPUTSPROTO']._serialized_end=2611
  _globals['_TSEVALOUTPUTSPROTO']._serialized_start=2614
  _globals['_TSEVALOUTPUTSPROTO']._serialized_end=2752
  _globals['_TSEVALRESULTPROTO']._serialized_start=2755
  _globals['_TSEVALRESULTPROTO']._serialized_end=2944
  _globals['_TRAINMODELINFOPROTO']._serialized_start=2946
  _globals['_TRAINMODELINFOPROTO']._serialized_end=3021
# @@protoc_insertion_point(module_scope)

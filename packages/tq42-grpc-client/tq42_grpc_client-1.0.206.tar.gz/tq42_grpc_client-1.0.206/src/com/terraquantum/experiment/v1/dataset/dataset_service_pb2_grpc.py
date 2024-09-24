# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from com.terraquantum.experiment.v1.dataset import create_dataset_request_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_create__dataset__request__pb2
from com.terraquantum.experiment.v1.dataset import dataset_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_dataset__pb2
from com.terraquantum.experiment.v1.dataset import delete_datasets_request_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_delete__datasets__request__pb2
from com.terraquantum.experiment.v1.dataset import delete_datasets_response_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_delete__datasets__response__pb2
from com.terraquantum.experiment.v1.dataset import get_dataset_count_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__count__pb2
from com.terraquantum.experiment.v1.dataset import get_dataset_request_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__request__pb2
from com.terraquantum.experiment.v1.dataset import list_datasets_pb2 as com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_list__datasets__pb2


class DatasetServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListDatasets = channel.unary_unary(
                '/com.terraquantum.experiment.v1.dataset.DatasetService/ListDatasets',
                request_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_list__datasets__pb2.ListDatasetsRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_list__datasets__pb2.ListDatasetsResponse.FromString,
                )
        self.CreateDataset = channel.unary_unary(
                '/com.terraquantum.experiment.v1.dataset.DatasetService/CreateDataset',
                request_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_create__dataset__request__pb2.CreateDatasetRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_dataset__pb2.DatasetProto.FromString,
                )
        self.GetDataset = channel.unary_unary(
                '/com.terraquantum.experiment.v1.dataset.DatasetService/GetDataset',
                request_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__request__pb2.GetDatasetRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_dataset__pb2.DatasetProto.FromString,
                )
        self.DeleteDatasets = channel.unary_unary(
                '/com.terraquantum.experiment.v1.dataset.DatasetService/DeleteDatasets',
                request_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_delete__datasets__request__pb2.DeleteDatasetsRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_delete__datasets__response__pb2.DeleteDatasetsResponse.FromString,
                )
        self.GetDatasetCount = channel.unary_unary(
                '/com.terraquantum.experiment.v1.dataset.DatasetService/GetDatasetCount',
                request_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__count__pb2.GetDatasetCountRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__count__pb2.GetDatasetCountResponse.FromString,
                )


class DatasetServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListDatasets(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateDataset(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDataset(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDatasets(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDatasetCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatasetServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListDatasets': grpc.unary_unary_rpc_method_handler(
                    servicer.ListDatasets,
                    request_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_list__datasets__pb2.ListDatasetsRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_list__datasets__pb2.ListDatasetsResponse.SerializeToString,
            ),
            'CreateDataset': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateDataset,
                    request_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_create__dataset__request__pb2.CreateDatasetRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_dataset__pb2.DatasetProto.SerializeToString,
            ),
            'GetDataset': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDataset,
                    request_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__request__pb2.GetDatasetRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_dataset__pb2.DatasetProto.SerializeToString,
            ),
            'DeleteDatasets': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteDatasets,
                    request_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_delete__datasets__request__pb2.DeleteDatasetsRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_delete__datasets__response__pb2.DeleteDatasetsResponse.SerializeToString,
            ),
            'GetDatasetCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDatasetCount,
                    request_deserializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__count__pb2.GetDatasetCountRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__count__pb2.GetDatasetCountResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.terraquantum.experiment.v1.dataset.DatasetService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DatasetService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListDatasets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.terraquantum.experiment.v1.dataset.DatasetService/ListDatasets',
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_list__datasets__pb2.ListDatasetsRequest.SerializeToString,
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_list__datasets__pb2.ListDatasetsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateDataset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.terraquantum.experiment.v1.dataset.DatasetService/CreateDataset',
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_create__dataset__request__pb2.CreateDatasetRequest.SerializeToString,
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_dataset__pb2.DatasetProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDataset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.terraquantum.experiment.v1.dataset.DatasetService/GetDataset',
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__request__pb2.GetDatasetRequest.SerializeToString,
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_dataset__pb2.DatasetProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDatasets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.terraquantum.experiment.v1.dataset.DatasetService/DeleteDatasets',
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_delete__datasets__request__pb2.DeleteDatasetsRequest.SerializeToString,
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_delete__datasets__response__pb2.DeleteDatasetsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDatasetCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.terraquantum.experiment.v1.dataset.DatasetService/GetDatasetCount',
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__count__pb2.GetDatasetCountRequest.SerializeToString,
            com_dot_terraquantum_dot_experiment_dot_v1_dot_dataset_dot_get__dataset__count__pb2.GetDatasetCountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

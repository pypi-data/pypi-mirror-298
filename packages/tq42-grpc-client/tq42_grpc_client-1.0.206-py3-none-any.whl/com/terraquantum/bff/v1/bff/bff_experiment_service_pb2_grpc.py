# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from com.terraquantum.bff.v1.bff import get_experiment_count_pb2 as com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_get__experiment__count__pb2


class BffExperimentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetExperimentCount = channel.unary_unary(
                '/com.terraquantum.bff.v1.bff.BffExperimentService/GetExperimentCount',
                request_serializer=com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_get__experiment__count__pb2.GetExperimentCountRequest.SerializeToString,
                response_deserializer=com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_get__experiment__count__pb2.GetExperimentCountResponse.FromString,
                )


class BffExperimentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetExperimentCount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BffExperimentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetExperimentCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetExperimentCount,
                    request_deserializer=com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_get__experiment__count__pb2.GetExperimentCountRequest.FromString,
                    response_serializer=com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_get__experiment__count__pb2.GetExperimentCountResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.terraquantum.bff.v1.bff.BffExperimentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BffExperimentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetExperimentCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.terraquantum.bff.v1.bff.BffExperimentService/GetExperimentCount',
            com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_get__experiment__count__pb2.GetExperimentCountRequest.SerializeToString,
            com_dot_terraquantum_dot_bff_dot_v1_dot_bff_dot_get__experiment__count__pb2.GetExperimentCountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import rpc_pb2 as rpc__pb2


class ReplicatorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.replicateMsg = channel.unary_unary(
                '/rpc.Replicator/replicateMsg',
                request_serializer=rpc__pb2.Request.SerializeToString,
                response_deserializer=rpc__pb2.Response.FromString,
                )


class ReplicatorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def replicateMsg(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReplicatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'replicateMsg': grpc.unary_unary_rpc_method_handler(
                    servicer.replicateMsg,
                    request_deserializer=rpc__pb2.Request.FromString,
                    response_serializer=rpc__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc.Replicator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Replicator(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def replicateMsg(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.Replicator/replicateMsg',
            rpc__pb2.Request.SerializeToString,
            rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

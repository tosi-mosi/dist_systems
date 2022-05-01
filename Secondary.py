import asyncio
import grpc
import rpc_pb2
import rpc_pb2_grpc
from aiohttp import web
import sys
log = []

# potentially secondary could run rpc server and web server separately, but would need to share data somehow one with another

# GRPC server
class Replicator(rpc_pb2_grpc.ReplicatorServicer):
    async def replicateMsg(
            self, request: rpc_pb2.Request,
            context: grpc.aio.ServicerContext) -> rpc_pb2.Response:
        print("replicating")
        log.append(request.msg)
        return rpc_pb2.Response(success=True)

async def serve() -> None:
    server = grpc.aio.server()
    rpc_pb2_grpc.add_ReplicatorServicer_to_server(Replicator(), server)
    listen_addr = '192.168.16.3:50051'
    server.add_insecure_port(listen_addr)
    # logging.info("Starting server on %s", listen_addr)
    print("starting server")
    await server.start()
    await server.wait_for_termination()

# HTTP server
async def handle_list(request):
    return web.Response(text="\n".join(log))

# Main
async def main():
    app = web.Application()
    app.add_routes([web.get('/list', handle_list)])
    await asyncio.gather(serve(), web._run_app(app))
    # await asyncio.gather(serve())

asyncio.run(main())
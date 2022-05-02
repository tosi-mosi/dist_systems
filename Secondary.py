import asyncio
import grpc
import rpc_pb2
import rpc_pb2_grpc
from aiohttp import web
import logging
import sys
import re
import subprocess

log = []

# potentially secondary could run rpc server and web server separately, but would need to share data somehow one with another.

def get_eth0_ipv4():
    ipv4_re = re.compile(r'.*inet\s+(.*)/')
    ip_output = subprocess.Popen('ip -family inet a s dev eth0', shell=True, stdout=subprocess.PIPE).stdout.read()
    line_with_ipv4 = ip_output.decode().split('\n')[1]
    res = ipv4_re.match(line_with_ipv4)
    return res.group(1)

async def delay(secs):
    logging.info('Sleeping for %s sec...', secs)
    await asyncio.sleep(secs)

# GRPC server
class Replicator(rpc_pb2_grpc.ReplicatorServicer):
    async def replicateMsg(
            self, request: rpc_pb2.Request,
            context: grpc.aio.ServicerContext) -> rpc_pb2.Response:
        logging.info('Processing gRPC request')

        if (len(sys.argv) > 1):
            await delay(int(sys.argv[1]))
        
        log.append(request.msg)
        logging.info('%s was appened to replica-log\n', request.msg)
        return rpc_pb2.Response(success=True)

async def rpc_serve() -> None:
    server = grpc.aio.server()
    rpc_pb2_grpc.add_ReplicatorServicer_to_server(Replicator(), server)
    listen_addr = f'{get_eth0_ipv4()}:50051'
    server.add_insecure_port(listen_addr)
    logging.info('Starting server on %s', listen_addr)
    await server.start()
    await server.wait_for_termination()

# HTTP server
async def handle_list(request):
    return web.Response(text='\n'.join(log))

# Main
async def main():
    app = web.Application()
    app.add_routes([web.get('/list', handle_list)])
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s.%(msecs)03d] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%H:%M:%S',
        stream=sys.stdout)
    await asyncio.gather(rpc_serve(), web._run_app(app, access_log=None))

asyncio.run(main())
import asyncio
import grpc
import rpc_pb2
import rpc_pb2_grpc
from aiohttp import web
import logging
import sys

log = []

# how to specify timout on request?
# Plus I need multiple connections to multiple secondaries

# GRPC clients
# For more channel options, please see https://grpc.io/grpc/core/group__grpc__arg__keys.html
CHANNEL_OPTIONS = [
    # ('grpc.lb_policy_name', 'pick_first'),
    # ('grpc.enable_retries', 0),
    # ('grpc.keepalive_timeout_ms', 10000)
]
secondaries_ips = [
    '192.168.16.3',
    '192.168.16.4'
]

async def replicate_msg(sec_ip, msg):
    # this will recreate channel on every single request, is it OK ?
    # need to understand what is this channel
    async with grpc.aio.insecure_channel(target=f'{sec_ip}:{50051}',
                                         options=CHANNEL_OPTIONS) as channel:
        stub = rpc_pb2_grpc.ReplicatorStub(channel)
        # response = await stub.replicateMsg(rpc_pb2.Request(msg=msg),
        #                                timeout=10)
        logging.info('Waiting for gRPC response from %s', sec_ip)
        response = await stub.replicateMsg(rpc_pb2.Request(msg=msg))
    logging.info('%s on %s', 'Success' if response.success else 'Fail', sec_ip)
    return (sec_ip, response.success)

# HTTP server
# https://demos.aiohttp.org/en/latest/tutorial.html#aiohttp-demos-polls-getting-started
async def handle_list(request):
    return web.Response(text="\n".join(log))

async def handle_append(request):
    logging.info('Processing http request from %r', request.remote)
    msg = await request.text()
    acks_info = await asyncio.gather(*[replicate_msg(s, msg) for s in secondaries_ips])
    logging.info(f'ACKs: {acks_info}\n')
    if all([ack[1] for ack in acks_info]):
        log.append(msg)
        return web.Response(text=f'Appending {msg} to in-memory list')
    else:
        # here some secondaries could have added msg, but some didn't. And master didn't.
        return web.Response(text=f'Got not enough ACKs from secondaries')

app = web.Application()
app.add_routes([web.get('/list', handle_list),
                web.post('/append', handle_append)])
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s.%(msecs)03d] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout)
web.run_app(app, access_log=None)
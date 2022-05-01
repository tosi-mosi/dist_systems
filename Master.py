import asyncio
import grpc
import rpc_pb2
import rpc_pb2_grpc
from aiohttp import web
import sys

log = ["hello"]

# I need an ACK from all
# how to specify timout on request?
# Plus I need multiple connections to multiple secondaries

# GRPC clients
# For more channel options, please see https://grpc.io/grpc/core/group__grpc__arg__keys.html
CHANNEL_OPTIONS = [('grpc.lb_policy_name', 'pick_first'),
                   ('grpc.enable_retries', 0),
                   ('grpc.keepalive_timeout_ms', 10000)]
secondaries_ips = ['192.168.16.3']

async def replicate_msg(sec_ip, msg):
    # this will recreate channel on every single request, is it OK ?
    # need to understand what is this channel
    async with grpc.aio.insecure_channel(target=f'{sec_ip}:{50051}',
                                         options=CHANNEL_OPTIONS) as channel:
        stub = rpc_pb2_grpc.ReplicatorStub(channel)
        response = await stub.replicateMsg(rpc_pb2.Request(msg=msg),
                                       timeout=10)
    print('Success' if response.success else 'Fail', f' on {sec_ip}')


# HTTP server
# https://demos.aiohttp.org/en/latest/tutorial.html#aiohttp-demos-polls-getting-started
async def handle_list(request):
    return web.Response(text="\n".join(log))

async def handle_append(request):
    msg = await request.text()
    log.append(msg)
    await asyncio.gather(*[replicate_msg(s, msg) for s in secondaries_ips])
    # after this need to blocking-wait for ACKS
    return web.Response(text=f'Appending {msg} to in-memory list')

app = web.Application()
app.add_routes([web.get('/list', handle_list),
                web.post('/append', handle_append)])
web.run_app(app)
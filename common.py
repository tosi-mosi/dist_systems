import asyncio
import logging
import grpc
import os
import re
import subprocess

BACKOFF_INIT = 1
BACKOFF_MULTIPLIER = 2
MAX_BACKOFF = 32

async def retry(task, *args, delay=BACKOFF_INIT, **kwargs):
	try:
		return await task(*args, **kwargs)
	except Exception as e:
		error_output = e._code if isinstance(e, grpc.RpcError) and not os.getenv('DEBUG') else e
		logging.error(f'Retry of {task.__name__}(args={args}, kwargs={kwargs}) got error: {error_output}. Retring again in: {delay:.2f}s')
		await asyncio.sleep(delay)
		new_delay = delay*BACKOFF_MULTIPLIER
		return await retry(task, *args, delay=new_delay if new_delay < MAX_BACKOFF else MAX_BACKOFF, **kwargs)

def get_eth0_ipv4():
    ipv4_re = re.compile(r'.*inet\s+(.*)/')
    ip_output = subprocess.Popen('ip -family inet a s dev eth0', shell=True, stdout=subprocess.PIPE).stdout.read()
    line_with_ipv4 = ip_output.decode().split('\n')[1]
    res = ipv4_re.match(line_with_ipv4)
    return res.group(1)
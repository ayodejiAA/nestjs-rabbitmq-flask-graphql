import logging
import asyncio
from typing import Any
from enum import Enum

from aio_pika import connect_robust
from aio_pika.patterns import JsonRPC
from aio_pika.message import IncomingMessage
from aio_pika.exceptions import AMQPException

log = logging.getLogger(__name__)


class RPCMessageTypes(Enum):
    error = "err"
    result = "response"
    call = "call"


class RPC(JsonRPC):
    async def on_result_message(self, message: IncomingMessage):
        correlation_id = (
            int(message.correlation_id) if message.correlation_id else None
        )

        future = self.futures.pop(correlation_id, None)

        if future is None:
            log.warning("Unknown message: %r", message)
            return

        try:
            payload = self.deserialize(message.body)
        except Exception as e:
            log.error("Failed to deserialize response on message: %r", message)
            future.set_exception(e)
            return

        if RPCMessageTypes.result.value in payload:
            future.set_result(payload[RPCMessageTypes.result.value])

        elif RPCMessageTypes.error.value in payload:
            future.set_exception(AMQPException(
                payload[RPCMessageTypes.error.value]))

        elif message.type == RPCMessageTypes.call.value:
            future.set_exception(
                asyncio.TimeoutError("Message timed-out", message),
            )

        else:
            future.set_exception(
                RuntimeError("Unknown message type %r" % message.type),
            )

    def serialize(self, data: Any) -> bytes:
        return self.SERIALIZER.dumps(data, ensure_ascii=False, default=repr).encode()

    def deserialize(self, data: bytes) -> Any:
        return self.SERIALIZER.loads(data)


class ClientRPC:
    def __init__(self, **kwargs):
        self.url = kwargs["url"]
        self.routing_key = kwargs['routing_key']
        self.id = "client_rpc_py"
        print("ClientRPC Initialized ✅")

    async def __main(self, pattern, data):
        connection = await connect_robust(self.url, client_properties={"connection_name": "caller"})

        async with connection:
            channel = await connection.channel()
            rpc = await RPC.create(channel)
            return await rpc.call(self.routing_key, dict(id=self.id, pattern=pattern, data=data))

    def send(self, pattern, data=None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.__main(pattern, data))

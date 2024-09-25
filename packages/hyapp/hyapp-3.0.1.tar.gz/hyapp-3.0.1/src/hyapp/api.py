import dataclasses
import logging
import re
from contextvars import ContextVar

import starlette.datastructures
import starlette.types

from .trace import TRACE_ID_VAR, new_trace_id

LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass()
class TraceIdMiddleware:
    app: starlette.types.ASGIApp
    header_name: str = "X-Request-ID"
    header_validation_re: str = r"^[a-z0-9]{12,20}$"
    trace_id_var: ContextVar[str | None] = TRACE_ID_VAR
    trace_id_prefix: str = "aa"  # "API App"

    def _new_trace_id(self, parent: str | None = None) -> str:
        return new_trace_id(self.trace_id_prefix, parent=parent)

    async def __call__(
        self, scope: starlette.types.Scope, receive: starlette.types.Receive, send: starlette.types.Send
    ) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        headers = starlette.datastructures.MutableHeaders(scope=scope)
        header_value = headers.get(self.header_name.lower())
        parent_trace_id = None
        if header_value:
            if re.search(self.header_validation_re, header_value):
                parent_trace_id = header_value
            else:
                LOGGER.debug("Invalid trace id in header %r: %r", self.header_name, header_value)

        trace_id = self._new_trace_id(parent=parent_trace_id)

        self.trace_id_var.set(trace_id)

        async def handle_outgoing_request(message: starlette.types.Message) -> None:
            local_trace_id = self.trace_id_var.get()
            if message["type"] == "http.response.start" and local_trace_id:
                headers = starlette.datastructures.MutableHeaders(scope=message)
                headers.append(self.header_name, local_trace_id)

            await send(message)

        await self.app(scope, receive, handle_outgoing_request)

from starlette.middleware.base import BaseHTTPMiddleware

class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.headers.get("content-type") == "text/event-stream; charset=utf-8":
            response.headers["content-type"] = "text/event-stream"
        return response

# app/middleware.py
from fastapi import Request


async def log_request_body(request: Request, call_next):
    body = await request.body()
    print("RAW BODY:", body.decode())
    response = await call_next(request)
    return response

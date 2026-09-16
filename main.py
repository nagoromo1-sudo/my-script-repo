"""
FastAPI webhook server.

Exposes a single POST /webhook endpoint intended to receive alerts
(e.g. from TradingView or another signal source) and a GET /health
endpoint for uptime checks / Render health checks.

Auth: pass a shared secret in the `X-Webhook-Secret` header. Set the
expected value via the WEBHOOK_SECRET environment variable on Render.
If WEBHOOK_SECRET is not set, auth is skipped (useful for local dev
only -- always set it in production).
"""

import logging
import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook")

app = FastAPI(title="Webhook Server")

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")


@app.get("/health")
async def health() -> dict[str, str]:
    """Simple liveness check for Render / uptime monitors."""
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(
    request: Request,
    x_webhook_secret: str | None = Header(default=None),
) -> JSONResponse:
    if WEBHOOK_SECRET:
        if x_webhook_secret != WEBHOOK_SECRET:
            raise HTTPException(status_code=401, detail="invalid or missing webhook secret")

    payload: Any
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="body must be valid JSON")

    logger.info("Received webhook payload: %s", payload)

    # ---------------------------------------------------------------
    # Placeholder: strategy/trade logic goes here.
    # Nothing below this point executes any trade or external action
    # yet -- this just accepts and logs the payload.
    # ---------------------------------------------------------------

    return JSONResponse(content={"status": "received"})


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "webhook-server", "status": "running"}

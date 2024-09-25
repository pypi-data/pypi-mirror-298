import asyncio
import json
import logging
from logging.config import dictConfig
from pathlib import Path

from aiortc import RTCSessionDescription
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket, WebSocketDisconnect

from whipweb.settings import LOGGING_CONFIG

BASE_DIR = Path(__file__).parent.absolute()

websocket_client = None

ws_exchange_queue = asyncio.Queue()

dictConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger(__name__)


async def whip_offer(request: Request):
    global websocket_client

    sdp_data = await request.body()
    sdp_str = sdp_data.decode("utf-8")

    offer = RTCSessionDescription(sdp=sdp_str, type="offer")

    if websocket_client:
        await websocket_client.send_text(
            json.dumps(
                {
                    "format": "application/vnd.whippyweb.connection+json",
                    "type": "connection-offer",
                    "payload": {
                        "sdp": offer.sdp,
                        "type": offer.type,
                    },
                }
            )
        )
    else:
        raise Exception("WebSocket client not connected")

    answer = await ws_exchange_queue.get()

    return Response(
        content=answer.sdp,
        headers={"Content-Type": "application/sdp", "Location": "/whip"},
        status_code=201,
    )


async def whip_delete(request: Request):
    global websocket_client

    if websocket_client:
        await websocket_client.send_text(
            json.dumps(
                {
                    "format": "application/vnd.whippyweb.connection+json",
                    "type": "connection-close",
                }
            )
        )

    return Response(status_code=200)


async def websocket_endpoint(websocket: WebSocket):
    global websocket_client
    await websocket.accept()
    websocket_client = websocket

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            if data["type"] == "connection-answer":
                answer = RTCSessionDescription(
                    sdp=data["payload"]["sdp"], type=data["payload"]["type"]
                )
                await ws_exchange_queue.put(answer)
    except WebSocketDisconnect:
        LOGGER.info("WebSocket disconnected")
    except Exception:
        LOGGER.exception("WebSocket error")
    finally:
        websocket_client = None


async def serve_player(request):
    with open(BASE_DIR / "index.html") as f:
        html_content = f.read()
    return HTMLResponse(
        content=html_content,
        headers={"Content-Type": "text/html", "Cache-Control": "no-cache"},
    )


app = Starlette(
    debug=True,
    routes=[
        Route("/whip", whip_offer, methods=["POST"]),
        Route("/whip", whip_delete, methods=["DELETE"]),
        Route("/player", serve_player),
        WebSocketRoute("/ws", websocket_endpoint),
        Mount("/static", app=StaticFiles(directory=BASE_DIR / "static"), name="static"),
    ],
)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio

from utils.db import database
from routers import routers


app = FastAPI()

loop = asyncio.get_event_loop()


app.include_router(routers.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def index():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Bewise_test</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

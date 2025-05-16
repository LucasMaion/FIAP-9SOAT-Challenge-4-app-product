"""
This is a FastFood API. 🍔

It implements all the necessary endpoints to manage a FastFood restaurant.
Allowing the creation of clients, products, and purchases.
Managing the queue of purchases and the status of the purchases.

It was developed as a challenge project for the FIAP Software Architecture Post Graduation 9th class.
"""

import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBearer

from builder import build_db, seed_db
from src.adapters.driven.infra.database.db import start_db
from src.adapters.driver.API import (
    cliente_router,
    payment_router,
    pedido_router,
    produto_router,
    queue_router,
    maintenance_router,
    web_hook_example_router,
)

auth_scheme = HTTPBearer()


def get_token(token: str = Depends(auth_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


STAGE_PREFIX = os.getenv("STAGE_PREFIX", "dev")
app = FastAPI(
    title="FastFood API - FIAP-9SOAT 🚀",
    description=__doc__,
    summary="Challenge project for FIAP Software Architecture Post Graduation 9th class.",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Lucas Maion",
        "url": "https://github.com/LucasMaion",
        "email": "lucasmgois@outlook.com",
    },
    license_info={
        "name": "MIT License",
        "identifier": "MIT",
    },
)

start_db()
if int(os.getenv("DB_BUILD", 0)):
    build_db()
if int(os.getenv("DB_SEED", 0)):
    seed_db()


@app.get(f"/{STAGE_PREFIX}/new_docs", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url=f"/{STAGE_PREFIX}/openapijson",
        title="FastFood API - Swagger UI",
    )


@app.get(f"/{STAGE_PREFIX}/openapijson", include_in_schema=False)
async def openapijson():
    return app.openapi()


@app.get(f"/{STAGE_PREFIX}/health_check", dependencies=[Depends(get_token)])
def health_check():
    """
    Request this to check on the server health.
    """
    return "Healthy"


app.include_router(
    cliente_router.router, prefix=f"/{STAGE_PREFIX}", dependencies=[Depends(get_token)]
)
app.include_router(
    produto_router.router, prefix=f"/{STAGE_PREFIX}", dependencies=[Depends(get_token)]
)
app.include_router(
    pedido_router.router, prefix=f"/{STAGE_PREFIX}", dependencies=[Depends(get_token)]
)
app.include_router(
    payment_router.router, prefix=f"/{STAGE_PREFIX}", dependencies=[Depends(get_token)]
)
app.include_router(
    queue_router.router, prefix=f"/{STAGE_PREFIX}", dependencies=[Depends(get_token)]
)
app.include_router(
    maintenance_router.router,
    prefix=f"/{STAGE_PREFIX}",
    dependencies=[Depends(get_token)],
)
app.include_router(
    web_hook_example_router.router,
    prefix=f"/{STAGE_PREFIX}",
    dependencies=[Depends(get_token)],
)

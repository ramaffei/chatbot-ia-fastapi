import logging

from api.external_api import api_router as api_router_external
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_exceptionshandler import APIExceptionHandler, APIExceptionMiddleware
from fastapi_versioning import VersionedFastAPI
from pydantic import ValidationError
from settings.project_settings import project_settings
from starlette.middleware.cors import CORSMiddleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

app_original = FastAPI(
    title="MSCampaign",
    description="MSCampaign Microservice",
    root_path=project_settings.RootPath,
)

# ==== Include external routes
app_original.include_router(api_router_external)

# ==== Version
app = VersionedFastAPI(app_original, root_path=project_settings.RootPath)


# ==== Logging
logger = logging.getLogger("app")
logger.addHandler(logging.StreamHandler())

# ==== Middlewares
app.add_middleware(
    APIExceptionMiddleware,
    capture_unhandled=True,
    log_error=True,
    logger_name="app.exceptions",
)
app.add_middleware(RawContextMiddleware, plugins=(plugins.RequestIdPlugin(),))
app.add_middleware(
    CORSMiddleware,
    allow_origins=project_settings.CORSOrigins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==== Exception handlers
if not project_settings.DEBUG:
    logger.setLevel(logging.INFO)
    app.add_exception_handler(RequestValidationError, APIExceptionHandler.unhandled)
    app.add_exception_handler(ValidationError, APIExceptionHandler.unhandled)
else:
    logger.setLevel(logging.DEBUG)

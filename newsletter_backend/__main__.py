import uvicorn

from .config import AppEnv, AppSettings

uvicorn.run(
    "newsletter_backend.app:app",
    port=int(AppSettings.port),
    host="0.0.0.0",
    server_header=False,
    reload=(AppSettings.env == AppEnv.dev),
)

import uvicorn

from newsletter_backend.config import AppEnv, app_config


uvicorn.run(
    "newsletter_backend.app:app",
    port=int(app_config.port),
    host="0.0.0.0",
    server_header=False,
    reload=(app_config.env == AppEnv.dev),
)

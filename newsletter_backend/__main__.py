import os
import uvicorn

PORT = os.environ.get("PORT", "8000")
RELOAD = os.environ.get("DEV", "false")

uvicorn.run(
    "newsletter_backend.app:app",
    port=int(PORT),
    host="0.0.0.0",
    server_header=False,
    reload=(RELOAD == "true"),
)

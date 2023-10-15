from fastapi import FastAPI

from newsletter_backend.routes import auth_route

app = FastAPI()

app.include_router(auth_route.router, prefix="/auth", tags=["auth"])


@app.get("/")
async def health_check():
    return {"status": "online"}

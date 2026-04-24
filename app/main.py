from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .db import init_db
from .router import router

app = FastAPI(title="Herd Manager", version="1.0.0")
init_db()

# Static assets (UI)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory="data/uploads"), name="uploads")

@app.get("/")
def index():
    return FileResponse("app/static/index.html")

# API routes
app.include_router(router)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware

from app.db.session import engine
from app.db.models import Base

from app.core.config import settings

from app.routers.auth import router as auth_router
from app.routers.drive import router as drive_router
from app.routers.summary import router as summary_router
from app.routers.export import router as export_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# templates = Jinja2Templates(
#     directory="app/templates"
# )

app.include_router(auth_router)
app.include_router(drive_router)
app.include_router(summary_router)
app.include_router(export_router)


@app.get("/")
async def home():
    return {"message": "DriveDigest Running"}
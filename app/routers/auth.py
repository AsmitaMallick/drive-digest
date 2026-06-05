from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.core.config import settings

router = APIRouter()

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile https://www.googleapis.com/auth/drive.readonly"
    }
)


@router.get("/login")
async def login(request: Request):

    redirect_uri = settings.GOOGLE_REDIRECT_URI

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
        prompt="consent"
    )


@router.get("/auth/callback")
async def auth_callback(request: Request):

    token = await oauth.google.authorize_access_token(request)

    user_info = token["userinfo"]

    request.session["user"] = dict(user_info)

    token_min = {
        "access_token": token.get("access_token"),
        "refresh_token": token.get("refresh_token"),
        "expires_at": token.get("expires_at"),
        "token_type": token.get("token_type"),
        "scope": token.get("scope")
    }

    request.session["token"] = token_min

    return RedirectResponse(url="/documents")


@router.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse("/")
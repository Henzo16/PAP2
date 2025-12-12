from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from auth.jwt import decode_access_token
from crud.user import get_user_by_email
from database import SessionLocal

PUBLIC_PATHS = [
    "/api/auth/login",
    "/api/auth/register",
    "/docs",
    "/redoc",
    "/openapi.json"
]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        path = request.url.path

        # Rotas públicas → não exigem token
        if any(path.startswith(pub) for pub in PUBLIC_PATHS):
            return await call_next(request)

        # Buscar token
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token ausente")

        token = auth_header.split(" ")[1]

        payload = decode_access_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")

        email = payload.get("sub")

        db = SessionLocal()
        user = get_user_by_email(db, email)
        db.close()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        request.state.user = user

        return await call_next(request)

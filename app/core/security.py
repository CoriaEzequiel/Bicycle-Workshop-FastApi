from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from app.core.config import settings
from app.utils.jwks_cache import JWKSCache
import json
import base64

bearer_scheme = HTTPBearer(auto_error=False)

# Cache de JWKS para validar JWTs
jwks_cache = JWKSCache(
    url=f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json",
    ttl_seconds=settings.JWKS_CACHE_TTL_SECONDS
)


async def _get_signing_key(kid: str) -> dict[str, Any]:
    jwks = await jwks_cache.get()
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    raise HTTPException(status_code=401, detail="Signing key not found")


async def validate_jwt(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]
) -> dict[str, Any]:
    if creds is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = creds.credentials

    # Leer header para obtener kid sin validar primero
    try:
        header_segment = token.split(".")[0]
        # padding adecuado para base64
        padding = "=" * (-len(header_segment) % 4)
        header_data = json.loads(base64.urlsafe_b64decode(header_segment + padding).decode())
        kid = header_data.get("kid")
    except Exception:  # noqa
        raise HTTPException(status_code=401, detail="Invalid token header")

    key = await _get_signing_key(kid)

    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=[settings.AUTH0_ALGORITHMS],
            audience=settings.AUTH0_AUDIENCE,
            issuer=settings.AUTH0_ISSUER,
            options={"verify_at_hash": False},  # FastAPI + Auth0
        )
        return payload  # dict con claims (sub, roles, permissions, etc.)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token invalid: {str(e)}")



# Helpers de autorización


def require_roles(*roles: str):
    """
    Decorador para endpoints que requieren ciertos roles.
    Ejemplo de uso:
    @app.get("/admin-only")
    async def admin_route(user=Depends(require_roles("admin", "super_admin"))):
        ...
    """
    async def wrapper(payload: dict[str, Any] = Depends(validate_jwt)) -> dict[str, Any]:
        user_roles = payload.get(settings.AUTH0_ROLES_CLAIM, [])
        if not any(role in user_roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges"
            )
        return payload

    return wrapper


def require_permissions(*perms: str):
    """
    Decorador para endpoints que requieren ciertos permisos.
    Ejemplo:
    @app.post("/products")
    async def create_product(user=Depends(require_permissions("products:create"))):
        ...
    """
    async def wrapper(payload: dict[str, Any] = Depends(validate_jwt)) -> dict[str, Any]:
        user_perms = payload.get(settings.AUTH0_PERMS_CLAIM, [])
        if not all(p in user_perms for p in perms):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return payload

    return wrapper

import jwt
from jwt import PyJWKClient

from app.core.config import settings


jwks_client = PyJWKClient(settings.supabase_jwks_url)


def verify_jwt(token: str):
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["ES256"],
        audience="authenticated",
        issuer=f"{settings.supabase_url}/auth/v1",
    )

    return payload

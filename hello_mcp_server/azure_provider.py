import time
import httpx
from jose import jwt
from mcp.server.auth.provider import OAuthAuthorizationServerProvider, AccessToken


class AzureResourceProvider(OAuthAuthorizationServerProvider):
    def __init__(self, issuer: str, audience: str):
        self.issuer = issuer
        self.audience = audience
        self._jwks_url = None          # filled lazily from metadata
        self._jwks_cache: dict | None = None
        self._jwks_expires = 0         # <-- use the same name everywhere

    async def _get_jwks(self) -> dict:
        if not self._jwks_cache or time.time() > self._jwks_expires:
            async with httpx.AsyncClient() as c:
                if self._jwks_url is None:
                    meta = (
                        await c.get(f"{self.issuer}/.well-known/openid-configuration")
                    ).json()
                    self._jwks_url = meta["jwks_uri"]

                self._jwks_cache = (await c.get(self._jwks_url)).json()
            self._jwks_expires = time.time() + 3600
        return self._jwks_cache

    async def load_access_token(self, token: str) -> AccessToken | None:
        keys = await self._get_jwks()
        header = jwt.get_unverified_header(token)
        kid = header["kid"]
        alg = header["alg"]          # e.g. RS256
        key = next(k for k in keys["keys"] if k["kid"] == kid)

        claims = jwt.decode(
            token,
            key,
            algorithms=[alg],
            audience=self.audience,
            issuer=self.issuer,
        )

        return AccessToken(
            token=token,
            client_id=claims.get("appid") or claims.get("azp"),
            scopes=claims.get("scp", "").split(),
            expires_at=int(claims["exp"]),
        )

    # The rest stay un-implemented for resource-server mode

    async def authorize(self, *_): raise NotImplementedError
    async def exchange_authorization_code(self, *_): ...
    async def load_authorization_code(self, *_):     ...
    async def load_refresh_token(self, *_):          ...
    async def exchange_refresh_token(self, *_):      ...
    async def revoke_token(self, *_): return None

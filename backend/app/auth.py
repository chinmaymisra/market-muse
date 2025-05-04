from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ALGORITHMS = ["RS256"]

if not AUTH0_DOMAIN or not API_AUDIENCE:
    raise RuntimeError("AUTH0_DOMAIN or API_AUDIENCE not set in environment")

http_bearer = HTTPBearer()

def get_jwks():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    try:
        return requests.get(jwks_url).json()
    except Exception as e:
        print(f"[Auth0] Failed to fetch JWKS: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch Auth0 keys")

def verify_token(token: str):
    jwks = get_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError as e:
        print(f"[Auth0] Invalid JWT header: {e}")
        raise HTTPException(status_code=401, detail="Invalid token header")

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header.get("kid"):
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }

    if not rsa_key:
        print("[Auth0] No matching key found in JWKS")
        raise HTTPException(status_code=401, detail="Token key not found")

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        print("Decoded token payload:", payload)  # optional debug
        return {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "picture": payload.get("picture")
        }

    except JWTError as e:
        print(f"[Auth0] Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Token verification failed")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    return verify_token(credentials.credentials)

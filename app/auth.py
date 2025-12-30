import os
from fastapi import Header, HTTPException

INGEST_TOKEN = os.getenv("INGEST_TOKEN")
CLIENT_TOKEN = os.getenv("CLIENT_TOKEN")

def require_ingest_token(x_token: str = Header(...)):
    if x_token != INGEST_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid ingest token")

def require_client_token(x_token: str = Header(...)):
    if x_token != CLIENT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid client token")

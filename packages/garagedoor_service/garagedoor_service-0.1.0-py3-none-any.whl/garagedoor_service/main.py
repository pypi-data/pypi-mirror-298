#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Any
import garagedoor_service.door_controller as door_controller
import garagedoor_service.tools.api_key as api_key_tools
import garagedoor_service.tools.config as config
import uvicorn

app = FastAPI()

api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify the API key.
    
    Parameters:
        api_key (str): The API key.
        
    Returns:
        str: The API key.
        
    Raises:
        HTTPException: If the API key is invalid.
    """
    if not api_key_tools.verify(api_key):
        raise HTTPException(status_code=403, detail="Unauthorized")
    return api_key


@app.post("/toggle")
def toggle_door(api_key: str = Security(verify_api_key)) -> Any:
    try:
        door_controller.request_door_toggle()
    except Exception as e:
        return {"result": "nok", "message": str(e)}
    return {"result": "ok"}


@app.get("/state")
def get_status(api_key: str = Security(verify_api_key)) -> Any:
    try:
        state = door_controller.get_door_state()
    except Exception as e:
        return {"result": "nok", "message": str(e)}
    return {"result": "ok", "state": state}


@app.get("/readyz")
def readyz() -> Any:
    return {"result": "ok"}


@app.get("/healthz")
def healthz() -> Any:
    return {"result": "ok"}


def main():
    host = config.get_bind_host()
    port = config.get_bind_port()
    uvicorn.run("garagedoor_service.main:app", host=host, port=port, reload=False)
    

if __name__ == "__main__":
    main()
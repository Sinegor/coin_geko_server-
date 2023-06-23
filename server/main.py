from fastapi import FastAPI, Depends
from typing import Union
from starlette.responses import JSONResponse
from pydantic import BaseModel

# Модуль для разрешения CORS-запросов
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from server.routes.crypto import c_router as Crypto_router

#from server.consts import http


app = FastAPI(title='server_gasket')

# Список того, что разрешено передавать и какими методами пользоваться:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = http.ELA_API_ORIGINS,
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"],
    
    
# )

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to this fantastic app!"}


app.include_router(Crypto_router)

if __name__ == "__main__":
    import logging
    import uvicorn
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('unicorn')
    logger.setLevel(logging.DEBUG)

    uvicorn.run(app, host ="127.0.0.1", port=8000)







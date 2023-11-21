from fastapi import FastAPI, Depends
from typing import Union
from starlette.responses import JSONResponse
from pydantic import BaseModel

# Модуль для разрешения CORS-запросов
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from remoute_server.routes.crypto import c_router as Crypto_router



#from server.consts import http


app = FastAPI(title='server_gasket')


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
    

    uvicorn.run(app, host ="94.142.136.139", port=80)
    #uvicorn.run(app, host ="127.0.0.1", port=8000)






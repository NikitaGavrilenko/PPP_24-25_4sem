from fastapi import FastAPI
from app.api.v1 import auth, crypto
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(crypto.router, tags=["Crypto"])
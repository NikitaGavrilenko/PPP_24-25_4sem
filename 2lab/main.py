from fastapi import FastAPI
from app.api.encoding import router as encoding_router
from app.api.users import router as users_router

app = FastAPI()

app.include_router(encoding_router, prefix='/encoding')
app.include_router(users_router, prefix='/users')
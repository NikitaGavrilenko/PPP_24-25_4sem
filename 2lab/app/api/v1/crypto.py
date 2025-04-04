from fastapi import APIRouter
from app.schemas.crypto import EncodeRequest, EncodeResponse, DecodeRequest, DecodeResponse
from app.services.crypto_service import encode_text, decode_text

router = APIRouter()

@router.post("/encode", response_model=EncodeResponse)
def encode(req: EncodeRequest):
    return encode_text(req)

@router.post("/decode", response_model=DecodeResponse)
def decode(req: DecodeRequest):
    return decode_text(req)
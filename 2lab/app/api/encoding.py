from fastapi import APIRouter
from pydantic import BaseModel
import base64

router = APIRouter()

class EncodeRequest(BaseModel):
    text: str
    key: str

class EncodeResponse(BaseModel):
    encoded_data: str
    key: str
    huffman_codes: dict
    padding: int

class DecodeRequest(BaseModel):
    encoded_data: str
    key: str
    huffman_codes: dict
    padding: int

class DecodeResponse(BaseModel):
    decoded_text: str
@router.post("/encode", response_model=EncodeResponse)
def encode(request: EncodeRequest):
    encoded_data = base64.b64encode(request.text.encode()).decode()
    return {
        "encoded_data": encoded_data,
        "key": request.key,
        "huffman_codes": {"H": "00", "e": "01"},
        "padding": 3
    }

@router.post("/decode", response_model=DecodeResponse)
def decode(request: DecodeRequest):
    decoded_text = base64.b64decode(request.encoded_data).decode()
    return {"decoded_text": decoded_text}
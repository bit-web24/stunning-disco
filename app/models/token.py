from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str # _id
    exp: int
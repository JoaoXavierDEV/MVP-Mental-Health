from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """Define como uma mensagem de erro sera representada."""
    message: str

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "username": "johndoe",
                "first_name": "john",
                "last_name": "doe",
                "password": "mypassword",
                "role": "admin",
                "phone_number": "00000000",
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str

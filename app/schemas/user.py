from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    """
    Payload for user registration.
    Password schould meet minimum complexity
    """
    username: constr(strip_whitespace=True)
    password: constr(min_length=8)

    class Config:
        str_strip_whitespace = True

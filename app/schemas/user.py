from pydantic import BaseModel, constr, ConfigDict


class UserCreate(BaseModel):
    """
    Payload for user registration.
    Password schould meet minimum complexity
    """
    username: constr(strip_whitespace=True)
    password: constr(min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True)

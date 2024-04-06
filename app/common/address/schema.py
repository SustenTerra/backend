from typing import Optional
from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    street: str = Field(
        json_schema_extra={
            "title": "Street",
            "description": "User's street name",
            "examples": ["Acacia Street"],
        },
    )
    number: str = Field(
        description="Number of the place where the user lives",
    )
    neighborhood: str = Field(
        json_schema_extra={
            "title": "Neighborhood",
            "description": "Neighborhood where the user lives",
            "examples": ["University District"],
        },
    )
    complement: str = Field(
        json_schema_extra={
            "title": "Complement",
            "description": "Additional information about the user's address",
            "examples": ["apartment 504"],
        },
    )
    city: str = Field(
        json_schema_extra={
            "title": "City",
            "description": "City where the user lives",
            "examples": ["Campina Grande"],
        },
    )
    state: str = Field(
        json_schema_extra={
            "title": "State",
            "description": "State where the user lives",
            "examples": ["Paraíba"],
        },
    )
    cep: str = Field(
        pattern=r"^[0-9]{8,15}$",
        json_schema_extra={
            "title": "Cep",
            "description": "User postal address",
            "examples": ["58429-170"],
        },
    )


class AddressCreate(AddressBase):
    user_id: int


class AddressCreateWithoutUserId(AddressBase):
    pass


class AddressView(AddressBase):
    id: int


class AddressUpdate(BaseModel):
    street: Optional[str] = Field(default=None, description="User's street name")
    number: Optional[str] = Field(
        default=None, description="Number of the place where the user lives"
    )
    complement: Optional[str] = Field(
        default=None,
        description="Additional information about the user's address",
    )
    neighborhood: Optional[str] = Field(default=None, description="Neighborhood")
    city: Optional[str] = Field(default=None, description="City where the user lives")
    state: Optional[str] = Field(default=None, description="State where the user lives")
    cep: Optional[str] = Field(
        default=None,
        description="User's postal address",
        pattern=r"^[0-9]{8,15}$",
    )

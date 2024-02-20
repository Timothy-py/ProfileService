

from datetime import date
from enum import Enum
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field


class WalletUpdate(BaseModel):
   amount: int
   auth_id: str


class PayoutDetail(BaseModel):
    rider_auth_id: str
    amount: int
    narration: str
    # errands_successful: bool


class ProfileCreate(BaseModel):
    auth_id: str
    full_name: str
    email: EmailStr
    phone_number: str
    email_verified: bool
    phone_number_verified: bool
    role: str
    country: str


class ProfileStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'
    away = 'away'


class ProfileUpdateStatus(BaseModel):
    status: ProfileStatus


class ProfileUpdate(BaseModel):
    language: Optional[str] = Field(None, description="User's preferred language.")
    gender: Optional[str] = Field(None, description="User's gender.")
    date_of_birth: Optional[date] = Field(None, description="User's date of birth.")
    # >>>>>>>>>>>>>>TODO: Request for the actual status values to use.>>>>>>>>>>>>>>>>>>>>
    status: Optional[ProfileStatus] = Field(None, description="User's status")
    country: Optional[str] = Field(None, description="User's country of residence.")
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    city: Optional[str] = Field(None, description="Rider's city of operation.")

    class Config:
        # Exclude fields that shouldn't be updated, like auth_id, id, or roles
        exclude = {"auth_id", "id", "role"}
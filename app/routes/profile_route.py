from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.services.profile_service import ProfileService
from app.services.address_service import AddressService
from ..core.database import get_db
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileUpdateStatus, WalletUpdate, PayoutDetail
from app.schemas.address import Address, AddressCreate
from app.core.authenticate import get_current_user
from app.services.card_service import CardService
from app.schemas.card import CardCreate
from app.serializer.card_serializer import card_serializer

profile_router = APIRouter(prefix='/api/v1/profile')


# CREATE A Profile
# TODO: This is API should not be exposed. It should be automatically triggered after
# a successful user email verification on the Authentication service.
@profile_router.post('/', status_code=status.HTTP_201_CREATED, tags=['Profiles'])
async def create_profile(profile: ProfileCreate, request: Request, db: Session = Depends(get_db)):
    print("Automatic profile creation triggered")
    print(request)
    return ProfileService.create_profile(profile, db)


# UPDATE A Profile
@profile_router.put('/', status_code=status.HTTP_200_OK, tags=['Profiles'])
async def update_profile(profile: ProfileUpdate, auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return ProfileService.update_profile(auth_id, profile, db)


# UPDATE PROFILE STATUS
@profile_router.patch('/status', status_code=status.HTTP_200_OK, tags=['Profiles'])
async def update_profile_status(status: ProfileUpdateStatus, auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return ProfileService.update_profile_status(auth_id, status, db)


# Get My Profile
@profile_router.get('/', status_code=status.HTTP_200_OK, tags=['Profiles'], description="Get the current logged in user profile")
async def get_my_profile(auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return ProfileService.get_profile(auth_id, db)


# GET A Profile
@profile_router.get('/{auth_id}', status_code=status.HTTP_200_OK, tags=['Profiles'])
async def get_a_profile(auth_id: Annotated[str, Path(description="The auth_id of the profile to retrieve")], db: Session = Depends(get_db)):
    return ProfileService.get_profile(auth_id, db)


# >>>>>>>>>>>>>>>>>ADDRESS ROUTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@profile_router.post('/address', status_code=status.HTTP_201_CREATED, tags=['Addresss'])
async def add_address(address: AddressCreate, auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return AddressService.add_address(auth_id, address, db)


# GET MY ADDRESSS
@profile_router.get('/address', status_code=status.HTTP_200_OK, response_model=list[Address], tags=['Addresss'])
async def get_my_addresss(auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return AddressService.get_my_addresss(auth_id, db)


# GET A ADDRESS
@profile_router.get('/address/{address_id}', status_code=status.HTTP_200_OK, response_model=Address, tags=['Addresss'])
async def get_address(auth_id: Annotated[str, Depends(get_current_user)], address_id: Annotated[str, Path(description="The ID of the address to retrieve")], db: Session = Depends(get_db)):
    return AddressService.get_address(auth_id, address_id, db)


# REMOVE An ADDRESS
@profile_router.delete('/address/{address_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Addresss'])
async def remove_address(auth_id: Annotated[str, Depends(get_current_user)], address_id: Annotated[str, Path(description="The ID of the address to delete")], db: Session = Depends(get_db)):
    return AddressService.remove_address(auth_id, address_id, db)


# >>>>>>>>>>>>>>>>>Card ROUTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Store A Card for Profile
# TODO: This is API should not be exposed. It should be automatically triggered by an event after
# a successful payment verification process from the Payment service.
@profile_router.post('/card', status_code=status.HTTP_201_CREATED, tags=['Card'])
async def add_card(card: CardCreate, auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return CardService.add_card(auth_id, card, db)


# GET MY CARDS
@profile_router.get('/card', status_code=status.HTTP_200_OK, tags=['Card'])
async def get_card(auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return CardService.get_my_cards(auth_id, db)


# REMOVE A CARD
@profile_router.delete('/card/{card_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Card'])
async def remove_card(auth_id: Annotated[str, Depends(get_current_user)], card_id: Annotated[str, Path(description="The ID of the card to delete")], db: Session = Depends(get_db)):
    return CardService.remove_card(auth_id, card_id, db)


# >>>>>>>>>>>>>>>>>Wallet Update ROUTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Update the profile balance after successfull payment
# TODO: This is API should not be exposed. It should be automatically triggered after
# a successful payment from the Payment service.
@profile_router.post('/credit_wallet', status_code=status.HTTP_200_OK, tags=['Profiles'], description="Increase a user balance")
async def credit_profile_wallet(wallet: WalletUpdate, db: Session = Depends(get_db)):
    return ProfileService.credit_profile_wallet(wallet, db)


# >>>>>>>>>>>>>>>>>Wallet Update ROUTES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Update the profile balance after successfull payment
# TODO: This is API should not be exposed. It should be automatically triggered by an event after
# a successful payment from the Payment service.
@profile_router.post('/debit_wallet', status_code=status.HTTP_200_OK, tags=['Profiles'], description="Decrease a user balance")
async def debit_profile_wallet(wallet: WalletUpdate,  db: Session = Depends(get_db)):
    return ProfileService.debit_profile_wallet(wallet, db)


@profile_router.post("/update_rider_wallet", status_code=status.HTTP_200_OK, tags=['Profiles'], description="Pay a rider after a successful errand")
def pay_rider(payout: PayoutDetail, auth_id: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    return ProfileService.pay_rider(payout, auth_id, db)

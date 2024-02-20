import json
from datetime import datetime

from fastapi import HTTPException
from fastapi.responses import JSONResponse
import sqlalchemy
from sqlalchemy.orm import joinedload

from app.schemas.profile import PayoutDetail


from ..models.profile import Profile


class ProfileService:
    def create_profile(profile, db):
        try:
            profile = Profile(
                auth_id=profile.auth_id,
                full_name=profile.full_name,
                email=profile.email,
                phone_number=profile.phone_number,
                email_verified=profile.email_verified,
                role=profile.role,
                balance=0,
                date_credited=None
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)

        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Profile already existed"
            )
        else:
            return profile

    def credit_profile_wallet(wallet, db):
        profile = db.query(Profile).filter(
            Profile.auth_id == wallet.auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        profile.balance += wallet.amount
        profile.date_credited = datetime.now()
        db.commit()
        db.refresh(profile)
        return profile

    def debit_profile_wallet(wallet, db):
        profile = db.query(Profile).filter(
            Profile.auth_id == wallet.auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        if profile.balance < wallet.amount:
            raise HTTPException(
                status_code=404, detail="Insufficient balance")

        profile.balance -= wallet.amount
        db.commit()
        db.refresh(profile)
        return profile

    def get_profile(auth_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).options(
            joinedload(Profile.addresses), joinedload(Profile.cards)).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        return profile

    def update_profile(auth_id, profile, db):
        data = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if data is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        for field, value in profile.dict(exclude_unset=True).items():
            setattr(data, field, value)

        db.commit()
        db.refresh(data)

        return {"message": "Profile updated successfully"}

    def update_profile_status(auth_id, status, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        profile.status = status.status
        # setattr(profile, 'status', status)
        db.commit()

        return {"message": "Profile status updated successfully"}
    
    def pay_rider(payout: PayoutDetail, auth_id, db):
        rider_profile = db.query(Profile).filter(Profile.auth_id == payout.rider_auth_id).first()
        customer_profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if rider_profile is None:
            raise HTTPException(status_code=404, detail="Rider profile not found")
        if customer_profile is None:
            raise HTTPException(status_code=404, detail="Customer profile not found")
        
        if customer_profile.balance < payout.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        

        # EMIT EVENT TO CREDIT A RIDER WITH THE AMOUNT
        # {
        #     "auth_id": rider_profile.auth_id,
        #     "amount": payout.amount,
        # }

        # EMIT EVENT TO DEBIT A CUSTOMER WITH THE AMOUNT
        # {
        #     "auth_id": customer_profile.auth_id,
        #     "amount": payout.amount,
        # }
        return True


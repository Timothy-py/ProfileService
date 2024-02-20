import json
import sqlalchemy

from datetime import datetime
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from ..models.profile import Card, Profile
from app.core.config import env_vars


class CardService:
    def add_card(auth_id, card, db):

        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        card = Card(first_6digits=card.first_6digits, last_4digits=card.last_4digits,
                    issuer=card.issuer, country=card.country, type=card.type, token=card.token,
                    expiry=card.expiry, profile_id=profile.id)
        
        db.add(card)
        db.commit()
        db.refresh()

        return card

    def get_my_cards(auth_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        cards = db.query(Card).filter(Card.profile_id == profile.id).all()

        return cards
    
    def remove_card(auth_id, card_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        card = db.query(Card).filter(Card.id == card_id,
                                       Card.profile_id == profile.id).first()

        if card is None:
            raise HTTPException(
                status_code=404, detail="Card not found for the specified profile")

        db.delete(card)
        db.commit()

        return {"message": "Card deleted successfully"}

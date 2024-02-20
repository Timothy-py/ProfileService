

def card_serializer(card, auth_id) -> dict:
    return {
        "card_number": str(card.card_number),
        "cvv": str(card.cvv),
        "expiry_month": str(card.expiry_month),
        "expiry_year": str(card.expiry_year),
        "auth_id": str(auth_id),
        "profile_id": str(card.profile_id),
        "date_stored": str(card.date_stored)
	}
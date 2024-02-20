

from fastapi import HTTPException


from app.models.profile import Address, Profile


class AddressService:
    def add_address(auth_id, address, db):
        # query profile data
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        address = Address(name=address.name, address=address.address,
                      profile_id=profile.id)

        db.add(address)
        db.commit()
        db.refresh(address)

        return address

    def remove_address(auth_id, address_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        address = db.query(Address).filter(Address.id == address_id,
                                       Address.profile_id == profile.id).first()

        if address is None:
            raise HTTPException(
                status_code=404, detail="Address not found for the specified profile")

        db.delete(address)
        db.commit()

        return {"message": "Address deleted successfully"}

    def get_my_addresss(auth_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        addresss = db.query(Address).filter(Address.profile_id == profile.id).all()

        return addresss

    def get_address(auth_id, address_id, db):
        profile = db.query(Profile).filter(Profile.auth_id == auth_id).first()

        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")

        address = db.query(Address).filter(Address.id == address_id).first()

        if address is None:
            raise HTTPException(
                status_code=404, detail="Address not found for the specified profile")

        return address

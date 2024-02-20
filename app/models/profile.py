from uuid import uuid4


from sqlalchemy import UUID, Boolean, Column, Date, Enum, ForeignKey, String, Integer
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Session


from ..core.database import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                nullable=False, unique=True, index=True)
    auth_id = Column(String, nullable=False, index=True, unique=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone_number = Column(String, default=False)
    email_verified = Column(Boolean, default=False)
    phone_number_verified = Column(Boolean, default=False)
    role = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    language = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    status = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    balance = Column(Integer, default=0)
    date_credited = Column(Date, nullable=True)
    # Establishing a one-to-many relationship with the Address table
    addresses = relationship("Address", back_populates='profile')
    # Establishing a one-to-many relationship with the Card table
    cards = relationship("Card", back_populates="profile")


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Foreign key relationship with the Profile table
    profile_id = Column(UUID(as_uuid=True), ForeignKey(
        "profiles.id"), nullable=False)

    # Establishing the relationship from the Address side
    profile = relationship(Profile, back_populates='addresses')
    # profile = relationship(Profile, back_populates='addresses', cascade="all, delete-orphan", single_parent=True)


class Card(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                nullable=False, unique=True, index=True)
    profile_id = Column(UUID(as_uuid=True), ForeignKey(
        "profiles.id"), nullable=False)
    first_6digits = Column(String, nullable=False)
    last_4digits = Column(String, nullable=False)
    issuer = Column(String, nullable=False)
    country = Column(String, nullable=False)
    token = Column(String, nullable=False)
    expiry = Column(String, nullable=False)

    # Establishing the relationship from the Card side
    profile = relationship(Profile, back_populates="cards")
    # profile = relationship(Profile, back_populates="cards", cascade="all, delete-orphan", single_parent=True)

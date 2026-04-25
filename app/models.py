# app/models.py
from datetime import date, datetime
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship


class Species(str, Enum):
    cow = "cow"
    goat = "goat"
    sheep = "sheep"
    horse = "horse"
    swine = "swine"
    chicken = "chicken"
    rabbit = "rabbit"


class TreatmentCategory(str, Enum):
    shot = "shot"
    medicine = "medicine"


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_info: Optional[str] = None


class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    species: Species
    name: str
    birthday: Optional[date] = None
    height_inches: Optional[float] = 0.0
    weight_lbs: Optional[float] = 0.0
    coloring: Optional[str] = None

    # self-referencing foreign keys
    sire_id: Optional[int] = Field(default=None, foreign_key="animal.id")
    dam_id: Optional[int] = Field(default=None, foreign_key="animal.id")

    sire_name: Optional[str] = None
    dam_name: Optional[str] = None
    photo_url: Optional[str] = None

    organization_id: Optional[int] = Field(
        default=None, foreign_key="organization.id"
    )

    # ❗ FIXED: disambiguate relationships (was causing AmbiguousForeignKeysError)
    sire: Optional["Animal"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": [sire_id],
            "remote_side": "Animal.id",
            "uselist": False,
        }
    )

    dam: Optional["Animal"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": [dam_id],
            "remote_side": "Animal.id",
            "uselist": False,
        }
    )

    treatments: list["Treatment"] = Relationship(back_populates="animal")
    documents: list["Document"] = Relationship(back_populates="animal")

    organization: Optional[Organization] = Relationship()


class Treatment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    date: date
    category: TreatmentCategory
    name: str
    dose: Optional[str] = None
    notes: Optional[str] = None

    animal: "Animal" = Relationship(back_populates="treatments")


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    organization_id: Optional[int] = Field(
        default=None, foreign_key="organization.id"
    )
    title: str
    file_url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = None

    animal: "Animal" = Relationship(back_populates="documents")
    organization: Optional[Organization] = Relationship()

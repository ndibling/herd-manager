from datetime import date, datetime
from typing import Optional, Literal
from sqlmodel import SQLModel, Field, Relationship

SpeciesLiteral = Literal["cow", "goat", "sheep", "horse", "swine", "chicken", "rabbit"]

class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_info: Optional[str] = None

class Animal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    species: SpeciesLiteral
    name: str
    birthday: Optional[date] = None
    height_inches: Optional[float] = 0.0
    weight_lbs: Optional[float] = 0.0
    coloring: Optional[str] = None

    # Parent references (optional)
    sire_id: Optional[int] = Field(default=None, foreign_key="animal.id")
    dam_id: Optional[int] = Field(default=None, foreign_key="animal.id")

    # Parent names (free text to satisfy “parents names” requirement)
    sire_name: Optional[str] = None
    dam_name: Optional[str] = None

    photo_url: Optional[str] = None
    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")

    sire: Optional["Animal"] = Relationship(sa_relationship_kwargs={"remote_side": "Animal.id"})
    dam: Optional["Animal"] = Relationship(sa_relationship_kwargs={"remote_side": "Animal.id"})
    treatments: list["Treatment"] = Relationship(back_populates="animal")
    documents: list["Document"] = Relationship(back_populates="animal")
    organization: Optional[Organization] = Relationship()

class Treatment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    date: date
    category: Literal["shot", "medicine"]
    name: str
    dose: Optional[str] = None
    notes: Optional[str] = None

    animal: Animal = Relationship(back_populates="treatments")

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animal_id: int = Field(foreign_key="animal.id")
    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    title: str
    file_url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = None

    animal: Animal = Relationship(back_populates="documents")
    organization: Optional[Organization] = Relationship()

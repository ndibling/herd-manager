# app/router.py (only showing changed params)

from enum import Enum
from .models import Animal, Treatment, Organization, Document, Species, TreatmentCategory

@router.post("/api/animals")
def create_animal(
    species: Species = Form(...),  # <- Enum
    name: str = Form(...),
    birthday: Optional[date] = Form(None),
    height_inches: Optional[float] = Form(None),
    weight_lbs: Optional[float] = Form(None),
    coloring: Optional[str] = Form(None),
    sire_id: Optional[int] = Form(None),
    dam_id: Optional[int] = Form(None),
    sire_name: Optional[str] = Form(None),
    dam_name: Optional[str] = Form(None),
    organization_id: Optional[int] = Form(None),
    photo: Optional[UploadFile] = File(None),
):
    # photo handling unchanged...
    a = Animal(
        species=species, name=name, birthday=birthday,
        height_inches=height_inches or 0.0, weight_lbs=weight_lbs or 0.0,
        coloring=coloring, sire_id=sire_id, dam_id=dam_id,
        sire_name=sire_name, dam_name=dam_name,
        photo_url=photo_url, organization_id=organization_id
    )
    # save unchanged...

@router.post("/api/animals/{animal_id}/treatments")
def add_treatment(
    animal_id: int,
    date: date = Form(...),
    category: TreatmentCategory = Form(...),  # <- Enum
    name: str = Form(...),
    dose: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
):
    # unchanged...

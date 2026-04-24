import os
from datetime import date
from typing import Optional, Literal
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from .db import engine
from .models import Animal, Treatment, Organization, Document
from .utils import compute_age, build_pedigree

router = APIRouter()

# Seed organization if missing
@router.on_event("startup")
def seed_org():
    with Session(engine) as s:
        exists = s.exec(select(Organization).where(Organization.name == "Mini Zebu of America")).first()
        if not exists:
            s.add(Organization(name="Mini Zebu of America"))
            s.commit()

# Animals
@router.get("/api/animals")
def list_animals():
    with Session(engine) as s:
        animals = s.exec(select(Animal)).all()
        return [
            {
                **a.model_dump(),
                "age": compute_age(a.birthday),
                "organization_name": a.organization.name if a.organization else None
            }
            for a in animals
        ]

@router.post("/api/animals")
def create_animal(
    species: Literal["cow","goat","sheep","horse","swine","chicken","rabbit"] = Form(...),
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
    photo_url = None
    if photo:
        if not photo.filename.lower().endswith((".png",".jpg",".jpeg",".webp",".gif")):
            raise HTTPException(status_code=400, detail="Unsupported image type")
        path = f"data/uploads/photos/{name.strip().replace(' ','_')}_{photo.filename}"
        with open(path, "wb") as f:
            f.write(photo.file.read())
        photo_url = path
    a = Animal(
        species=species, name=name, birthday=birthday,
        height_inches=height_inches or 0.0, weight_lbs=weight_lbs or 0.0,
        coloring=coloring, sire_id=sire_id, dam_id=dam_id,
        sire_name=sire_name, dam_name=dam_name,
        photo_url=photo_url, organization_id=organization_id
    )
    with Session(engine) as s:
        s.add(a); s.commit(); s.refresh(a)
        return {"id": a.id}

@router.get("/uploads/photos/{filename}")
def get_photo(filename: str):
    path = os.path.join("data/uploads/photos", filename)
    if not os.path.exists(path): raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(path)

# Treatments (shots & medicines)
@router.get("/api/animals/{animal_id}/treatments")
def list_treatments(animal_id: int):
    with Session(engine) as s:
        ts = s.exec(select(Treatment).where(Treatment.animal_id == animal_id)).all()
        return [t.model_dump() for t in ts]

@router.post("/api/animals/{animal_id}/treatments")
def add_treatment(
    animal_id: int,
    date: date = Form(...),
    category: Literal["shot","medicine"] = Form(...),
    name: str = Form(...),
    dose: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
):
    with Session(engine) as s:
        if not s.get(Animal, animal_id):
            raise HTTPException(status_code=404, detail="Animal not found")
        t = Treatment(animal_id=animal_id, date=date, category=category, name=name, dose=dose, notes=notes)
        s.add(t); s.commit(); s.refresh(t)
        return {"id": t.id}

# Pedigree
@router.get("/api/animals/{animal_id}/pedigree")
def get_pedigree(animal_id: int, generations: int = 4):
    with Session(engine) as s:
        return build_pedigree(s, animal_id, generations=generations)

# Documents
@router.get("/api/animals/{animal_id}/documents")
def list_docs(animal_id: int):
    with Session(engine) as s:
        ds = s.exec(select(Document).where(Document.animal_id == animal_id)).all()
        return [d.model_dump() for d in ds]

@router.post("/api/animals/{animal_id}/documents")
def upload_doc(
    animal_id: int,
    title: str = Form(...),
    organization_id: Optional[int] = Form(None),
    note: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith((".pdf",".png",".jpg",".jpeg",".webp",".gif")):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    path = f"data/uploads/docs/{animal_id}_{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    with Session(engine) as s:
        if not s.get(Animal, animal_id):
            raise HTTPException(status_code=404, detail="Animal not found")
        d = Document(animal_id=animal_id, organization_id=organization_id, title=title, file_url=path, note=note)
        s.add(d); s.commit(); s.refresh(d)
        return {"id": d.id}

# Organizations
@router.get("/api/organizations")
def list_orgs():
    with Session(engine) as s:
        orgs = s.exec(select(Organization)).all()
        return [o.model_dump() for o in orgs]

@router.post("/api/organizations")
def add_org(name: str = Form(...), contact_info: Optional[str] = Form(None)):
    with Session(engine) as s:
        o = Organization(name=name, contact_info=contact_info)
        s.add(o); s.commit(); s.refresh(o)
        return {"id": o.id}

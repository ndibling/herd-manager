from datetime import date
from typing import Optional, Dict, Any, List
from sqlmodel import Session, select
from .models import Animal

def compute_age(birthday: Optional[date]) -> Optional[int]:
    if not birthday:
        return None
 date.today()
    years = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    return max(years, 0)

def build_pedigree(session: Session, animal_id: int, generations: int = 4) -> Dict[str, Any]:
    """Return a nested pedigree up to N generations {animal, sire, dam, ...}."""
    a = session.get(Animal, animal_id)
    if not a:
        return {}
    def node(x: Animal, depth: int) -> Dict[str, Any]:
        if not x or depth == 0: 
            return {}
        data = {
            "id": x.id, "name": x.name, "species": x.species,
            "sire_name": x.sire_name, "dam_name": x.dam_name,
            "photo_url": x.photo_url,
        }
        sire = session.get(Animal, x.sire_id) if x.sire_id else None
        dam  = session.get(Animal, x.dam_id)  if x.dam_id  else None
        data["sire"] = node(sire, depth-1) if sire else {"name": x.sire_name} if x.sire_name else {}
        data["dam"]  = node(dam,  depth-1) if dam  else {"name": x.dam_name} if x.dam_name else {}
        return data
    return node(a, generations)

from datetime import date
from typing import Optional, Dict, Any
from sqlmodel import Session
from .models import Animal


def compute_age(birthday: Optional[date]) -> Optional"""Return age in years based on a birthday."""
    if not birthday:
        return None

    today = date.today()
    years = today.year - birthday.year - (
        (today.month, today.day) < (birthday.month, birthday.day)
    )
    return max(years, 0)


def build_pedigree(
    session: Session, animal_id: int, generations: int = 4
) -> Dict[str, Any]:
    """Return a nested pedigree dictionary up to N generations."""

    animal = session.get(Animal, animal_id)
    if not animal:
        return {}

    def node(a: Optional[Animal], depth: int) -> Dict[str, Any]:
        if not a or depth == 0:
            return {}

        result = {
            "id": a.id,
            "name": a.name,
            "species": a.species.value,
            "photo_url": a.photo_url,
            "sire_name": a.sire_name,
            "dam_name": a.dam_name,
        }

        # Recurse into parents
        sire = session.get(Animal, a.sire_id) if a.sire_id else None
        dam = session.get(Animal, a.dam_id) if a.dam_id else None

        result["sire"] = (
            node(sire, depth - 1)
            if sire
            else ({"name": a.sire_name} if a.sire_name else {})
        )
        result["dam"] = (
            node(dam, depth - 1)
            if dam
            else ({"name": a.dam_name} if a.dam_name else {})
        )

        return result

    return node(animal, generations)

from datetime import date
from typing import Optional, Dict, Any
from sqlmodel import Session
from .models import Animal


def compute_age(birthday: Optional[date]) -> Optional"""Return age in years based on a birthday.

    If `birthday` is None, returns None.
    """
    if birthday is None:
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
    if animal is None:
        return {}

    def node(a: Optional[Animal], depth: int) -> Dict[str, Any]:
        if a is None or depth == 0:
            return {}

        result: Dict[str, Any] = {
            "id": a.id,
            "name": a.name,
            "species": a.species.value if hasattr(a.species, "value") else a.species,
            "photo_url": getattr(a, "photo_url", None),
            "sire_name": getattr(a, "sire_name", None),
            "dam_name": getattr(a, "dam_name", None),
        }

        sire = (
            session.get(Animal, getattr(a, "sire_id", None))
            if getattr(a, "sire_id", None)
            else None
        )
        dam = (
            session.get(Animal, getattr(a, "dam_id", None))
            if getattr(a, "dam_id", None)
            else None
        )

        result["sire"] = (
            node(sire, depth - 1)
            if sire
            else ({"name": getattr(a, "sire_name", None)} if getattr(a, "sire_name", None) else {})
        )
        result["dam"] = (
            node(dam, depth - 1)
            if dam
            else ({"name": getattr(a, "dam_name", None)} if getattr(a, "dam_name", None) else {})
        )

        return result

    return node(animal, generations)

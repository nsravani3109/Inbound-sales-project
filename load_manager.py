from db import SessionLocal, Load
from sqlalchemy import or_, and_

CITY_ALIASES = {
    "los angeles": ["los angeles", "la", "l.a."],
    "new york": ["new york", "nyc", "n.y."],
    "san francisco": ["san francisco", "sf", "s.f."],
    # add more cities as needed
}

class LoadManager:
    def __init__(self):
        self.db = SessionLocal()

    def normalize(self, text):
        return text.lower().strip()

    def expand_aliases(self, city):
        city_lower = self.normalize(city)
        return CITY_ALIASES.get(city_lower, [city_lower])

    def search_loads(self, **kwargs):
        """
        Search loads dynamically based on any provided fields.
        Example fields: origin, destination, equipment_type, weight, commodity_type, etc.
        """
        query = self.db.query(Load)
        filters = []

        for field, value in kwargs.items():
            if value is None:
                continue

            if field == "origin":
                origin_aliases = self.expand_aliases(value)
                filters.append(or_(*[Load.origin.ilike(f"%{alias}%") for alias in origin_aliases]))
            elif field == "destination":
                dest_aliases = self.expand_aliases(value)
                filters.append(or_(*[Load.destination.ilike(f"%{alias}%") for alias in dest_aliases]))
            elif field in ["equipment_type", "commodity_type", "notes", "dimensions"]:
                filters.append(getattr(Load, field).ilike(f"%{value}%"))
            else:
                filters.append(getattr(Load, field) == value)

        if filters:
            query = query.filter(and_(*filters))

        return [l.__dict__ for l in query.all()]
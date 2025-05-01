from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    distance_from_sun_mln_km: Mapped[int]
    amount_of_moons: Mapped[int]
    
    def to_dict(self):
        planet_as_dict = {}
        planet_as_dict["id"] = self.id
        planet_as_dict["name"] = self.name
        planet_as_dict["description"] = self.description
        planet_as_dict["distance_from_sun_mln_km"] = self.distance_from_sun_mln_km
        planet_as_dict["amount_of_moons"] = self.amount_of_moons
        
        return planet_as_dict
    
    @classmethod
    def from_dict(cls, planet_data):
        new_planet = Planet(name=planet_data["name"],
                            description=planet_data["description"],
                            distance_from_sun_mln_km=planet_data["distance_from_sun_mln_km"],
                            amount_of_moons=planet_data["amount_of_moons"])
        return new_planet
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    distance_from_sun_mln_km: Mapped[int]
    amount_of_moons: Mapped[int]
    
    moons = relationship('Moon', back_populates='planet', cascade='all, delete-orphan')
    
    def to_dict(self):
        planet_as_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "distance_from_sun_mln_km": self.distance_from_sun_mln_km,
            "amount_of_moons": self.amount_of_moons,
            "moons": [moon.to_dict() for moon in self.moons]  # Includes moons in the planet's response
        }
        
        return planet_as_dict
    
    @classmethod
    def from_dict(cls, planet_data):
        new_planet = Planet(name=planet_data["name"],
                            description=planet_data["description"],
                            distance_from_sun_mln_km=planet_data["distance_from_sun_mln_km"],
                            amount_of_moons=planet_data["amount_of_moons"])
        return new_planet
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    size_km: Mapped[float]  # Size of the moon (in kilometers or chosen unit)
    description: Mapped[str]
    discovery_date: Mapped[str]  # Discovery date as a string (could also be Date type if you prefer)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey('planet.id'))

    planet = relationship("Planet", back_populates="moons")

    def to_dict(self):
        moon_as_dict = {}
        moon_as_dict["id"] = self.id
        moon_as_dict["name"] = self.name
        moon_as_dict["size_km"] = self.size_km
        moon_as_dict["description"] = self.description
        moon_as_dict["discovery_date"] = self.discovery_date
        moon_as_dict["planet_id"] = self.planet_id
        
        return moon_as_dict

    @classmethod
    def from_dict(cls, moon_data, planet_id):
        new_moon = Moon(name=moon_data["name"],
                        size_km=moon_data["size_km"],
                        description=moon_data["description"],
                        discovery_date=moon_data["discovery_date"],
                        planet_id=planet_id)
        return new_moon

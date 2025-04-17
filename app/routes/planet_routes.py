from flask import Blueprint
from app.models.planet import planets

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.get("")
def get_all_planets():
    planets_response = []
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "distance_from_sun": planet.distance_from_sun_km,
                "amount_of_moons": planet.amount_of_moons
            }
        )
    return planets_response
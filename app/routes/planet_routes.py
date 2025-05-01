from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from .route_utilities import validate_model
from ..db import db

bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@bp.post("")
def create_planet():
    request_body = request.get_json()

    try:
        new_planet = Planet.from_dict(request_body)
        
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort (make_response(response, 400))
        
    db.session.add(new_planet)
    db.session.commit()
    
    return new_planet.to_dict(), 201

@bp.get("")
def get_all_planets():
    query = db.select(Planet)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Planet.name.ilike(f"%{name_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    min_distance_param = request.args.get("min_distance")
    if min_distance_param:
        try: 
            min_distance = float(min_distance_param)
            query = query.where(Planet.distance_from_sun_mln_km >= min_distance)
    
        except ValueError:
            pass

    max_distance_param = request.args.get("max_distance")
    if max_distance_param:
        try: 
            max_distance = float(max_distance_param)
            query = query.where(Planet.distance_from_sun_mln_km <= max_distance)
    
        except ValueError:
            pass

    sort_param = request.args.get("sort")
    allowed_sort_fields = ["id", "name", "distance_from_sun_mln_km", "amount_of_moons"]
    if sort_param in allowed_sort_fields:
        query = query.order_by(getattr(Planet, sort_param))
    else:
        query = query.order_by(Planet.name)

    planets = db.session.scalars(query)

    planets_response = []
    for planet in planets:
        planets_response.append(planet.to_dict())
    return planets_response

@bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)

    return planet.to_dict()

@bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.distance_from_sun_mln_km = request_body["distance_from_sun_mln_km"]
    planet.amount_of_moons = request_body["amount_of_moons"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
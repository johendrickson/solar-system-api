from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    distance_from_sun_mln_km = request_body["distance_from_sun_mln_km"]
    amount_of_moons = request_body["amount_of_moons"]

    new_planet = Planet(name=name, 
                        description=description, 
                        distance_from_sun_mln_km=distance_from_sun_mln_km, 
                        amount_of_moons=amount_of_moons)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "description": new_planet.description,
        "distance_from_sun_mln_km": new_planet.distance_from_sun_mln_km,
        "amount_of_moons": new_planet.amount_of_moons,
    }
    return response, 201

@planets_bp.get("")
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
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "distance_from_sun_mln_km": planet.distance_from_sun_mln_km,
                "amount_of_moons": planet.amount_of_moons
            }
        )
    return planets_response

@planets_bp.get("/<planet_id>")
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance_from_sun_mln_km": planet.distance_from_sun_mln_km,
        "amount_of_moons": planet.amount_of_moons,
    }

def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        response = {"message": f"planet {planet_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(Planet).where(Planet.id == planet_id)
    planet = db.session.scalar(query)
    
    if not planet:
        response = {"message": f"planet {planet_id} not found"}
        abort(make_response(response, 404))

    return planet

@planets_bp.put("/<planet_id>")
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.distance_from_sun_mln_km = request_body["distance_from_sun_mln_km"]
    planet.amount_of_moons = request_body["amount_of_moons"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planets_bp.delete("/<planet_id>")
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# @planets_bp.get("")
# def get_all_planets():
#     planets_response = []
#     for planet in planets:
#         planets_response.append(
#             {
#                 "id": planet.id,
#                 "name": planet.name,
#                 "description": planet.description,
#                 "distance_from_sun": planet.distance_from_sun_mln_km,
#                 "amount_of_moons": planet.amount_of_moons
#             }
#         )
#     return planets_response

# @planets_bp.get("/<planet_id>")
# def get_one_planet(planet_id):
#     planet = validate_planet(planet_id)

#     return {
#         "id": planet.id,
#         "name": planet.name,
#         "description": planet.description,
#         "distance_from_sun": planet.distance_from_sun_mln_km,
#         "amount_of_moons": planet.amount_of_moons,
#     }
        
# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except:
#         response = {"message": f"planet {planet_id} invalid"}
#         abort(make_response(response, 400))

#     for planet in planets:
#         if planet.id == planet_id:
#             return planet

#     response = {"message": f"planet {planet_id} not found"}
#     abort(make_response(response, 404))
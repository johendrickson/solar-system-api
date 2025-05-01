from app.routes.route_utilities import validate_model
from app.models.planet import Planet
from werkzeug.exceptions import HTTPException
import pytest

def test_validate_model(two_saved_planets):
    result_planet = validate_model(Planet, 1)
    
    assert result_planet.id == 1
    assert result_planet.name == "Jupiter"
    assert result_planet.description == "Largest planet in the solar system"
    assert result_planet.distance_from_sun_mln_km == 778
    assert result_planet.amount_of_moons == 95
    
def test_validate_model_missing_record(two_saved_planets):
    with pytest.raises(HTTPException) as error:
        result_book = validate_model(Planet, "999")
        
    response = error.value.response
    assert response.status == "404 NOT FOUND"
    
def test_validate_model_invalid_id(two_saved_planets):
    with pytest.raises(HTTPException) as error:
        result_planet = validate_model(Planet, "fire")

    response = error.value.response
    assert response.status == "400 BAD REQUEST"
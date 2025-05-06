from app.models.planet import Planet
import pytest

def test_to_dict_no_missing_data():
    test_data = Planet(id=1,
                    name="Jupiter",
                    description="Largest planet in the solar system",
                    distance_from_sun_mln_km=778,
                    amount_of_moons=95)
    
    result = test_data.to_dict()
    
    assert len(result) == 6
    assert result == {
        "id": 1,
        "name": "Jupiter",
        "description": "Largest planet in the solar system",
        "distance_from_sun_mln_km": 778,
        "amount_of_moons": 95,
        "moons": []  # Assuming no moons yet
    }
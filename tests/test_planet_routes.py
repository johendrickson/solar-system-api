def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []
    
def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Jupiter",
        "description": "Largest planet in the solar system",
        "distance_from_sun_mln_km": 778,
        "amount_of_moons": 95
    }
    
def test_create_one_planet(client):
    response = client.post("/planets", json={
        "name": "Saturn",
        "description": "Second-largest planet with prominent rings",
        "distance_from_sun_mln_km": 1434,
        "amount_of_moons": 83
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Saturn",
        "description": "Second-largest planet with prominent rings",
        "distance_from_sun_mln_km": 1434,
        "amount_of_moons": 83
    }
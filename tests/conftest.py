import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.planet import Planet

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_planets(app):

    jupiter_planet = Planet(name="Jupiter",
                    description="Largest planet in the solar system",
                    distance_from_sun_mln_km= 778,
                    amount_of_moons= 95)
    neptune_planet = Planet(name="Neptune",
                        description="Farthest known planet from the sun",
                        distance_from_sun_mln_km=4495,
                        amount_of_moons=14)

    db.session.add_all([jupiter_planet, neptune_planet])
    db.session.commit()
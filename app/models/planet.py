class Planet:
    def __init__(self, id, name, description, distance_from_sun_mln_km, amount_of_moons):
        self.id = id
        self.name = name
        self.description = description
        self.distance_from_sun_mln_km = distance_from_sun_mln_km
        self.amount_of_moons = amount_of_moons

planets = [
    Planet(1, "Mercury", "Closest to the sun", 57.9, 0),
    Planet(2, "Venus", "Second planet from the sun", 108.2, 0),
    Planet(3, "Earth", "Our home planet", 149.6, 1),
    Planet(4, "Mars", "The 'Red Planet'", 227.9, 2),
]
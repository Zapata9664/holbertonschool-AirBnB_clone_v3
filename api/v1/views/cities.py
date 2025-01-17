#!/usr/bin/python3
"""
<<<<<<< HEAD
city's routes
=======
Citites's routes
>>>>>>> 5a1d92166569b2197f5d01018fb52f16fb2c5e2e
"""

from models.state import State
from models.city import City
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """ Returns a list with all obj """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state_list = []
    for i in state.cities:
        state_list.append(i.to_dict())
    return jsonify(state_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city_id(city_id):
    """ Return one obj """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City obj """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def new_city(state_id):
    """ Create a new City """
    state = storage.get(State, state_id)
    city = request.get_json()
    if city is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in city:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if state is None:
        abort(404)

    new_city = request.get_json()
    new_city['state_id'] = state_id
    cities = City(**new_city)
    cities.save()
    return make_response(jsonify(cities.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Update a City """
    city = storage.get(City, city_id)
    list_to_ignore = ["id", "state_id", "created_at", "updated_at"]

    if city is None:
        abort(404)
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, val in request.get_json().items():
        if key not in list_to_ignore:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict())

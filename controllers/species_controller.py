from flask import jsonify, request

from db import db
from lib.authenticate import authenticate_return_auth
from models.species import Species, species_schema, species_many_schema
from util.reflection import populate_object


@authenticate_return_auth
def add_species(auth_info):
    post_data = request.form if request.form else request.get_json()

    if auth_info.user.role == "grand-master" or auth_info.user.role == "master":

        new_species = Species.new_species_obj()
        populate_object(new_species, post_data)

        db.session.add(new_species)
        db.session.commit()

        return jsonify({"message": "species created", "result": species_schema.dump(new_species)}), 201

    return jsonify({"message": "invalid permisssion"}), 403

def get_species_by_id(species_id):
    species_query = db.session.query(Species).filter(Species.species_id == species_id).first()

    if not species_query:
        return jsonify({"message": "species not found"}), 404

    return jsonify({"message": "species found", "result": species_schema.dump(species_query)}), 200

def get_all_species():
    species_query = db.session.query(Species).all()

    return jsonify({"message": "species found", "results": species_many_schema.dump(species_query)}), 200
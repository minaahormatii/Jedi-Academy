from flask import jsonify, request

from db import db
from lib.authenticate import authenticate_return_auth
from models.temple import Temples, temple_schema, temples_schema
from util.reflection import populate_object


@authenticate_return_auth
def add_temple(auth_info):
    post_data = request.form if request.form else request.get_json()

    if auth_info.user.role == "grand-master":

        new_temple = Temples.new_temple_obj()
        populate_object(new_temple, post_data)

        db.session.add(new_temple)
        db.session.commit()

        return jsonify({"message": "temple created", "result": temple_schema.dump(new_temple)}), 201

    return jsonify({"message": "invalid permisssion"}), 403

def get_temple_by_id(temple_id):
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

    if not temple_query:
        return jsonify({"message": "temple not found"}), 404

    return jsonify({"message": "temple found", "result": temple_schema.dump(temple_query)}), 200

def get_all_temples():
    temple_query = db.session.query(Temples).all()

    return jsonify({"message": "temples found", "results": temples_schema.dump(temple_query)}), 200

@authenticate_return_auth
def update_temple_by_id(temple_id, auth_info):
    post_data = request.form if request.form else request.get_json()
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

    if auth_info.user.role == "grand-master":

        if temple_query:
            populate_object(temple_query, post_data)

            db.session.commit()
            return jsonify({"message": "temple updated", "result": temple_schema.dump(temple_query)}), 200

        return jsonify({"message": "temple not found"}), 404

    return jsonify({"message": "invalid permisssion"}), 403

@authenticate_return_auth
def delete_temple_by_id(temple_id, auth_info):
    temple_query = db.session.query(Temples).filter(Temples.temple_id == temple_id).first()

    if not temple_query:
        return jsonify({"message": "temple not found"}), 404

    if auth_info.user.role == "grand-master":

        try:
            db.session.delete(temple_query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete temple"}), 400

        return jsonify({"message": "temple deleted"}), 200

    return jsonify({"message": "invalid permisssion"}), 403
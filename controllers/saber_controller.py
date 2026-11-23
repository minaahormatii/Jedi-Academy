from flask import jsonify, request

from db import db
from lib.authenticate import authenticate_return_auth
from models.saber import Sabers, saber_schema
from models.app_user import AppUsers
from util.reflection import populate_object


@authenticate_return_auth
def add_saber(auth_info):
    post_data = request.form if request.form else request.get_json()
    owner_id = post_data.get("owner_id")

    if auth_info.user.role == "grand-master" or auth_info.user.role == "padawan":

        if not owner_id:
            return jsonify({"message": "owner_id is required"}), 400

        owner_query = db.session.query(AppUsers).filter(AppUsers.user_id == owner_id).first()

        if not owner_query:
            return jsonify({"message": "owner not found"}), 404

        new_saber = Sabers.new_saber_obj()
        populate_object(new_saber, post_data)

        db.session.add(new_saber)
        db.session.commit()

        return jsonify({"message": "saber created", "result": saber_schema.dump(new_saber)}), 201

    return jsonify({"message": "invalid permisssion"}), 403

def get_saber_by_owner_id(owner_id):
    saber_query = db.session.query(Sabers).filter(Sabers.owner_id == owner_id).first()

    if not saber_query:
        return jsonify({"message": "saber not found"}), 404
    
    return jsonify({"message": "saber found", "result": saber_schema.dump(saber_query)}), 200

@authenticate_return_auth
def update_saber_by_id(saber_id, auth_info):

    saber_query = db.session.query(Sabers).filter(Sabers.saber_id == saber_id).first()
    owner_query = db.session.query(AppUsers).filter(saber_query.owner_id == AppUsers.user_id).first()

    if not saber_query:
        return jsonify({"message": "saber not found"}), 404
    
    if (owner_query and auth_info.user.user_id == owner_query.user_id) or auth_info.user.role == "grand-master":

        post_data = request.form if request.form else request.get_json()
        populate_object(saber_query, post_data)
        db.session.commit()

        return jsonify({"message": "saber updated", "result": saber_schema.dump(saber_query)}), 200

    return jsonify({"message": "invalid permisssion"}), 403

@authenticate_return_auth
def delete_saber_by_id(saber_id, auth_info):
    saber_query = db.session.query(Sabers).filter(Sabers.saber_id == saber_id).first()

    if not saber_query:
        return jsonify({"message": "saber not found"}), 404
    
    owner_query = db.session.query(AppUsers).filter(saber_query.owner_id == AppUsers.user_id).first()

    if not owner_query:
        return jsonify({"message": "owner not found"}), 404

    if auth_info.user.user_id == owner_query.user_id or auth_info.user.role == "council-member" or auth_info.user.role == "grand-master":

        try:
            db.session.delete(saber_query)
            db.session.commit()
            return jsonify({"message": "saber deleted"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "error deleting saber", "error": str(e)}), 500

    return jsonify({"message": "invalid permisssion"}), 403
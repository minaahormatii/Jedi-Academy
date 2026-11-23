from flask import jsonify, request

from db import db
from lib.authenticate import authenticate_return_auth
from models.master import Masters, master_schema, masters_schema
from models.app_user import AppUsers
from models.species import Species
from models.padawan import Padawans
from models.course import Courses
from util.reflection import populate_object

@authenticate_return_auth
def add_master(auth_info):
    post_data = request.form if request.form else request.json
    user_id = post_data.get("user_id")
    species_id = post_data.get("species_id")

    if auth_info.user.role == "grand-master" or auth_info.user.role == "council-member":

        if not user_id:
            return jsonify({"message": "user_id is required"}), 400

        if not species_id:
            return jsonify({"message": "species_id is required"}), 400

        user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
        species_query = db.session.query(Species).filter(Species.species_id == species_id).first()

        if not user_query:
            return jsonify({"message": "user not found"}), 404

        if not species_query:
            return jsonify({"message": "species not found"}), 404


        new_master = Masters.new_master_obj()

        populate_object(new_master, post_data)

        db.session.add(new_master)
        db.session.commit()

        return jsonify({"message": "master created", "result": master_schema.dump(new_master)}), 201

    return jsonify({"message": "invalid permisssion"}), 403

@authenticate_return_auth
def master_get_all(auth_info):
    if auth_info.user.role == "grand-master" or auth_info.user.role == "padawan":

        masters_query = db.session.query(Masters).all()

        return jsonify({"message": "masters found", "results": masters_schema.dump(masters_query)}), 200

    return jsonify({"message": "invalid permissions"}), 403

@authenticate_return_auth
def master_get_by_id(master_id, auth_info):

    master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

    if not master_query:
        return jsonify({"message": "master not found"}), 404
    
    if auth_info.user.role == "grand-master" or str(auth_info.user.user_id) == master_id:

        return jsonify({"message": "master found", "result": master_schema.dump(master_query)}), 200


    return jsonify({"message": "invalid permissions"}), 403

@authenticate_return_auth
def master_update_by_id(master_id, auth_info):

    master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

    if not master_query:
        return jsonify({"message": "master not found"}), 404

    if auth_info.user.role == "grand-master" or auth_info.user.role == "council-member" or str(auth_info.user.user_id) == master_id:

        post_data = request.form if request.form else request.json

        populate_object(master_query, post_data)

        db.session.commit()

        return jsonify({"message": "master updated", "result": master_schema.dump(master_query)}), 200


    return jsonify({"message": "invalid permissions"}), 403

@authenticate_return_auth
def master_delete_by_id(master_id, auth_info):

    if auth_info.user.role != "grand-master":
        return jsonify({"message": "invalid permissions"}), 403

    master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

    if not master_query:
        return jsonify({"message": "master not found"}), 404

    post_data = request.form if request.form else request.json
    new_master_id = post_data.get("new_master_id")

    if not new_master_id:
        return jsonify({"message": "new_master_id is required"}), 400

    new_master_query = db.session.query(Masters).filter(Masters.master_id == new_master_id).first()

    if not new_master_query:
        return jsonify({"message": "replacement master not found"}), 404

    if new_master_query.master_id == master_query.master_id:
        return jsonify({"message": "cannot reassign padawans to the same master"}), 400

    try:
        old_user = db.session.query(AppUsers).filter(AppUsers.user_id == master_query.user_id).first()

        if not old_user:
            return jsonify({"message": "master user not found"}), 404

        for padawan in master_query.padawans:
            padawan.master_id = new_master_query.master_id

        old_user.role = "padawan"

        db.session.delete(master_query)
        db.session.commit()

        return jsonify({"message": "master status removed and padawans reassigned"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "error removing master status", "error": str(e)}), 500

@authenticate_return_auth
def order_66(auth_info):

    if auth_info.user.role != "grand-master":
        return jsonify({"message": "invalid permission"}), 403

    try:
        db.session.query(Padawans).delete()
        db.session.query(Courses).update({Courses.master_id: None})
        db.session.query(Masters).delete()
        db.session.commit()

        return jsonify({"message": "order 66 executed"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "order 66 failed.", "error": str(e)}), 500

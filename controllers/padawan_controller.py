from flask import jsonify, request

from datetime import date

from db import db
from lib.authenticate import authenticate_return_auth
from models.padawan import Padawans, padawan_schema, padawans_schema
from models.master import Masters
from models.app_user import AppUsers
from models.species import Species
from models.course import Courses
from util.reflection import populate_object

@authenticate_return_auth
def add_padawan(auth_info):
    post_data = request.form if request.form else request.json
    master_id = post_data.get("master_id")
    user_id = post_data.get("user_id")
    species_id = post_data.get("species_id")

    if auth_info.user.role == "grand-master" or auth_info.user.role == "master":

        if not master_id:
            return jsonify({"message": "master_id is required"}), 400

        if not user_id:
            return jsonify({"message": "user_id is required"}), 400

        if not species_id:
            return jsonify({"message": "species_id is required"}), 400

        master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()
        user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()
        species_query = db.session.query(Species).filter(Species.species_id == species_id).first()

        if not master_query:
            return jsonify({"message": "master not found"}), 404

        if not user_query:
            return jsonify({"message": "user not found"}), 404

        if not species_query:
            return jsonify({"message": "species not found"}), 404


        new_padawan = Padawans.new_padawan_obj()

        populate_object(new_padawan, post_data)

        db.session.add(new_padawan)
        db.session.commit()

        return jsonify({"message": "padawan created", "result": padawan_schema.dump(new_padawan)}), 201

    return jsonify({"message": "invalid permisssion"}), 403

@authenticate_return_auth
def enroll_padawan_in_course(auth_info):
    post_data = request.get_json()

    padawan_id = post_data.get("padawan_id")
    course_id = post_data.get("course_id")

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404

    if not course_query:
        return jsonify({"message": "course not found"}), 404

    if auth_info.user.role == "master":
        master_query = db.session.query(Masters).filter(Masters.user_id == auth_info.user.user_id).first()

        if not master_query or master_query.master_id != course_query.master_id:
            return jsonify({"message": "invalid permission"}), 403

    elif auth_info.user.role != "grand-master":
        return jsonify({"message": "invalid permission"}), 403

    if course_query in padawan_query.courses:
        return jsonify({"message": "padawan already enrolled"}), 409

    padawan_query.courses.append(course_query)
    db.session.commit()

    return jsonify({"message": "padawan added to course", "result": padawan_schema.dump(padawan_query)}), 200

@authenticate_return_auth
def remove_padawan_from_course(auth_info):
    post_data = request.get_json()
    
    padawan_id = post_data.get("padawan_id")
    course_id = post_data.get("course_id")

    if not padawan_id or not course_id:
        return jsonify({"message": "padawan_id and course_id are required."}), 400


    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404

    if not course_query:
        return jsonify({"message": "course not found"}), 404

    if auth_info.user.role == "master":
        master_query = db.session.query(Masters).filter(Masters.user_id == auth_info.user.user_id).first()

        if not master_query or master_query.master_id != course_query.master_id:
            return jsonify({"message": "invalid permission"}), 403

    elif auth_info.user.role != "grand-master":
        return jsonify({"message": "invalid permission"}), 403

    if course_query not in padawan_query.courses:
        return jsonify({"message": "padawan not enrolled"}), 409

    padawan_query.courses.remove(course_query)
    db.session.commit()

    return jsonify({"message": "padawan removed from course", "result": padawan_schema.dump(padawan_query)}), 200

@authenticate_return_auth
def padawan_get_all(auth_info):
    if auth_info.user.role == "grand-master" or auth_info.user.role == "master":

        padawans_query = db.session.query(Padawans).all()
        
        return jsonify({"message": "padawans found", "results": padawans_schema.dump(padawans_query)}), 200
    
    return jsonify({"message": "invalid permissions"}), 403

def padawan_get_active():
    today = date.today()
    padawans_query = db.session.query(Padawans).filter((Padawans.graduation_date == None) | (Padawans.graduation_date > today)).all()

    if not padawans_query:
        return jsonify({"message": "padawans not found"}), 404

    return jsonify({"message": "active padawans found", "results": padawans_schema.dump(padawans_query)}), 200

@authenticate_return_auth
def padawan_update_by_id(padawan_id, auth_info):

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()
    master_query = db.session.query(Masters).filter(Masters.user_id == auth_info.user.user_id).first()

    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404

    
    if (auth_info.user.role == "grand-master" or auth_info.user.role == "council-member"
    or (master_query and master_query.master_id == padawan_query.master_id)):

        post_data = request.form if request.form else request.json

        populate_object(padawan_query, post_data)

        db.session.commit()

        return jsonify({"message": "padawan updated", "result": padawan_schema.dump(padawan_query)}), 200


    return jsonify({"message": "invalid permissions"}), 403

@authenticate_return_auth
def padawan_promote_by_id(padawan_id, auth_info):

    if auth_info.user.role not in ["grand-master", "council-member"]:
        return jsonify({"message": "invalid permission"}), 403

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404

    if not padawan_query.graduation_date or padawan_query.graduation_date > date.today():
        return jsonify({"message": "padawan must graduate before promotion"}), 400

    try:
        padawan_query.user.role = "knight"
        db.session.commit()

        return jsonify({"message": "padawan promoted to Jedi Knight", "result": padawan_schema.dump(padawan_query)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "promotion failed", "error": str(e)}), 500

@authenticate_return_auth
def padawan_get_by_id(padawan_id, auth_info):

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404
    
    if auth_info.user.role == "grand-master" or str(auth_info.padawan.padawan_id) == padawan_id:

        return jsonify({"message": "padawan found", "result": padawan_schema.dump(padawan_query)}), 200


    return jsonify({"message": "invalid permissions"}), 403

@authenticate_return_auth
def padawan_delete_by_id(padawan_id, auth_info):

    padawan_query = db.session.query(Padawans).filter(Padawans.padawan_id == padawan_id).first()

    if not padawan_query:
        return jsonify({"message": "padawan not found"}), 404
    
    if auth_info.user.role == "grand-master":

        db.session.delete(padawan_query)
        db.session.commit()

        return jsonify({"message": "padawan deleted"}), 200


    return jsonify({"message": "invalid permissions"}), 403
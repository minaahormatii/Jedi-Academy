from flask import jsonify, request

from db import db
from lib.authenticate import authenticate_return_auth
from models.course import Courses, course_schema, courses_schema
from models.master import Masters
from util.reflection import populate_object

@authenticate_return_auth
def add_course(auth_info):
    post_data = request.form if request.form else request.get_json()
    master_id = post_data.get("master_id")

    if auth_info.user.role == "grand-master" or auth_info.user.role == "master":

        if not master_id:
            return jsonify({"message": "master_id is required"}), 400

        master_query = db.session.query(Masters).filter(Masters.master_id == master_id).first()

        if not master_query:
            return jsonify({"message": "master not found"}), 404

        new_course = Courses.new_course_obj()
        populate_object(new_course, post_data)

        db.session.add(new_course)
        db.session.commit()

        return jsonify({"message": "course created", "result": course_schema.dump(new_course)}), 201

    return jsonify({"message": "invalid permisssion"}), 403

def get_course_by_id(course_id):
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if not course_query:
        return jsonify({"message": "course not found"}), 404
    
    return jsonify({"message": "course found", "result": course_schema.dump(course_query)}), 200

def get_course_by_difficulty(difficulty):
    course_query = db.session.query(Courses).filter(Courses.difficulty == difficulty).all()

    if not course_query:
        return jsonify({"message": "course not found"}), 404
    
    return jsonify({"message": "course found", "results": courses_schema.dump(course_query)}), 200

@authenticate_return_auth
def update_course_by_id(course_id, auth_info):
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()
    master_query = db.session.query(Masters).filter(Masters.user_id == auth_info.user.user_id).first()

    if not course_query:
        return jsonify({"message": "course not found"}), 404

    if auth_info.user.role == "council-member" or auth_info.user.role == "grand-master" or master_query.master_id == course_query.master_id:

        post_data = request.form if request.form else request.get_json()

        if course_query:
            populate_object(course_query, post_data)

            db.session.commit()

            return jsonify({"message": "course updated", "result": course_schema.dump(course_query)}), 200

    return jsonify({"message": "invalid permisssion"}), 403

@authenticate_return_auth
def delete_course_by_id(course_id, auth_info):
    course_query = db.session.query(Courses).filter(Courses.course_id == course_id).first()

    if not course_query:
            return jsonify({"message": "course not found"}), 404

    if auth_info.user.role == "council-member" or auth_info.user.role == "grand-master":
        db.session.delete(course_query)
        db.session.commit()
        
        return jsonify({"message": "course deleted"}), 200

    
    master_query = db.session.query(Masters).filter(Masters.user_id == auth_info.user.user_id).first()

    if master_query and master_query.master_id == course_query.master_id:

        db.session.delete(course_query)
        db.session.commit()

        return jsonify({"message": "course deleted"}), 200

    return jsonify({"message": "invalid permisssion"}), 403
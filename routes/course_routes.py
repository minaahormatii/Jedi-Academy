from flask import Blueprint

import controllers
from models import course

course = Blueprint('course', __name__)

@course.route("/course", methods=["POST"])
def add_course():
    return controllers.add_course()

@course.route("/course/<course_id>", methods=["GET"])
def get_course_by_id(course_id):
    return controllers.get_course_by_id(course_id)

@course.route("/course/difficulty/<difficulty>", methods=["GET"])
def get_course_by_difficulty(difficulty):
    return controllers.get_course_by_difficulty(difficulty)

@course.route("/course/<course_id>", methods=["PUT"])
def update_course_by_id(course_id):
    return controllers.update_course_by_id(course_id)

@course.route("/course/delete/<course_id>", methods=["DELETE"])
def delete_course_by_id(course_id):
    return controllers.delete_course_by_id(course_id)
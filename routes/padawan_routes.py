from flask import Blueprint

import controllers

padawan = Blueprint('padawan', __name__)


@padawan.route("/padawan", methods=["POST"])
def add_padawan():
    return controllers.add_padawan()

@padawan.route("/padawans", methods=["GET"])
def padawan_get_all():
    return controllers.padawan_get_all()

@padawan.route("/padawans/active", methods=["GET"])
def padawan_get_active():
    return controllers.padawan_get_active()

@padawan.route("/padawan/<padawan_id>", methods=["PUT"])
def padawan_update_by_id(padawan_id):
    return controllers.padawan_update_by_id(padawan_id)

@padawan.route("/padawan/promote/<padawan_id>", methods=["PUT"])
def padawan_promote_by_id(padawan_id):
    return controllers.padawan_promote_by_id(padawan_id)

@padawan.route("/padawan/<padawan_id>", methods=["GET"])
def padawan_get_by_id(padawan_id):
    return controllers.padawan_get_by_id(padawan_id)

@padawan.route("/padawan/delete/<padawan_id>", methods=["DELETE"])
def padawan_delete_by_id(padawan_id):
    return controllers.padawan_delete_by_id(padawan_id)

@padawan.route("/padawan/course", methods=["POST", "PUT"])
def enroll_padawan_in_course():
    return controllers.enroll_padawan_in_course()

@padawan.route("/padawan/course/remove", methods=["DELETE"])
def remove_padawan_from_course():
    return controllers.remove_padawan_from_course()



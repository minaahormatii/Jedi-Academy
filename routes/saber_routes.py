from flask import Blueprint

import controllers

saber = Blueprint('saber', __name__)

@saber.route("/saber", methods=["POST"])
def add_saber():
    return controllers.add_saber()

@saber.route("/saber/<owner_id>", methods=["GET"])
def get_saber_by_owner_id(owner_id):
    return controllers.get_saber_by_owner_id(owner_id)

@saber.route("/saber/<saber_id>", methods=["PUT"])
def update_saber_by_id(saber_id):
    return controllers.update_saber_by_id(saber_id)

@saber.route("/saber/delete/<saber_id>", methods=["DELETE"])
def delete_saber_by_id(saber_id):
    return controllers.delete_saber_by_id(saber_id)

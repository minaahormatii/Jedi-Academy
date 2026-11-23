from flask import Blueprint

import controllers

master = Blueprint("master", __name__)

@master.route("/master", methods=["POST"])
def add_master():
    return controllers.add_master()

@master.route("/masters", methods=["GET"])
def master_get_all():
    return controllers.master_get_all()

@master.route("/master/<master_id>", methods=["GET"])
def master_get_by_id(master_id):
    return controllers.master_get_by_id(master_id)

@master.route("/master/<master_id>", methods=["PUT"])
def master_update_by_id(master_id):
    return controllers.master_update_by_id(master_id)

@master.route("/master/delete/<master_id>", methods=["DELETE"])
def master_delete_by_id(master_id):
    return controllers.master_delete_by_id(master_id)

@master.route("/order-66", methods=["DELETE"])
def order_66():
    return controllers.order_66()
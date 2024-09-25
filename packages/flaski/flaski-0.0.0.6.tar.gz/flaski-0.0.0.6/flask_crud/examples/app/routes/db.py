from flask import Blueprint, request
from app.dbutil import DBController
from app.routes.base import Route

class DBRoute(Route):
    url_prefix = "/db"
    blueprint = Blueprint("db", __name__)
    
    @blueprint.route("usuarios", methods=["GET", "POST"])
    def usuario():
        if request.method == "POST":
            DBController.update("INSERT INTO usuarios() ")
        return DBController.all("usuarios")
    
    @blueprint.route("clientes", methods=["GET", "POST"])
    def cliente():
        if request.method == "POST":
            DBController.update("INSERT INTO usuarios ")
        return DBController.all("usuarios")

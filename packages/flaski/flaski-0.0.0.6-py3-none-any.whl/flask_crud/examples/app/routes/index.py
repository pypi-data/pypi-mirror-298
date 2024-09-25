from flask import Blueprint, redirect, url_for
from app.routes.base import MenuBase, Route

class IndexRoute(Route):
    blueprint = Blueprint("index", __name__)

    @blueprint.route("/")
    def index():
        return redirect(url_for("index.dashboard"))
    
    @blueprint.route("/dashboard")
    def dashboard():
        return MenuBase.render("dashboard.html")  
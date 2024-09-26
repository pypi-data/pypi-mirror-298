from flask import Blueprint, redirect, url_for
from flask_login import login_required
from app.routes.base import MenuBase
from flask_crud.routeutil import Route

class IndexRoute(Route):
    blueprint = Blueprint("index", __name__)

    @blueprint.route("/")
    def index():
        # return redirect(url_for("index.dashboard"))        
        return redirect(url_for("auth.login"))
    
    @blueprint.route("/dashboard")
    @login_required
    def dashboard():
        return MenuBase.render("dashboard.html")  

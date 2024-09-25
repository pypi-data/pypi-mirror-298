from app.config import Config
from flask_mysqldb import MySQL
from flask import Flask, render_template

from app.dbutil import DBController
from app.routes.db import DBRoute
from .routes.options import IngresoRoute, InformeRoute, EliminacionMantenimientoRoute
from .routes.index import IndexRoute

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql = MySQL(app)
    DBController.mysql = mysql
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    IndexRoute.to(app)
    IngresoRoute.to(app)
    InformeRoute.to(app)
    EliminacionMantenimientoRoute.to(app)
    DBRoute.to(app)
    return app


from app.config.dbconfig import DBConfig
from flask_mysqldb import MySQL
from flask import Flask, render_template

from flask_crud.dbutil import DBController, DBMapper
from flask_crud.routeutil import Route
from flask_crud.util import import_submodules
from flask_crud.manage import CrudEntityStore
from app.config.authconfig import preRegisterBlueprint
import_submodules('app.routes')
import_submodules('app.admin_viewmodel')
import_submodules('app.admin_dbmapper')
import_submodules('app.viewmodels')
import_submodules('app.dbmappers')
CrudEntityStore.executePosRenderViews()

Route.preRegisterBlueprint = preRegisterBlueprint

print("DBMappers: "+str(DBMapper._db_mappers))
print("Routes: "+str(Route._routes))
def create_app():
    app = Flask(__name__)
    # Configuración de la base datos
    app.config.from_object(DBConfig)
    mysql = MySQL(app)
    DBController.mysql = mysql    
    # Página 404    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    for route in Route._routes:
        route:Route
        route.to(app)
    # IndexRoute.to(app)
    # IngresoRoute.to(app)
    # InformeRoute.to(app)
    # EliminacionMantenimientoRoute.to(app)
    return app


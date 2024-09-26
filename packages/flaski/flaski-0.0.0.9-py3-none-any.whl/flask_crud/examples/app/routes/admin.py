from flask import Blueprint, redirect, request, url_for
from flask_crud.dbutil import DBController, DBMapper
from flask_crud.routeutil import Route
from flask_crud.manage import CrudEntityStore

from app.routes.base import MenuBase


class AdminRoute(Route):
    blueprint = Blueprint("admin", __name__)

    @blueprint.route("/edit-usuario", methods=["GET","POST"])
    def update(id=None):
        return f"id {id}"
    
    @blueprint.route("/delete-usuario", methods=["GET","POST"])
    def delete(id=None):
        return f"id {id}"
    

    @blueprint.route("/registrar-usuario")
    def registrar():
        if request.method == "POST":
            DBMapper.exec("admin-registra-usuario", request.form)
        view_edit_user = CrudEntityStore.getView("edit-user")
        return MenuBase.renderFromFactory(
            main_title="Registrar usuario",
            comps_data=[
                {
                    "type":"form",
                    "form_data": view_edit_user.form.toForm(None)
                }
            ],
        )
    
    @blueprint.route("/editar-usuario", methods=["GET","POST"])
    def editar(id=None):
        usersdata = None
        user_formdata = None
        if request.method == "POST":  
            if id is not None:                      
                user_formdata = DBController.queryOne("SELECT * FROM usuarios u WHERE u.id=%s", (id,))
            elif request.form:
                DBController.updateOne("usuarios", "id", request.form)                
        usersdata = DBController.all("usuarios")
        view_edit_user = CrudEntityStore.getView("edit-user")
        return MenuBase.renderFromFactory(
            main_title="Editar usuario",
            comps_data=[
                {
                    "type":"form",
                    "form_data": view_edit_user.form.toForm(user_formdata)
                },
                {
                    "type":"table",
                    "table_data": view_edit_user.table.toTable(usersdata)
                }
            ],
        )

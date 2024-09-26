from flask import flash
from flask_crud.dbutil import DBMapper
from flask_crud.dbutil import DBController

class ConsultarUsuarios(DBMapper):
    dbmapper_name = "admin-registra-usuario"
    @staticmethod
    def operation(form):
        try:
            if DBController.insertUpdateOne("usuarios", "username", form):                
                flash("Usuario registrado con éxito", "success")
            else:
                flash("El usuario ya estaba registrado, se actualizo con éxito", "info")
        except Exception as e:
            flash(str(e), "danger")

# class ConsultarUsuarios(DBMapper):
#     dbmapper_name = "admin-consulta-usuarios"
#     @staticmethod
#     def operation(form):
#         try:
#             DBController.insertUpdateOne("vehiculo", "matricula", form)
#             flash("Vehiculo registrado con éxito", "success")
#         except Exception as e:
#             flash(str(e), "warning")
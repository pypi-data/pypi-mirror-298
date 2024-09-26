from flask_crud.manage import CrudRegistrable
from flask_crud.view import ViewConfig
from app.config.permission import roles
from app.config.viewmodelconfig import DeleteOpt, EditOpt
from app.config.viewmodelconfig import cancel_btn, main_btn, delete_btn

class ImplDefaultPosRenderView:
    @staticmethod
    def posRenderView(view):
        view.form.main_btn = main_btn
        view.form.cancel_btn = cancel_btn
CrudRegistrable.posRenderView = ImplDefaultPosRenderView.posRenderView

class EditarUserViewCfg(CrudRegistrable):
    table_name = "usuarios"  # Nombre de la tabla en la base de datos
    id_name = "id"  # Nombre de la columna del ID en la tabla
    entity_name = "edit-user"  # Nombre de la entidad para uso en la lógica de negocio
    enums = {
        "role_name": list(roles.keys()),
        "estado_usuario":["ACTIVO", "INACTIVO"]
    }
    requireds = [
        "estado_usuario",
        "role_name",
        "username",
        "password",
    ]  # Campos requeridos

    def __init__(
        self,
        role_name="SELECCIONE:",
        estado_usuario="SELECCIONE:",
        username="",
        password="",
        email="morocho@gmail.com",
        telefono="0958967172",
    ) -> None:
        self.role_name = role_name
        self.estado_usuario = estado_usuario
        self.username = username
        self.password = password
        self.email = email
        self.telefono = telefono

    @staticmethod
    def posRenderView(view:ViewConfig):
        editOpt = EditOpt.copy()
        deleteOpt = DeleteOpt.copy()
        editOpt.endpoint_name = "admin.editar"
        deleteOpt.endpoint_name = "admin.delete"
        view.table.opts["edit"] = editOpt
        view.table.opts["del"] = deleteOpt
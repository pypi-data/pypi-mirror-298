from flask_crud.view import Btn, Opt

main_btn = Btn(
    # "Guardar",
    "Guardar",
    isSubmit=True,
    # htmlclass="btn btn-primary",
    htmlclass="btn btn-success",
)
delete_btn = Btn(
    "Eliminar",
    isSubmit=True,
    # htmlclass="btn btn-primary",
    htmlclass="btn btn-danger",
)
cancel_btn = Btn(
    "Cancelar",
    htmlclass="btn btn-secondary",
    endpoint_name="index.dashboard",
)

# Para las tablas 
EditOpt = Opt(
    name_action= "Editar",
    isGetId= True,
    endpoint_name="edit",
    htmlclass="btn btn-warning btn-sm"
)
DeleteOpt = Opt(
    name_action= "Eliminar",
    isPostId= True,
    endpoint_name="delete",
    htmlclass="btn btn-danger btn-sm"
)

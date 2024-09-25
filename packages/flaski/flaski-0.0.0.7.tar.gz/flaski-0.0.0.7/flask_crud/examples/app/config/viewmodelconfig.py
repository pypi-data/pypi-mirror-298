from flask_crud.view import Btn

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

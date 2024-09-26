menu_opts = [
        {
            "text": "Ingreso",
            "childs":[
                {
                "text": "Vehículo",
                "endpoint":"ingreso.vehiculo",
                },
                {
                "text": "Clientes",
                "endpoint":"ingreso.cliente",
                },
                {
                "text": "Revisiones",
                "endpoint":"ingreso.revision",
                },
                {
                "text": "Regresar",
                "endpoint":"index.dashboard",
                },
            ]
        },
        {
            "text": "Informe",
            "childs":[
                {
                "text": "Clientes",
                "endpoint":"informe.cliente"
                },
                {
                "text": "Mantenimiento",
                "endpoint":"informe.revision"
                },
                {
                "text": "Regresar",
                "endpoint":"index.dashboard",
                },
            ]
        },
        {
        "text": "Eliminación",
        "endpoint":"eliminacion.eliminar",
        },
        {
        "text": "Salir",
        "endpoint":"auth.logout",
        },
    ]

endpoints_cliente = []
def collect_endpoints(menu_opts, endpoint_list:list[str]):
    for menuitem in menu_opts:
        if "endpoint" in menuitem:
            endpoint_list.append(menuitem["endpoint"])
        if "childs" in menuitem:
            collect_endpoints(menuitem, endpoint_list)
collect_endpoints(menu_opts, endpoints_cliente)
    

VALUE_ALL_PERMISSIONS = "all"
admin_opt =         {
            "text": "Gestión usuarios",
            "childs":[
                {
                "text": "Registrar",
                    "endpoint":"admin.registrar",
                },
                {
                "text": "Editar",
                    "endpoint":"admin.editar",
                },
            ]
        }

admin_menu_opts = menu_opts.copy()
admin_menu_opts.insert(0, admin_opt)
permisos_admin = {
    "endpoints": VALUE_ALL_PERMISSIONS,
    "menu": admin_menu_opts
}
permisos_cliente = {
    "endpoints": endpoints_cliente,
    "menu":menu_opts
}

roles = {}
# roles["ADMIN"] = permisos_admin
roles["ADMINISTRADOR"] = permisos_admin
# roles["CLIENTE"] = permisos_cliente
roles["CLIENTE"] = permisos_admin
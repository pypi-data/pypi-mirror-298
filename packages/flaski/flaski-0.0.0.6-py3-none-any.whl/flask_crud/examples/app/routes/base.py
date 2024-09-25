from flask import Flask, Blueprint, render_template

class Route:
    url_prefix = ""
    blueprint: Blueprint = None

    @classmethod
    def to(cls, app: Flask):
        if cls.blueprint:
            app.register_blueprint(cls.blueprint, url_prefix=cls.url_prefix)

class MenuBase:
    title = "Menu"
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
        },
    ]

    @classmethod
    def renderFromFactory(cls, main_title, comps_data):        
        return cls.render(
            "macros/template_factory.html",
            main_title=main_title,
            comps_data=comps_data)

    @classmethod
    def render(cls, template_name_or_list: str| list[str], **context):        
        menu_data = {
            "title": cls.title,
            "opts": cls.menu_opts,
        }
        return render_template(template_name_or_list, menu_data=menu_data, **context)

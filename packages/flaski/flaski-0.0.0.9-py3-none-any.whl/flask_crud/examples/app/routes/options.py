from flask_crud.dbutil import DBMapper
from app.routes.base import MenuBase
from flask_crud.routeutil import Route
from flask import Blueprint, request
from flask_crud.manage import CrudEntityStore
from flask_crud.view import ViewConfig
from app.viewmodels import (
    ClienteConsultaViewCfg,
    MantenimientoEliminacionViewCfg,
    # IngresoVehiculoViewCfg,
    IngresoClienteViewCfg,
    RevisionViewCfg,
    VehiculoCompradoViewCfg,
)

class IngresoRoute(Route):
    url_prefix = "/ingreso"
    blueprint = Blueprint("ingreso", __name__)

    @blueprint.route("/vehiculo", methods=["GET", "POST"])
    def vehiculo():
        if request.method == "POST":
            DBMapper.exec("add-or-update-vehiculo", request.form)
        vehiculoView: ViewConfig = CrudEntityStore.getView("view-registro-vehiculo")
        return MenuBase.render(
            "macros/template_factory.html",
            main_title="Ingreso de vehículos",
            comps_data=[{"type": "form", "form_data": vehiculoView.form.toForm(None)}],
        )
    
    @blueprint.route("/clientes", methods=["GET", "POST"])
    def cliente():
        if request.method == "POST":
            # Decodificar el campo 'selecteds'
            DBMapper.exec("registra cliente y compra de vehiculos", request.form)
        client_view: ViewConfig = CrudEntityStore.getView(
            IngresoClienteViewCfg.entity_name
        )
        table_data = DBMapper.getSimple("vehiculos a la venta")
        return MenuBase.render(
            "macros/template_factory.html",
            main_title="Ingreso de clientes",
            comps_data=[
                {
                    # "type": "viewer",
                    "type": "form+table_selector",
                    "form_data": client_view.form.toForm(None),
                    "viewer_data": table_data[0] if table_data else None,
                    "mount_field": {
                        "stock_name": "cantidad_disponible",
                        "name": "cantidad",
                        "label": "Cantidad a comprar",
                        "head": "Cantidad",
                        "text_btn": "Agregar",
                    },
                    "cfg_table_selector": {
                        "detail_title": "Detalles del vehiculo",
                        "order_title": "Orden/Pedido",
                        "sales_title": "Vehiculos a la venta",
                    },
                    # END: Viewer settings
                    "table_data": table_data,
                },
            ],
        )

    @blueprint.route("/revisiones", methods=["GET", "POST"])
    def revision():
        CrudEntityStore.getEntity(RevisionViewCfg.entity_name)
        if request.method == "POST":
            return request.form
        vehiculoView = CrudEntityStore.getView(VehiculoCompradoViewCfg.entity_name)
        # vehiculoView.form.main_btn = main_btn
        # vehiculoView.form.cancel_btn = cancel_btn
        revisionView = CrudEntityStore.getView(RevisionViewCfg.entity_name)
        data_to_table = None
        data_to_table = [
            {
                "matricula": "MAS-544",
                "marca": "Volksvagen",
                "modelo": "",
                "color": "Verde Neon",
                "precio_de_venta": 17188,
                "cantidad_disponible": 10,
            },
            {
                "matricula": "OMD-454",
                "marca": "mazda",
                "modelo": "",
                "color": "Verde Neon",
                "precio_de_venta": 17188,
                "cantidad_disponible": 10,
            },
        ]
        clienteConsultaViewCfg = CrudEntityStore.getView(ClienteConsultaViewCfg.entity_name)
        clienteConsultaViewCfg.form.title = "Consulta cliente"
        return MenuBase.render(
            "macros/template_factory.html",
            main_title="Ingreso de revisiones",
            comps_data=[
                {
                    "type": "form",
                    "form_data": clienteConsultaViewCfg.form.toForm(None),
                },
                {
                    "type": "form+simple_selector",
                    "form_data": revisionView.form.toForm(None),
                    "table_data": data_to_table,
                    "cfg_simple_selector": {"title": "Seleccionar Vehiculos:"},
                },
                # {
                #     "type":"form+table",
                #     "form_data":revisionView.form.toForm(None),
                #     "table_data":vehiculoView.table.toTable(data_to_table),
                # },
            ],
        )


class InformeRoute(Route):
    url_prefix = "/informe"
    blueprint = Blueprint("informe", __name__)

    @blueprint.route("/clientes", methods=["GET", "POST"])
    def cliente():
        vehicles = [
            {
                "matricula": "MAS-544",
                "marca": "Volksvagen",
                "modelo": "",
                "color": "Verde Neon",
                "precio_de_venta": 17188,
                "cantidad_disponible": 10,
            },
            {
                "matricula": "OMD-454",
                "marca": "mazda",
                "modelo": "",
                "color": "Verde Neon",
                "precio_de_venta": 17188,
                "cantidad_disponible": 10,
            },
        ]
        clients = [
            {"name": "Jos", "edad": "25", "estado": "vivo :)", "vehiculos": vehicles}
        ]
        return MenuBase.render(
            "macros/template_factory.html",
            main_title="Informe de clientes",
            comps_data=[{"type": "table2", "table_data": clients}],
        )

    @blueprint.route("/revisiones", methods=["GET", "POST"])
    def revision():
        CrudEntityStore.getEntity(RevisionViewCfg.entity_name)
        if request.method == "POST":
            return request.form
        revisionView = CrudEntityStore.getView(RevisionViewCfg.entity_name)
        clienteConsultaViewCfg = CrudEntityStore.getView(
            ClienteConsultaViewCfg.entity_name
        )
        clienteConsultaViewCfg.form.title = "Consulta cliente"
        revisionView.table.title = "Revisiones realizadas"
        return MenuBase.render(
            "macros/template_factory.html",
            main_title="Informe de revisiones",
            comps_data=[
                {
                    "type": "form",
                    "form_data": clienteConsultaViewCfg.form.toForm(None),
                },
                {
                    "type": "table",
                    "table_data": revisionView.table.toTable(None),
                },
            ],
        )


class EliminacionMantenimientoRoute(Route):
    url_prefix = "/eliminacion"
    blueprint = Blueprint("eliminacion", __name__)

    @blueprint.route("", methods=["GET", "POST"])
    def eliminar():
        if request.method == "POST":
            return request.form
        viewDeleteMantenimiento = CrudEntityStore.getView(
            MantenimientoEliminacionViewCfg.entity_name
        )
        return MenuBase.renderFromFactory(
            main_title="Eliminación de mantenimientos",
            comps_data=[
                {"type": "form", "form_data": viewDeleteMantenimiento.form.toForm(None)}
            ],
        )

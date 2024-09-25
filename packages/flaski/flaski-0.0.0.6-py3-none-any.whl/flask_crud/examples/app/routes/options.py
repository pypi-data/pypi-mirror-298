import json
from app.dbutil import DBController
from app.viewmodels import (
    ClienteConsultaViewCfg,
    MantenimientoEliminacionViewCfg,
    IngresoVehiculoViewCfg,
    IngresoClienteViewCfg,
    RevisionViewCfg,
    VehiculoCompradoViewCfg,
)
from app.routes.base import MenuBase, Route
from flask import Blueprint, request, flash
from flask_crud.manage import CrudEntityStore
from flask_crud.view import ViewConfig, Btn

main_btn = Btn(
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
    "Cancelar", htmlclass="btn btn-secondary", endpoint_name="index.dashboard"
)

for entity_name, view in CrudEntityStore.getViews().items():
    if view and view.form:
        if entity_name == ClienteConsultaViewCfg.entity_name:
            view.form.main_btn = main_btn.copyName("Consultar")
            view.form.cancel_btn = None
            continue
        if entity_name == MantenimientoEliminacionViewCfg.entity_name:
            view.form.main_btn = delete_btn.copyName("Dar de baja")
            view.form.cancel_btn = cancel_btn.copyName("Volver")
            continue
        view.form.main_btn = main_btn
        view.form.cancel_btn = cancel_btn


class IngresoRoute(Route):
    url_prefix = "/ingreso"
    blueprint = Blueprint("ingreso", __name__)

    @blueprint.route("/vehiculo", methods=["GET", "POST"])
    def vehiculo():
        if request.method == "POST":
            try:
                DBController.insertUpdateOne("vehiculo", "matricula", request.form)
                flash("Vehiculo registrado con éxito", "success")
            except Exception as e:
                flash(str(e), "warning")
        CrudEntityStore.getEntity(IngresoVehiculoViewCfg.entity_name)
        vehiculoView: ViewConfig = CrudEntityStore.getView(
            IngresoVehiculoViewCfg.entity_name
        )
        return MenuBase.render(
            "macros/template_factory.html",
            main_title="Ingreso de vehículos",
            comps_data=[{"type": "form", "form_data": vehiculoView.form.toForm(None)}],
        )

    @blueprint.route("/clientes", methods=["GET", "POST"])
    def cliente():
        if request.method == "POST":
            # Decodificar el campo 'selecteds'
            selecteds = json.loads(request.form["selecteds"])
            client = dict(request.form)
            client.pop("selecteds")
            client = client
            DBController.insert("clientes", client)
            for item in selecteds:
                values = (
                    item["color"],
                    item["marca"],
                    item["modelo"],
                    item["precio_de_venta"],
                    # cantidad a comprar
                    item["quantity"],
                )
                # Seleccionar tantos ids como numero de vehiculos a comprar
                ids = DBController.query(
                    """
                    SELECT id
                    FROM vehiculo
                    WHERE color = %s
                    AND marca = %s
                    AND modelo = %s
                    AND precio_de_venta = %s
                    LIMIT %s;
                    """,
                    values,
                )
                for i in ids:
                    id_vehiculo = i["id"]
                    DBController.execute(
                        """
                        INSERT INTO ventas (id_cliente, id_vehiculo) 
                        VALUES (LAST_INSERT_ID(), %s); 
                        """,
                        (id_vehiculo,),
                    )
                # DBController.insert("ventas", )
            return selecteds
        client_view: ViewConfig = CrudEntityStore.getView(
            IngresoClienteViewCfg.entity_name
        )
        table_data = DBController.query(
            """
                SELECT 
                    vh.marca, 
                    vh.modelo, 
                    vh.color, 
                    vh.precio_de_venta, 
                    COUNT(vh.id) AS cantidad_disponible
                FROM vehiculo vh
                LEFT JOIN ventas vt ON vh.id = vt.id_vehiculo
                WHERE vt.id_vehiculo IS NULL
                GROUP BY vh.marca, vh.modelo, vh.color, vh.precio_de_venta;
        """,
            None,
        )
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

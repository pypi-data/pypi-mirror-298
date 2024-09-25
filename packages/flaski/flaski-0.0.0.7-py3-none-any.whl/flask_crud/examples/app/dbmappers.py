from flask import flash
from flask_crud.dbutil import DBController, DBMapper
import json

class AddOrUpdateVehiculo(DBMapper):
    dbmapper_name = "add-or-update-vehiculo"

    @staticmethod
    def operation(form):
        try:
            DBController.insertUpdateOne("vehiculo", "matricula", form)
            flash("Vehiculo registrado con éxito", "success")
        except Exception as e:
            flash(str(e), "warning")

class RegistrarClienteYCompraVehiculos(DBMapper):
    dbmapper_name = "registra cliente y compra de vehiculos"
    @staticmethod
    def operation(form):
        selecteds = json.loads(form["selecteds"])
        client = dict(form)
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

class VehiculosALaVenta(DBMapper):
    """
    Obtiene todos los vehiculos que no han sido registrados en ventas
    """
    dbmapper_name = "vehiculos a la venta"
    @staticmethod
    def operation(_):
        # Obtener todos los vehiculos que no han sido registrados en ventas
        return DBController.query(
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

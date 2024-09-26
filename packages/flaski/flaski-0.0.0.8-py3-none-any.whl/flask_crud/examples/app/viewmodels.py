from flask_crud.manage import CrudRegistrable
from app.config.viewmodelconfig import cancel_btn, main_btn, delete_btn

class ImplDefaultPosRenderView:
    @staticmethod
    def posRenderView(view):
        view.form.main_btn = main_btn
        view.form.cancel_btn = cancel_btn
CrudRegistrable.posRenderView = ImplDefaultPosRenderView.posRenderView

# START:INGRESO
class IngresoVehiculoViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "view-registro-vehiculo"
    enums = {
        "tipo_vehiculo":[
            "PESADO",
            "MEDIANO",
            "LIVIANO"
        ]
    }
    requireds = "matricula,marca,modelo,tipo_vehiculo,color,precio_de_venta".split(",")
    def __init__(self, matricula="", marca="", modelo="", tipo_vehiculo="SELECCIONE:",  color="", precio_de_venta=9.76) -> None:
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.tipo_vehiculo = tipo_vehiculo
        self.color = color
        self.precio_de_venta = precio_de_venta

    def __str__(self) -> str:
        return f"{self.matricula} | {self.marca} | {self.modelo} | {self.color}"
    
class SalesVehiculoViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "SalesVehiculoViewCfg"    
    # requireds = "matricula,marca,modelo,tipo_vehiculo,color,precio_de_venta".split(",")
    def __init__(self, marca="", modelo="",color="", precio_de_venta=9.76, cantidad_disponible=5) -> None:
        self.marca = marca
        self.modelo = modelo
        self.color = color
        self.precio_de_venta = precio_de_venta
        self.cantidad_disponible = cantidad_disponible

    def __str__(self) -> str:
        return f"{self.matricula} | {self.marca} | {self.modelo} | {self.color}"


class IngresoClienteViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "IngresoClienteViewCfg"
    requireds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    # disableds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    enums = {
        "ciudad": ["PORTOVIEJO", "MANTA", "CHONE"],
    }
    def __init__(self, numero_de_cedula="1301347618", nombres="", apellidos="", dirección="", ciudad="SELECCIONE:", telefono="0998826188") -> None:
        self.numero_de_cedula = numero_de_cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.dirección = dirección
        self.ciudad = ciudad
        self.telefono = telefono


class RevisionViewCfg(CrudRegistrable):
    table_name = "revisiones"           # Nombre de la tabla en la base de datos
    id_name = "id"            # Nombre de la columna del ID en la tabla
    entity_name = "revision"           # Nombre de la entidad para uso en la lógica de negocio    
    enums = {
        "tipo_mantenimiento":["cambio de frenos", "cambio de aceite", "cambio de filtro"]
    }

    def __init__(self, fecha_hora_recepcion="2024-09-22 14:30", fecha_hora_entrega="2024-09-22 14:30", tipo_mantenimiento="SELECCIONE:") -> None:
        self.fecha_hora_recepcion = fecha_hora_recepcion
        self.fecha_hora_entrega = fecha_hora_entrega
        self.tipo_mantenimiento = tipo_mantenimiento
# END:INGRESO
class VehiculoCompradoViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "VehiculoCompradoViewCfg"
    def __init__(self, matricula="", marca="", modelo="", color="") -> None:
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.color = color

    def __str__(self) -> str:
        return f"{self.matricula} | {self.marca} | {self.modelo} | {self.color}"

class ClienteConsultaViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "ClienteConsultaViewCfg"
    requireds = ["numero_de_cedula"]
    # disableds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    def __init__(self, numero_de_cedula="1301347618") -> None:
        self.numero_de_cedula = numero_de_cedula

    @staticmethod
    def posRenderView(view):
        view.form.main_btn = main_btn.copyName("Consultar")
        view.form.cancel_btn = None

class VehiculoConsultaViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "VehiculoConsultaViewCfg"
    requireds = ["matricula"]
    # disableds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    def __init__(self, matricula="MAS-154") -> None:
        self.matricula = matricula

class MantenimientoEliminacionViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "MantenimientoEliminacionViewCfg"
    requireds = ["matrícula"]
    # disableds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    def __init__(self, matrícula="1301347618", motivo="\n") -> None:
        self.matrícula = matrícula
        self.motivo = motivo

    @staticmethod
    def posRenderView(view):
        view.form.main_btn = delete_btn.copyName("Dar de baja")
        view.form.cancel_btn = cancel_btn.copyName("Volver")

class RevisionViewCfg(CrudRegistrable):
    table_name = "revisiones"           # Nombre de la tabla en la base de datos
    id_name = "id"            # Nombre de la columna del ID en la tabla
    entity_name = "revision"           # Nombre de la entidad para uso en la lógica de negocio    
    enums = {
        "tipo_mantenimiento":["cambio de frenos", "cambio de aceite", "cambio de filtro"]
    }

    def __init__(self, fecha_hora_recepcion="2024-09-22 14:30", fecha_hora_entrega="2024-09-22 14:30", tipo_mantenimiento="SELECCIONE:") -> None:
        self.fecha_hora_recepcion = fecha_hora_recepcion
        self.fecha_hora_entrega = fecha_hora_entrega
        self.tipo_mantenimiento = tipo_mantenimiento
            

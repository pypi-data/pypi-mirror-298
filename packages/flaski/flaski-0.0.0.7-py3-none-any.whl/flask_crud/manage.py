from flask_crud.view import FormView, TableView, ViewConfig, ViewFactory

class EntityNotFoundError(Exception):
    """Excepción cuando una entidad no está registrada en CrudEntityStore."""

    def __init__(self, entity_name):
        super().__init__(f"Entidad '{entity_name}' no registrada en CrudEntityStore")

class IlegalArgumentOnEntityStore(Exception):
    """Excepción cuando un método de CrudEntityStore recibe un argumento no válido."""

    def __init__(self, name, value, cause=None):
        cause = '' if not cause else ' '+str(cause)
        super().__init__(f"El argumento '{ value}' no válido para parametro {name} en CrudEntityStore.{cause}")        

class ViewNotFoundError(Exception):
    """Excepción cuando una entidad no está registrada en CrudEntityStore."""

    def __init__(self, entity_name):
        super().__init__(f"View '{entity_name}' no registrada en CrudEntityStore")
        self.entity_name = entity_name

class FormNotFoundError(Exception):
    """Excepción cuando el metódo getForm no está implementado."""

    def __init__(self, entity_name):
        super().__init__(
            f"ViewConfig no implementado en clase con entity_name='{entity_name}'"
        )
        self.entity_name = entity_name

class CrudRegistrable:    
    """
    Clase CrudRegistrable para gestión CRUD en Flask.

    Rules of implementation:
    - La clase debe poder instanciarse sin necesidad de pasarle parámetros al método `__init__`.
    - Deben especificarse a nivel de clase los atributos: `table_name`, `id_name` y `entity_name`.

    Example:

    .. code-block:: python

        from flask_crud.manage import CrudRegistrable

        class ProductEntity(CrudRegistrable):
            table_name = "products"           # Nombre de la tabla en la base de datos
            id_name = "id_product"            # Nombre de la columna del ID en la tabla
            entity_name = "product"           # Nombre de la entidad para uso en la lógica de negocio
            enums = {
                "category": ["lacteo", "embutido", "hogar", "alimentos"],
            }
            requireds = ["category","name_product"]          # Campos requeridos
            enumsmuliple = ["category"]       # Campos que aceptan múltiples valores

            def __init__(self, name_product="", price=9.76, category="SELECCIONE:") -> None:
                self.name_product = name_product
                self.price = price
                self.category = category
                
        Enjoy :)!
    """
    __keys_crud_registrable = ["table_name", "id_name", "entity_name", "requireds", "enums"]
    table_name = "undefined"
    id_name = "undefined"
    entity_name = "undefined"        
    auto_view = True
    # Se almacenan nombres de columnas que el formulario debe marcar con "required"
    requireds = []
    # Se almacenan nombres de columnas que el formulario debe marcar con "disabled"
    disableds = []
    # Se almacenan los valores a mostrar en el combobox del form
    enums = {}    
    enumsmuliple = []    
    exclude = [id_name]

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)        
        # Aquí llamamos al CrudEntityStore para registrar la subclase
        CrudEntityStore.registerEntity(cls)
        # print(cls)
        data = vars(cls)
        dtinf = {key: data[key] for key in CrudRegistrable.__keys_crud_registrable if key in data}
        cls._str_registrable_crud =  lambda : str(dtinf)
        cls._str_registrable_model =  lambda self: str(vars(self))
        cls._sample_registrable_model =  lambda : vars(cls())
        if CrudRegistrable.auto_view:
            # Se implementan métodos para form 
            CrudEntityStore.registerViewFromEntity(cls)       

    @classmethod
    def allRequireds(cls, excludeFields=None):
        cls.requireds = []
        if excludeFields is None:
            excludeFields=[]
        for field in cls._sample_registrable_model():
            if field in excludeFields:
                continue
            cls.requireds.append(field)
        return cls.requireds

    @classmethod
    def allDisableds(cls, excludeFields=None):
        cls.disableds = []
        if excludeFields is None:
            excludeFields=[]
        for field in cls._sample_registrable_model():
            if field in excludeFields:
                continue
            cls.disableds.append(field)
        return cls.disableds

    @staticmethod
    def posRenderView(view):
        pass

class RenderDataHandler:

    @staticmethod
    def onFormData(data: dict[str], endpoint_name=None):
        view: ViewConfig = CrudEntityStore.getView()
        view.onFormData(data, endpoint_name=endpoint_name)

    @staticmethod
    def onTableData(data: list[dict[str]]):
        view: ViewConfig = CrudEntityStore.getView()
        view.onTableData(data)

    @staticmethod
    def onForm(form: FormView):
        view: ViewConfig = CrudEntityStore.getView()
        view.form = form

    @staticmethod
    def onTable(table: TableView):
        view: ViewConfig = CrudEntityStore.getView()
        view.table = table

    @staticmethod
    def toTemplateData():
        view: ViewConfig = CrudEntityStore.getView()
        return view.toTemplate()

class CrudEntityStore:
    __entities:dict[str, CrudRegistrable] = {}
    __views:dict[str,ViewConfig] = {}
    current_entity_name = None

    @staticmethod
    def registerEntity(entityClass):
        CrudEntityStore.__entities[entityClass.entity_name] = entityClass

    @staticmethod
    def registerView(entityView, entity_name=None):
        if not entity_name and not CrudEntityStore.current_entity_name:
            raise IlegalArgumentOnEntityStore(name="entity_name", value=entity_name, cause="Because current_entity_name=None.")
        entity_name = (
            entity_name if entity_name else CrudEntityStore.current_entity_name
        )
        CrudEntityStore.__views[entity_name] = entityView

    @staticmethod
    def registerViewFromEntity(entityClass):
        view = ViewConfig(
            form=ViewFactory.formFromEntity(entity_class=entityClass),
            table=ViewFactory.tableFromEntity(entity_class=entityClass),
        )
        CrudEntityStore.registerView(view, entity_name=entityClass.entity_name)

    @staticmethod
    def getEntity(entity_name=None):
        if not entity_name and not CrudEntityStore.current_entity_name:
            raise IlegalArgumentOnEntityStore(name="entity_name", value=entity_name)
        if isinstance(entity_name, CrudRegistrable):
            entity_name = entity_name.entity_name
        if not entity_name:
            entity_name = CrudEntityStore.current_entity_name
        current_entity = CrudEntityStore.__entities.get(entity_name)
        if current_entity:
            CrudEntityStore.current_entity_name = entity_name
            return current_entity
        raise EntityNotFoundError(entity_name=entity_name)

    @staticmethod
    def getViews():
        return CrudEntityStore.__views
    
    @staticmethod
    def getView(entity_name=None):
        if isinstance(entity_name, CrudRegistrable):
            entity_name = entity_name.entity_name
        if not entity_name and not CrudEntityStore.current_entity_name:
            raise IlegalArgumentOnEntityStore(name="entity_name", value=entity_name)
        if entity_name is None:
            entity_name = CrudEntityStore.current_entity_name
        current_entity_view = CrudEntityStore.__views.get(entity_name)
        if current_entity_view:
            CrudEntityStore.current_entity_name = entity_name
            return current_entity_view
        raise ViewNotFoundError(entity_name=entity_name)
    
    @staticmethod
    def executePosRenderViews():
        for entity_name, view in CrudEntityStore.getViews().items():
            entity = CrudEntityStore.getEntity(entity_name)
            entity.posRenderView(view)

    @staticmethod
    def check():
        for name_entity, entityClass in CrudEntityStore.__entities.items():
            print(f"´´´´´´´´´´´´´ VIEW {name_entity} ´´´´´´´´")
            print(CrudEntityStore.__views.get(name_entity))
            print(f"´´´´´´´´´´´´´ END VIEW {name_entity} ´´´´´´´´")
            print(f"{name_entity}.__str__")
            print(entityClass._str_registrable_crud())
            print(f"{name_entity}.__sample__")
            print(entityClass._sample_registrable_model())

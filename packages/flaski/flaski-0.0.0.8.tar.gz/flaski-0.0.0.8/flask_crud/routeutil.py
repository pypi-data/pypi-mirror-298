from flask import Blueprint

class Route:
    """
    Ejemplo de uso:
    .. code-block:: python
        from flask import redirect, url_for

        class IndexRoute(Route):
            blueprint = Blueprint("index", __name__)

            @blueprint.route("/")
            def index():
                return redirect(url_for("index.dashboard"))
            
            @blueprint.route("/dashboard")
            def dashboard():
                return "Dashboard"  # Ejemplo de renderización

    """
    _routes = []
    url_prefix = ""
    blueprint: Blueprint = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Registrar automáticamente la subclase al ser creada
        cls.register()

    @classmethod
    def to(cls, app):
        if cls.blueprint:
            app.register_blueprint(cls.blueprint, url_prefix=cls.url_prefix)

    @classmethod
    def register(cls):
        # Registrar la subclase en la lista de rutas
        Route._routes.append(cls)

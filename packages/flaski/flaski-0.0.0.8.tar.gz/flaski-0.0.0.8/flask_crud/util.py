import importlib
import pkgutil

def import_submodules(package_name):
    """Importa todos los submódulos de un paquete."""
    package = importlib.import_module(package_name)
    if hasattr(package, '__path__'):
        package_path = package.__path__
        for _, name, _ in pkgutil.iter_modules(package_path):
            full_name = f"{package_name}.{name}"
            importlib.import_module(full_name)
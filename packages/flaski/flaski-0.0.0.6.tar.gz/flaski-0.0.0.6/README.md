# Flask CRUD

`flask_crud` es una librería simple que permite la creación de operaciones CRUD (Create, Read, Update, Delete) en aplicaciones Flask con una interfaz de usuario amigable. Este proyecto incluye un sistema básico de gestión de entidades, que soporta categorías, edición y eliminación de registros, así como la capacidad de realizar búsquedas.

## Requisitos

- Python 3.x
- Flask

## Instalación

Primero, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/jrodre/flask_crud.git
cd flask_crud
```
Asegúrate de tener las dependencias necesarias instaladas:
```bash
pip install flask
```
## Extensión de funcionalidades
La librería permite registrar nuevas entidades de manera fácil, simplemente extendiendo la clase CrudRegistrable y definiendo los atributos necesarios.
```python
# model:
from flask_crud.manage import CrudRegistrable

class YourEntity(CrudRegistrable):
    table_name = "your_entity"
    id_name = "id_entity"
    entity_name = "entity"
    requireds = ["name", "category"]
    
    def __init__(self, name="", category="SELECCIONE:"):
        self.name = name
        self.category = category

```
## Contribución
Si quieres contribuir a este proyecto, por favor crea un fork, realiza tus cambios y abre un pull request.

## Licencia
Este proyecto está licenciado bajo los términos de la MIT License.

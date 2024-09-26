class DBMapperException(Exception):
    def __init__(self,*args):
        super().__init__(*args)
    
class DBMapper:
    """
    Registra operaciones(se espera que sean de base de datos) asociadas a una clave   
    Ejemplo de uso:
    .. code-block:: python
        from flask import flash
        from flask_crud.dbutil import DBController, DBMapper

        class AddOrUpdateVehiculo(DBMapper):
        dbmapper_name = "add-or-update-vehiculo"

        @staticmethod
        def operation(form):
            try:
                DBController.insertUpdateOne("vehiculo", "matricula", form)
                flash("Vehiculo registrado con éxito", "success")
            except Exception as e:
                flash(str(e), "warning")
    """
    _db_mappers = {}
    dbmapper_name = None

    @staticmethod
    def get(key_dbmapper, form:dict) -> list[dict[str]]:
        dbmapper = DBMapper._db_mappers.get(key_dbmapper)
        if dbmapper:
            return dbmapper(form)
        raise DBMapperException(f"No existe dbmapper con clave '{key_dbmapper}'")
    
    @staticmethod
    def getSimple(key_dbmapper) -> list[dict[str]]:
        dbmapper = DBMapper._db_mappers.get(key_dbmapper)
        if dbmapper:
            return dbmapper(None)
        raise DBMapperException(f"No existe dbmapper con clave '{key_dbmapper}'")
    
    @staticmethod
    def exec(key_dbmapper, form:dict):
        # print("DDDDDDDDDDDDDDDDDDDD BBBBBBBBBBBBBBBBB DBMapper.__db_mappers")
        # print(DBMapper._db_mappers)
        dbmapper = DBMapper._db_mappers.get(key_dbmapper)
        print(dbmapper)
        if dbmapper is None:
            raise DBMapperException(f"No existe dbmapper con clave '{key_dbmapper}'")
        if "function" not in str(dbmapper):
            raise DBMapperException(f"Valor de dbmmaper con clave '{key_dbmapper}'. El dbmapper debe ser una funcion o metodo")
        dbmapper(form)
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Registrar automáticamente la subclase al ser creada
        cls.register()

    @staticmethod
    def operation(form):
        pass

    @classmethod
    def register(cls):
        if not cls.dbmapper_name:
            raise DBMapperException(f"{cls.__name__}(DBMapper).dbmapper_name no puede tener valor '{cls.dbmapper_name}'")
        if cls.dbmapper_name in DBMapper._db_mappers:
            raise DBMapperException(f"{cls.__name__}(DBMapper).dbmapper_name = '{cls.dbmapper_name}' ya está registrado en dbmappers.")
        # Registrar la subclase en la lista de rutas
        DBMapper._db_mappers[cls.dbmapper_name] = cls.operation

class DBController:
    mysql = None

    @staticmethod
    def checkMySQL():
        if not DBController.mysql:
            raise Exception("Asigne una instancia de MySQL a DBController.")
        return DBController.mysql

    @staticmethod
    def getColnames(table_name):
        mysql = DBController.checkMySQL()
        cursor = mysql.connection.cursor()
        query = f"SELECT * FROM {table_name} LIMIT 1"
        cursor.execute(query)
        column_names = [desc[0] for desc in cursor.description]
        return column_names

    @staticmethod
    def dict_fetch(cursor, one=False):
        """Convierte el resultado del cursor en un diccionario o lista de diccionarios"""
        columns = [col[0] for col in cursor.description]

        if one:
            row = cursor.fetchone()
            return dict(zip(columns, row)) if row else None
        else:
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def all(nametable):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            cursor.execute(f"SELECT * FROM {nametable}")
            result = DBController.dict_fetch(cursor)
            return result
        except Exception as e:
            raise Exception(f"Error al cargar TODOS los datos: {str(e)}")
        finally:
            cursor.close()

    @staticmethod
    def query(query, args: tuple):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            cursor.execute(query, args)
            result = DBController.dict_fetch(cursor, one=False)
            return result
        except Exception as e:
            raise Exception(f"Error al cargar los datos: {str(e)}")
        finally:
            cursor.close()

    @staticmethod
    def queryOne(query, args: tuple):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            cursor.execute(query, args)
            result = DBController.dict_fetch(cursor, one=True)
            return result
        except Exception as e:
            raise Exception(f"Error al cargar los datos: {str(e)}")
        finally:
            cursor.close()

    @staticmethod
    def execute(query, args: tuple):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            result = cursor.execute(query, args)
            result = mysql.connection.commit()
            return result
        except Exception as e:
            msg = f"Error durante actualización de datos: {str(e)}"
            raise Exception(msg)
        finally:
            cursor.close()

    @staticmethod
    def insert(table_name, form):
        try:                
            colnames = [field for field in form]
            marks = "%s," * len(form)
            marks = marks.rstrip(",")  # Elimina la última coma
            values = [str(form[field]) for field in form]
            query = "INSERT INTO {0}({1}) VALUES ({2})".format(table_name, ",".join(colnames), marks)
            # return query
            DBController.execute(query, tuple(values))
        except Exception as e:
            raise Exception(e)
        
    @staticmethod
    def update(table_name, where, vals, form):
        try:                
            assings = [field+"=%s" for field in form]
            values = [str(form[field]) for field in form]
            query = "UPDATE {0} SET {1} WHERE {2}".format(table_name, ",".join(assings), where)
            values = *tuple(values), *vals
            # return query+": "+str(values)
            # return query
            DBController.execute(query, tuple(values))
        except Exception as e:
            raise Exception(e)
        
    @staticmethod
    def insertUpdateOne(table_name, name_field, form):
        try:                
            try:                
                DBController.insert(table_name=table_name, form=form)
            except Exception:
                DBController.updateOne(table_name=table_name, name_field=name_field, form=form)                
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def updateOne(table_name, name_field, form):
        try:                
            assings = [field+"=%s" for field in form]
            values = [str(form[field]) for field in form]
            query = "UPDATE {0} SET {1} WHERE {2}=%s ".format(table_name, ",".join(assings), name_field)
            values = *tuple(values), form[name_field]
            DBController.execute(query, tuple(values))
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def delete(query, args: tuple):
        try:
            mysql = DBController.checkMySQL()
            cursor = mysql.connection.cursor()
            result = cursor.execute(query, args)
            result = mysql.connection.commit()
            return result
        except Exception as e:
            msg = f"Error al eliminar los datos: {str(e)}"
            raise Exception(msg)
        finally:
            cursor.close()


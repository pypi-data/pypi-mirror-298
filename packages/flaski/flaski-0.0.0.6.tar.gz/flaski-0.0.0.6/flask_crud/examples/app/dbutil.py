
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


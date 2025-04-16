import mysql.connector
from mysql.connector import Error
#clase que se encargara de comunicarse con la base de datos

class baseDatos():
    #la conexion con la base de datos se realiza una sola vez, en el constructor del objeto


    
    #funcion para buscar datos en la base de datos
    def buscar(self, tabla: str, columnas = '*', condiciones=None):
        
        #en cada funcion de la clase, se realizara la conexion al incio con la base de datos
        try:
            conexion = mysql.connector.connect(host="db-competencias.c3u4i2g2yefp.us-east-2.rds.amazonaws.com",
                                        user="admin",
                                            password="Juanpablo123",
                                            port=3306,
                                            database="trabajo")
            print("✅ Conexión exitosa")
            cursor = conexion.cursor()
        except mysql.connector.Error as err:
            print("Error al conectar:", err)
            return

        #se comprueba si hay mas de una columna a seleccionar. en caso de haberlo, se transforma la lista a cadena
        if isinstance(columnas, list):
            columnas = ", ".join(columnas)

        #se arma la consulta base
        sql = f"select {columnas} from {tabla}"

        #si hay condiciones, estos se agregan a la consulta usando marcadores de posicion para mas seguridad
        if condiciones:

            filtros = [f"{con} = %s" for con in condiciones]

            sql += " where " + "and ".join(filtros)

            valores = list(condiciones.values())

            try:
                cursor.execute(sql, valores)
                resultado = cursor.fetchall()
                return resultado
            except Error as e:
                print("error al realizar la busqueda " + str(e))
                return []
            except Exception as e:
                print("ocurrio un error al realizar la busqueda " + str(e))
                return []
            finally:
                conexion.close()

        #se ejecuta la consulta y se devuelve el valor, manejando las posibles exepciones que puedan saltar
        try:
            cursor.execute(sql)
            resultado = cursor.fetchall()
            return resultado
        except Error as e:
            print("error al realizar la busqueda " + str(e))
            return []
        except Exception as e:
            print("ocurrio un error al realizar la busqueda " + str(e))
            return []
        finally:
            conexion.close()
        
    #funcion dedicada a insertar datos en la base de datos

    def insertar(self, tabla: str, valores: list, columnas = []):
         
         #se comprueba la conexion
        try:
            conexion = mysql.connector.connect(host="db-competencias.c3u4i2g2yefp.us-east-2.rds.amazonaws.com",
                                        user="admin",
                                            password="Juanpablo123",
                                            port=3306,
                                            database="trabajo")
            print("✅ Conexión exitosa")
            cursor = conexion.cursor()
        except mysql.connector.Error as err:
            print("Error al conectar:", err)
            return
        #verifica si se quiere especificar las columnas
        if len(columnas) != 0:
            #se construye la consulta
            sql = f"insert into {tabla}(" + ", ".join(columnas) + ")"

           

            lista_valores = [f"%s" for i  in range(len(valores))]

            sql = sql + " values(" +  ", ".join(lista_valores)

            sql += ")"
           
            #se ejecuta la consulta, con su respectivo manejo de errores
            try:
                cursor.execute(sql, valores)
                conexion.commit()
                return True
            except Error as e:
                print("error al realizar la insercion " + str(e))
                return []
            except Exception as e:
                print("ocurrio un error al realizar la insercion " + str(e))
                return []
            finally:
                conexion.close()

        #este bloque es igual al anterior, solo que sin incluir las columnas
        else:
            sql = f"insert into {tabla}"

            lista_valores = [f"%s" for i  in range(len(valores))]

            sql = sql + " values(" +  ", ".join(lista_valores) + ")"
            print(sql)

            try:
                cursor.execute(sql, valores)
                return True
            except Error as e:
                print("error al realizar la insercion " + str(e))
            except Exception as e:
                print("ocurrio un error al realizar la insercion " + str(e))
            finally:
                conexion.close()
        return 
    
    #funcion que actualiza 
    def actualizar(self, tabla: str, condiciones : dict, columna_valor : dict):

        try:
            conexion = mysql.connector.connect(host="db-competencias.c3u4i2g2yefp.us-east-2.rds.amazonaws.com",
                                        user="admin",
                                            password="Juanpablo123",
                                            port=3306,
                                            database="trabajo")
            print("✅ Conexión exitosa")
            cursor = conexion.cursor()
        except mysql.connector.Error as err:
            print("Error al conectar:", err)
            return


        sql = f"update {tabla} set "

        columnas = [f"{con} = %s" for con in columna_valor.keys()]

        sql += ", ".join(columnas)

        if len(condiciones) != 0:

            condiciones_lista = [f"{con} = %s" for con in condiciones.keys()]

            sql += "where " + "and ".join(condiciones_lista)

            valores_condiciones = list(condiciones.values())

            valores_update = list(columna_valor.values())

            valores = valores_update + valores_condiciones

            try:
                cursor.execute(sql, valores)
                conexion.commit()
                return True
            except Error as e:
                print("error al realizar la insercion " + str(e))
            except Exception as e:
                print("ocurrio un error al realizar la insercion " + str(e))
            finally:
                conexion.close()

        valores_update = list(columna_valor.values())

        try:
            cursor.execute(sql, valores_update)
            conexion.commit()
            return True
        except Error as e:
            print("error al realizar la actualizacion " + str(e))
        except Exception as e:
            print("ocurrio un error al realizar la actualizacion " + str(e))
        finally:
                conexion.close()

        return 
    
    def eliminar(self, tabla: str, condiciones : dict):

        try:
            conexion = mysql.connector.connect(host="db-competencias.c3u4i2g2yefp.us-east-2.rds.amazonaws.com",
                                        user="admin",
                                            password="Juanpablo123",
                                            port=3306,
                                            database="trabajo")
            print("✅ Conexión exitosa")
            cursor = conexion.cursor()
        except mysql.connector.Error as err:
            print("Error al conectar:", err)
            return
    

        sql = f"delete from {tabla} where "

        condiciones_lista = [f"{con} = %s" for con in condiciones.keys()]

        sql += "and ".join(condiciones_lista)

        valores = list(condiciones.values())

        try:
            cursor.execute(sql, valores)
            conexion.commit()
            return True
        except Error as e:
            print("error al realizar la actualizacion " + str(e))
        except Exception as e:
            print("ocurrio un error al realizar la actualizacion " + str(e))
        finally:
                conexion.close()

        return
    


prueba = baseDatos()

print(prueba.buscar("productos", condiciones={"id_producto" : 1}))
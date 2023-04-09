import mysql.connector #Con esto tenemos acceso a la biblioteca de mysql
import os # Modulo para obtener las rutas
import subprocess
import datetime


#Creamos un diccionario con los datos de conexion

acceso_bd = {"host" : "localhost",
             "user" : "root",
             "password" : "Motorola12.warwick",
             "database" : "florentina_store"
             }

# --> Rutas

# Obtenemos la raiz de la carpeta del proyecto
carpeta_principal = os.path.dirname(__file__)

carpeta_respaldo = os.path.join(carpeta_principal, "respaldo")
print(carpeta_respaldo)

# --> Clases

class BaseDatos:
    def __init__(self, **kwargs):
        self.conector = mysql.connector.connect(**kwargs) # Conectamos a la BD
        self.cursor = self.conector.cursor() # Creamos el cursor
        self.host = kwargs["host"]
        self.usuario = kwargs["user"]
        self.contraseña = kwargs["password"]
        self.conexion_cerrada = False # Si esta en False significa que no esta cerrada
        print("Se abrio la conexion con el servidor.")
        
        
    # Decoradora para el reporte de bases de datos del servidor
    def reporte_db(fun_externa):
        def fun_interna(self, nombre_bd):
            fun_externa(self, nombre_bd)
            BaseDatos.mostrar_bd(self) # hay que hacer referencia a la clase que pertene el metodo para que nos de el alcance
        return fun_interna
    
    
    # Decorador para cerrar el cursor y la conexion con la base de datos
    def conexion(funcion_externa):
        def fun_interna(self, *args, **kwars):
            try:
                if self.conexion_cerrada:
                    # Si la conexion esta cerrada, lo volvemos a conectar
                    self.conector = mysql.connector.connect(
                        host = self.host,
                        user = self.usuario,
                        password = self.contraseña
                    )
                    # Volvemos a crear el cursor
                    self.cursor = self.conector.cursor()
                    # Indicamos al programa que la conexion esta abierta de nuevo
                    self.conexion_cerrada = False
                    print("Se abrio la conexion con el servidor.")
                    
                # Se llama a la funcion externa, tiene que estar dentro del try no del if, porque si la conexion esta abierta no hace falta abrirla con el if
                funcion_externa(self, *args, **kwars)
            except Exception as e:
                # Se informa de un error en la llamada
                print(f"Ocurrio un error: {e}")
                # Propago la excepcion
                raise e
            finally:
                if self.conexion_cerrada:
                    pass
                else:
                    # Cerramos el cursor y la conexion
                    self.cursor.close()
                    self.conector.close()
                    print("Se cerro la conexion con el servidor")
                    self.conexion_cerrada = True
            return self.resultado
        return fun_interna
    
    
    # Decorador para comprobar la base de datos
    def comprueba_db(funcion_externa):
        def funcion_interna(self, nombre_db, *args):
            # Primero se verifica si la base de datos existe
            sql = f"SHOW DATABASES LIKE '{nombre_db}'"
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            
            # Ejecuta la funcion decorada y devuelve el resultado
            return funcion_externa(self, nombre_db, *args)
        return funcion_interna
        
        
    # Consultas generales
    @conexion
    def consulta(self, sql):
        self.cursor.execute(sql)
        self.resultado = self.cursor.fetchall()

    # Muestra las bases de datos del servidor
    @conexion
    def mostrar_bd(self):
        self.cursor.execute("SHOW DATABASES")
        self.resultado = self.cursor.fetchall()
    
    
    # Borra base de datos
    @conexion
    @reporte_db
    @comprueba_db
    def borrar_bd(self, nombre_bd):
        self.cursor.execute(F"DROP DATABASE {nombre_bd}")

            
    # Crear base de datos 
    @conexion
    @reporte_db
    def crear_db(self,nombre_bd):
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nombre_bd}")

            
            
    #Crear backups de bases de datos
    @conexion
    @comprueba_db
    def copia_bd(self, nombre_bd):
        # Obetiendo la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            
        with open(f'{carpeta_respaldo}/{nombre_bd}_{fecha_actual}.sql', 'w') as out:
            subprocess.Popen(f'"C:/Program Files/MySQL/MySQL Workbench 8.0/"mysqldump --user=root --password={self.contraseña} --databases {nombre_bd}', shell=True, stdout=out)
        print(f"La copia de base de datos{ nombre_bd} se creo correctamente. Fecha {fecha_actual}")
        
    
    # Crear tablas, el argumento columna es una lista con diccionarios
    @conexion
    @comprueba_db
    def crear_tabla(self, nombre_bd, nombre_tabla, columnas):
        try:
            #String para guardar el string con las columnas y tipos de datos
            columnas_string = ""
            
            #Se itera la lista que se le pasa como argumento (cada diccionario)
            for columna in columnas:
                #formamos el string con nombre, tipo y longitud
                columnas_string += f"{columna['name']} {columna['type']}({columna['length']})"
                #Si es clave primaria, auto_increment o no adminte valores nulos, lo añade al string
                if columna['primary_key']:
                    columnas_string += " PRIMARY KEY"
                if columna['auto_increment']:
                    columnas_string += " AUTO_INCREMENT"
                if columna['not_null']:
                    columnas_string += " NOT NULL"
                #Hace un salto de línea después de cada diccionario    
                columnas_string += ",\n"
                
            #Elimina al final del string el salto de línea y la coma    
            columnas_string = columnas_string[:-2]
            #Le indica que base de datos utilizar
            self.cursor.execute(f"USE {nombre_bd}")
            
            #Se crea la tabla juntando la instrucción SQL con el string generado
            sql = f"CREATE TABLE {nombre_tabla} ({columnas_string});"
            #Se ejecuta la instrucción
            self.cursor.execute(sql)
            
            #Se hace efectiva
            self.conector.commit()
            
            print(f"Se creo la tabla {nombre_tabla} correctamente.")
        except:
            print(f"Ocurrio un error al intentar crear la tabla {nombre_tabla}.")
    
    
    @conexion
    @comprueba_db
    def borrar_tabla(self, nombre_db, nombre_tabla):
        try:
            self.cursor.execute(f"USE {nombre_db}")
            self.cursor.execute(f"DROP TABLE {nombre_tabla}")
            print(f"La tabla {nombre_tabla} se borro correctamente de la base de datos {nombre_db}.")
        except:
            print(f"La tabla {nombre_tabla} no se pudo eliminar de la base de datos {nombre_db}")
    
    
    @conexion
    @comprueba_db
    def mostrar_tablas(self, nombre_db):
        # Se selecciona la base de datos
        self.cursor.execute(f"USE {nombre_db};")
        # Realiza la consulta para mostrar las tablas de la base de datos actual
        self.cursor.execute("SHOW TABLES")
        resultado = self.cursor.fetchall()
        #Evalúa si no hay tablas en la base de datos
        if resultado == []:
            print(f"No hay tablas en la base de datos '{nombre_db}'.")
            return
       # Se informa de que se están obteniendo las tablas
        print("Aquí tienes el listado de las tablas de la base de datos:")
        # Recorre los resultados y los muestra por pantalla
        for tabla in resultado:
            print(f"-{tabla[0]}.")
    
    
    @conexion
    @comprueba_db
    def mostrar_columnas(self, nombre_db, nombre_tabla):
        # Se selecciona la base de datos
        self.cursor.execute(f"USE {nombre_db};")
        try:
            # Realizamos la consulta para mostrar las columnas de la tabla especificada
            self.cursor.execute(f"SHOW COLUMNS FROM {nombre_tabla};")
            resultado = self.cursor.fetchall()
            #print(resultado)
            print(f"Aqui tiene el listado de columnas de la tabla {nombre_tabla}")
            
            # Recorremos el resultado con bucle for y operaciones ternarias, toda la info de las columna esta en la variable resultado
            for columna in resultado:
                not_null = "No admite valores nulos." if columna[2] == "NO" else "Admite valores nulos."
                primary_key = "Es clave primaria." if columna[3] == "PRI" else ""
                foreign_key = "Es clave externa." if columna[3] == "MUL" else ""
                print(f"-{columna[0]} ({columna[1]}) {not_null} {primary_key} {foreign_key}")
                
        except:
            print("Ocurrio un error, compruebe que el nombre de la tabla sea el correcto.")
            
    
    @conexion
    @comprueba_db
    def insertar_registro(self, nombre_bd, nombre_tabla, registro):
        self.cursor.execute(f"USE {nombre_bd}")

        if not registro:  # Si la lista está vacía
            print("La lista de registro está vacía.")
            return

        # Obtener las columnas y los valores de cada diccionario
        columnas = []
        valores = []
        for registro in registro:
            columnas.extend(registro.keys())
            valores.extend(registro.values())

        # Convertir las columnas y los valores a strings
        columnas_string = ''
        for columna in columnas:
            columnas_string += f"{columna}, "
        columnas_string = columnas_string[:-2]  # Quitar la última coma y espacio

        valores_string = ''
        for valor in valores:
            valores_string += f"'{valor}', "
        valores_string = valores_string[:-2]  # Quitar la última coma y espacio

        # Crear la instrucción de inserción
        sql = f"INSERT INTO {nombre_tabla} ({columnas_string}) VALUES ({valores_string})"
        self.cursor.execute(sql)
        self.conector.commit()
        print("Registro añadido a la tabla.")
        
        
    # Metodo para eliminar registros con una condicion
    @conexion
    @comprueba_db 
    def eliminar_registro(self, nombre_db, nombre_tabla, condicion):
        try:
            self.cursor.execute(f"USE {nombre_db}")
            # Se crea a instrucion sql para eliminar
            sql = f"DELETE FROM {nombre_tabla} WHERE {condicion}"
            # Se ejecuta y confirma
            self.cursor.execute(sql)
            self.conector.commit()
            print("Registros eliminados.")
        except:
            print("Error al intentar borrar registros en la tabla.")
    
    
    # Método para borrar todos los registros de una tabla
    @conexion
    @comprueba_db
    def vaciar_tabla(self, nombre_db, nombre_tabla):
        try:
            self.cursor.execute(f"USE {nombre_db}")
            # Se borran todos los registros de una tabla
            sql = f"TRUNCATE TABLE {nombre_tabla}"
            self.cursor.execute(sql)
            self.conector.commit()
            print("Se han borrado todos los registros de la tabla.")
        except:
            print("Error al intentar borrar los registros de la tabla.")
    
    
    # Método para actualizar registros en una tabla
    # por ej: base_datos.actualizar_registro("pruebas", "usuarios", "apellidos = 'Barros Fernández',
    # direccion = 'Avenida de las ilusiones nº 7'", "nombre = 'Enrique';")
    @conexion
    @comprueba_db
    def actualizar_registro(self, nombre_db, nombre_tabla, columnas, condiciones):
        try:
          	# Se selecciona la base de datos
            self.cursor.execute(f"USE {nombre_db}")

            # Crear la instrucción de actualización
            sql = f"UPDATE {nombre_tabla} SET {columnas} WHERE {condiciones}"
            # Se ejecuta la instrucción de actualización y se hace efectiva
            self.cursor.execute(sql)
            self.conector.commit()
            print("Se actualizó el registro correctamente.")
        except:
            print("Ocurrió un error al intentar actualizar el registro.")
        
        
        
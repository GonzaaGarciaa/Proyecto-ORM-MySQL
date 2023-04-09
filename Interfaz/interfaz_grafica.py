import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import tkinter as tk
from tkinter.font import BOLD
from PIL import Image
import bd.base_dato as sqlbd

# Configuraciones globales para la aplicacion

# ---> Rutas

# Carpeta principal
carpeta_principal = os.path.dirname(__file__)
#.\proyecto-bd\bd\interfaz
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")
#.\proyecto-bd\bd\interfaz\Imagenes

# Objeto para manejar bases de datos MySQL
base_datos = sqlbd.BaseDatos(**sqlbd.acceso_bd)

# Modo de color y tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#  Fuentes del programa
fuente_windgets = ('Raleway', 16, BOLD)

class Login():
    def __init__(self):
        # Creacion de la ventana principal
        self.root = ctk.CTk() # Instancia
        self.root.title("Programacion Facil - Proyecto de bases de datos") # Titulo
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico")) # Icono
        self.root.geometry("400x500") # Tamaño ventana
        self.root.resizable(False,False) # Bloquedo de redimencion de la ventana en alto y largo
        
        # Contenido de la ventana principal
        # Logo
        logo = ctk.CTkImage(
            light_image = Image.open((os.path.join(carpeta_imagenes, "logo_claro.png"))), # Imagen modo claro
            dark_image = Image.open((os.path.join(carpeta_imagenes, "logo_oscuro.png"))), # Imagen modo oscuro
            size  = (250, 250) # Tamaño de las imagenes
        )
        
        # Etiqueta para mostrar la imagen
        etiqueta = ctk.CTkLabel(master = self.root, image=logo, text="")
        etiqueta.pack(pady=15)
        
        # Campo de texto
        # Usuario
        ctk.CTkLabel(self.root, text="Usuario").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Ej:Laura")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack()
        
        # Contraseña
        ctk.CTkLabel(self.root, text="Contraseña").pack()
        self.contraseña = ctk.CTkEntry(self.root)
        self.contraseña.insert(0, "*********")
        self.contraseña.bind("<Button-1>", lambda e: self.contraseña.delete(0, 'end'))
        self.contraseña.pack()
        
        # Boton
        ctk.CTkButton(self.root, text="Entrar", command=self.validar).pack(pady=10)
        
        # Bucle de ejecucion
        self.root.mainloop()
    
    # Función para validar el login
    def validar(self):
        obtener_usuario = self.usuario.get() # Obtenemos el nombre de usuario
        obtener_contrasena = self.contraseña.get() # Obtenemos la contraseña
        
        # Verifica si el valor que tiene el usuario o la contraseña o ambos no coinciden
        if obtener_usuario == sqlbd.acceso_bd["user"] or obtener_contrasena == sqlbd.acceso_bd["password"]:
            # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo remplaza
            if hasattr(self, "info_login"):
                self.info_login.configure(text="Usuario o contraseña incorrectos.")
            # Crea esta etiqueta siempre que el login sea incorrecto
            else:
                self.info_login = ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectos.")
                self.info_login.pack()
        else:
            # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo remplaza
            if hasattr(self, "info_login"):
                self.info_login.configure(text=f"Hola, {obtener_usuario}. Espere unos instantes...")
            else:
                # Crea esta etiqueta siempre que el login sea correcto
                self. info_login = ctk.CTkLabel(self.root, text=f"Hola, {obtener_usuario}. Espere unos instantes...")
                self.info_login.pack()
                self.root.destroy()
            
            # Se instancia la ventana de opciones
            ventana_opciones = VentanaOpciones()


class FuncionesPrograma():
    def ventana_consultaSQL(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana de consultas sql")
        # Pone el foco en la ventana
        ventana.grab_set()
        
        # Creaoms el frame y lo agregamos a la ventana
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=10, pady=10)
        
        # Crea el entry y establece su tamaño a 300px de ancho
        self.entrada = ctk.CTkEntry(marco, width=300)
        # Establece un valor personalizado de fuente
        self.entrada.configure(font=fuente_windgets)
        self.entrada.grid(row=0, column=0, pady=10)
        
        # Metodo para utilizar la logica del metodo consulta de base de datos.py
        def procesar_datos():
            try:
                # Borra el contenido de la caja de resultados
                self.texto.delete('1.0', 'end')
                # Obtiene el contenido del entry
                datos = self.entrada.get()
                # Llama al metodo base_datos.consulta() con los datos como argumento
                resultado = base_datos.consulta(datos)
                for registro in resultado:
                    self.texto.insert('end', registro)
                    self.texto.insert('end', '\n')
                # Actualiza el contador de registros devueltos
                numero_registros = len(resultado) # Lo contamos con len porque fetchall devuelve una lista con tuplas
                self.contador_registros.configure(text=f"Registros devueltos: {numero_registros}")
            except Exception:
                self.contador_registros.configure(text="Hay un error en tu consulta SQL. Porfavor, revisela.")
                CTkMessagebox(title="Error", message="Hay un error en tu consulta SQL. Porfavor, revisela.", icon="cancel")
                
        # Crea el boton de envio
        boton_envio = ctk.CTkButton(marco, text="Enviar",command=lambda : procesar_datos())
        boton_envio.grid(row=0, column=1)
        
        # Crea boton de borrado
        boton_borrar = ctk.CTkButton(marco, text="Borrar", command=self.limpiar_texto)
        boton_borrar.grid(row=0, column=2)
        
        # Creamos el widget de texto
        self.texto = ctk.CTkTextbox(marco, width=610, height=300)
        self.texto.grid(row=1, column=0, columnspan= 3, padx=10, pady=10)
        
        # Agregamos un widget label para mostrar el numero de registros devueltos
        self.contador_registros = ctk.CTkLabel(marco, text="Registros devultos: 0")
        self.contador_registros.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        
    # Funcion limpiar texto
    def limpiar_texto(self):
        # Borra todo el contenido del widget Text
        self.texto.delete('1.0', 'end') # 1.0 signidica desde fila 1 y columna 0
        
    
    def ventana_mostrar_bd(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar base de datos")
        ventana.geometry("480x565")
        # Se evita su redimension
        ventana.resizable(0,0)
        ventana.grab_set()
        
        # Se crea el marco principal
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=5, pady=5)
        
        # Etiqueta informativa para la ventana
        ctk.CTkLabel(marco, text="Listado de las bases de datos en el servidor",
        font=fuente_windgets).pack(padx=10, pady=10)
        
        # Agregar un campo de entrada para la busqueda
        self.busqueda_control = tk.StringVar()
        
        # Se crea la entrada de texto para busquedas
        ctk.CTkEntry(marco,
                    font=fuente_windgets,
                    textvariable=self.busqueda_control,
                    width=300).pack(padx=10)
        
        # Creamos caja de texto
        self.texto = ctk.CTkTextbox(marco, font=fuente_windgets, width=430, height=300)
        self.texto.pack(padx=10, pady=10)
        
        # Se crea una etiqueta para mostras el numero de resultados
        self.resultado_label = ctk.CTkLabel(marco, text="", font=fuente_windgets)
        self.resultado_label.pack(pady=10)
        
        # Creamos marco para lo botones
        marco_botones = ctk.CTkFrame(ventana)
        marco_botones.pack(padx=5, pady=5)
        
        
        # Función interna de actualización SHOW DATABASES
        def actualizar():
            # Se establece el valor de la variable de control a string vacío (reset)
            self.busqueda_control.set('')
            # Se elimina el contenido de la caja de resultados
            self.texto.delete('1.0', 'end')
            # Se realiza la llamada al método mostrar_bd (SHOW DATABASES) y se guarda en resultado
            resultado = base_datos.mostrar_bd()
            # Se itera el resultado y se presenta línea a línea en la caja de texto. 
            for bd in resultado:
                self.texto.insert('end', f"-{bd[0]}\n")
            
            # Se evalúa el resultado para deteminar la frase singular o plural
            numero_resultados = len(resultado)
            if numero_resultados == 1:
                self.resultado_label.configure(text=f"Se encontró {numero_resultados} resultado.")
            else:
                self.resultado_label.configure(text=f"Se encontraron {numero_resultados} resultados.")
        
       
        def buscar():
            # Se elimina el contenido de la caja de resultados
            self.texto.delete('1.0', 'end')
            # Se realiza la llamada al método mostrar_bd (SHOW DATABASES) y se guarda en resultado 
            resultado = base_datos.mostrar_bd()
            # Se obtiene el valor string de la variable de control (lo que se busca en el Entry())
            busqueda = self.busqueda_control.get().lower()
            
            # Se crea una lista vacía donde almacenar los resultados filtrados
            resultado_filtrado = []
            # Se itera la tupla fetchall.
            for bd in resultado:
                #Si lo que tiene la StringVar está en cada lista de la tupla, se añade a la lista
                if busqueda in bd[0]:
                    resultado_filtrado.append(bd)
            
            # Se itera la lista ya filtrada, con lo que se insertan los resultados en la caja de resultados
            for bd in resultado_filtrado:
                self.texto.insert('end', f"-{bd[0]}\n")
            
            # Se evalúa el resultado para deteminar la frase singular o plural
            numero_resultados = len(resultado_filtrado)
            if numero_resultados == 1:
                self.resultado_label.configure(text=f"Se encontró {numero_resultados} resultado.")
            else:
                self.resultado_label.configure(text=f"Se encontraron {numero_resultados} resultados.")
        
               
        def creando_bd():
            try:
                # Se elimina el contenido de la caja de resultados
                self.texto.delete('1.0', 'end')
                busqueda = self.busqueda_control.get().lower()
                # Se realiza la llamada al método borrar_bd (DROP DATABASE {nombre_bd}) y se guarda en resultado 
                base_datos.crear_db(f"{busqueda}")
                self.resultado_label.configure(text=f"{busqueda} se creo correctamente, o ya estaba creada.")
            except:
                self.resultado_label.configure(text=f"Ocurrio un error con la creacion de la base de datos.")
                CTkMessagebox(title="Error", message=f"Hay un error en los caracteres de la base de datos {busqueda}", icon="cancel")
        
              
        def borrando_bd():
            try:
                # Se elimina el contenido de la caja de resultados
                self.texto.delete('1.0', 'end')
                busqueda = self.busqueda_control.get().lower()
                # Se realiza la llamada al método borrar_bd (DROP DATABASE {nombre_bd}) y se guarda en resultado 
                base_datos.borrar_bd(f"{busqueda}")
                self.resultado_label.configure(text=f"La base de datos {busqueda} se borro correctamente.")
            except:
                self.resultado_label.configure(text=f"La base de datos {busqueda} no existe.")
                CTkMessagebox(title="Error", message=f"La base de datos {busqueda}, no existe.", icon="cancel")
        
        
        # Creando botones
        boton_buscar = ctk.CTkButton(marco_botones, text="Buscar", command=buscar)
        boton_buscar.grid(row=0, column=0, pady=10, padx=5)
        
        boton_crear = ctk.CTkButton(marco_botones, text="Crear", command=creando_bd)
        boton_crear.grid(row=0, column=1, pady=10, padx=5)
        
        boton_borrar = ctk.CTkButton(marco_botones, text="Borrar", command=borrando_bd)
        boton_borrar.grid(row=0, column=2, pady=10, padx=5)
        
        boton_actualizar = ctk.CTkButton(marco_botones, text="Actualizar", command=actualizar)
        boton_actualizar.grid(row=1, column=1, pady=10, padx=5)
        
        actualizar()
    
    
    def ventana_eliminar_bd(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar base de datos")
        ventana.geometry("450x600")
        # Se evita su redimension
        ventana.resizable(0,0)
        ventana.grab_set()
        
        # Se crea el marco
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=10, pady=10)
        
        # Etiqueta informativa para la ventana
        ctk.CTkLabel(marco, text="Listado de las bases de datos en el servidor",
        font=fuente_windgets).pack(padx=10, pady=10)
        
        # Agregar un campo de entrada para borrar
        self.borrar = tk.StringVar()
        
        # Se crea la entrada de texto para eliminar bd
        ctk.CTkEntry(marco,
                    font=fuente_windgets,
                    textvariable=self.borrar,
                    width=300).pack(padx=10)
        
        # Creamos caja de texto
        self.texto = ctk.CTkTextbox(marco, font=fuente_windgets, width=400, height=330)
        self.texto.pack(padx=10, pady=10)
        
        # Se crea una etiqueta para mostrar el numero de resultados
        self.resultado_label = ctk.CTkLabel(marco, text="", font=fuente_windgets)
        self.resultado_label.pack(pady=10)
        
        
        # Función interna de actualización SHOW DATABASES
        def actualizar():
            # Se establece el valor de la variable de control a string vacío (reset)
            self.borrar.set('')
            # Se elimina el contenido de la caja de resultados
            self.texto.delete('1.0', 'end')
            # Se realiza la llamada al método mostrar_bd (SHOW DATABASES) y se guarda en resultado
            resultado = base_datos.mostrar_bd()
            # Se itera el resultado y se presenta línea a línea en la caja de texto. 
            for bd in resultado:
                self.texto.insert('end', f"-{bd[0]}\n")
            
            # Se evalúa el resultado para deteminar la frase singular o plural
            numero_resultados = len(resultado)
            if numero_resultados == 1:
                self.resultado_label.configure(text=f"Se encontró {numero_resultados} resultado.")
            else:
                self.resultado_label.configure(text=f"Se encontraron {numero_resultados} resultados.")
        
        # Función interna para borrar bd        
        def borrando_bd():
            try:
                # Se elimina el contenido de la caja de resultados
                self.texto.delete('1.0', 'end')
                busqueda = self.borrar.get().lower()
                # Se realiza la llamada al método borrar_bd (DROP DATABASE {nombre_bd}) y se guarda en resultado 
                base_datos.borrar_bd(f"{busqueda}")
                self.resultado_label.configure(text=f"La base de datos {busqueda} se borro correctamente.")
            except:
                self.resultado_label.configure(text=f"La base de datos {busqueda} no existe.")
                CTkMessagebox(title="Error", message=f"La base de datos {busqueda}, no existe.", icon="cancel")
            
        # Boton borrar
        boton_borrar = ctk.CTkButton(marco, text="Borrar", command=borrando_bd)
        boton_borrar.pack(pady=10)
        
        # Boton actualizar
        boton_actualizar = ctk.CTkButton(marco, text="Actualizar", command=actualizar)
        boton_actualizar.pack(pady=10)
        
        actualizar()
    
    def ventana_crear_bd(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear base de datos")
        ventana.geometry("450x600")
        # Se evita su redimension
        ventana.resizable(0,0)
        ventana.grab_set()
        
        # Se crea el marco
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=10, pady=10)
        
        # Etiqueta informativa para la ventana
        ctk.CTkLabel(marco, text="Listado de las bases de datos en el servidor",
        font=fuente_windgets).pack(padx=10, pady=10)
        
        # Agregar un campo de entrada para poner bd
        self.crear = tk.StringVar()
        
        # Se crea la entrada de texto para crear bd
        ctk.CTkEntry(marco,
                    font=fuente_windgets,
                    textvariable=self.crear,
                    width=300).pack(padx=10)
        
        # Creamos caja de texto
        self.texto = ctk.CTkTextbox(marco, font=fuente_windgets, width=400, height=330)
        self.texto.pack(padx=10, pady=10)
        
        # Se crea una etiqueta para mostrar el numero de resultados
        self.resultado_label = ctk.CTkLabel(marco, text="", font=fuente_windgets)
        self.resultado_label.pack(pady=10)
        
        
        # Función interna de actualización SHOW DATABASES
        def actualizar():
            # Se establece el valor de la variable de control a string vacío (reset)
            self.crear.set('')
            # Se elimina el contenido de la caja de resultados
            self.texto.delete('1.0', 'end')
            # Se realiza la llamada al método mostrar_bd (SHOW DATABASES) y se guarda en resultado
            resultado = base_datos.mostrar_bd()
            # Se itera el resultado y se presenta línea a línea en la caja de texto. 
            for bd in resultado:
                self.texto.insert('end', f"-{bd[0]}\n")
            
            # Se evalúa el resultado para deteminar la frase singular o plural
            numero_resultados = len(resultado)
            if numero_resultados == 1:
                self.resultado_label.configure(text=f"Se encontró {numero_resultados} resultado.")
            else:
                self.resultado_label.configure(text=f"Se encontraron {numero_resultados} resultados.")
        
        # Función interna para crear bd        
        def creando_bd():
            try:
                # Se elimina el contenido de la caja de resultados
                self.texto.delete('1.0', 'end')
                busqueda = self.crear.get().lower()
                # Se realiza la llamada al método borrar_bd (DROP DATABASE {nombre_bd}) y se guarda en resultado 
                base_datos.crear_db(f"{busqueda}")
                self.resultado_label.configure(text=f"{busqueda} se creo correctamente, o ya estaba creada.")
            except:
                self.resultado_label.configure(text=f"Ocurrio un error con la creacion de la base de datos.")
                CTkMessagebox(title="Error", message=f"Hay un error en los caracteres de la base de datos {busqueda}", icon="cancel")
            
        # Boton crear
        boton_crear = ctk.CTkButton(marco, text="Crear", command=creando_bd)
        boton_crear.pack(pady=10)
        
        # Boton actualizar
        boton_actualizar = ctk.CTkButton(marco, text="Actualizar", command=actualizar)
        boton_actualizar.pack(pady=10)
        
        actualizar()
        
    def ventana_crear_respaldos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear respaldos")
        
    def ventana_crear_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear tablas")
        
    def ventana_eliminar_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar tablas")
        
    def ventana_mostrar_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar tablas")
    
    def ventana_mostrar_columnas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar columnas")
    
    def ventana_insertar_registros(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para insertar registros")
    
    def ventana_eliminar_registros(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar registros")
    
    def ventana_vaciar_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para vaciar tablas")
    
    def ventana_actualizar_registros(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para actualizar registros")

objeto_funciones = FuncionesPrograma()
    
    
class VentanaOpciones():
    
    # Diccionario para los botones
    botones = {'Consulta SQL': objeto_funciones.ventana_consultaSQL, 
               'Mostrar Bases de Datos': objeto_funciones.ventana_mostrar_bd,
               'Eliminar Bases de Datos': objeto_funciones.ventana_eliminar_bd,
               'Crear Bases de Datos': objeto_funciones.ventana_crear_bd, 
               'Crear Respaldos': objeto_funciones.ventana_crear_respaldos,
               'Crear Tablas': objeto_funciones.ventana_crear_tablas,
               'Eliminar Tablas': objeto_funciones.ventana_eliminar_tablas,
               'Mostrar Tablas': objeto_funciones.ventana_mostrar_tablas,
               'Mostrar Columnas': objeto_funciones.ventana_mostrar_columnas,
               'Insertar Registros': objeto_funciones.ventana_insertar_registros,
               'Eliminar Registros': objeto_funciones.ventana_eliminar_registros,
               'Vaciar Tablas': objeto_funciones.ventana_vaciar_tablas,
               'Actualizar Registros': objeto_funciones.ventana_actualizar_registros
               }
    
    def __init__(self):
        # Se crea la ventana de CustomTkinter
        self.root = ctk.CTk()
        # Se le da un título
        self.root.title("Opciones para trabajar con bases de datos.")
    
        # Marco para contener el menú superior
        menu_frame = ctk.CTkFrame(self.root)
        menu_frame.pack(side='top', fill='x')

        # Se crea el botón de Menú
        archivo = tk.Menubutton(menu_frame, 
                                text='Archivo', 
                                background='#2b2b2b', 
                                foreground='white', 
                                activeforeground='black', 
                                activebackground='gray52')
        
        # Se crea el botón de Menú
        edicion = tk.Menubutton(menu_frame, 
                                text='Edición', 
                                background='#2b2b2b', 
                                foreground='white', 
                                activeforeground='black', 
                                activebackground='gray52')
        
        # Se crea el menú
        menu_archivo = tk.Menu(archivo, tearoff=0)
        # Se crea el menú
        menu_edicion = tk.Menu(edicion, tearoff=0)

        # Añade una opción al menú desplegable
        menu_archivo.add_command(label='Imprimir Saludo', 
                                 command=lambda: print('Hello PC Master!'), 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
        
        
        # Crea un nuevo menú para la cascada
        cascada = tk.Menubutton(menu_edicion, 
                                text='Cascada', 
                                background='black', 
                                foreground='white', 
                                activeforeground='black', 
                                activebackground='gray52')
        
        # Se crea el menú
        menu_cascada = tk.Menu(cascada, tearoff=0)
        cascada.config(menu=menu_cascada)
        
        # Se crea una cascada dentro del menu de edición
        menu_edicion.add_cascade(label="Opciones", menu=menu_cascada, 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
    
        # Agrega opciones a la cascada
        menu_cascada.add_command(label="Opción 1", 
                                 command=lambda: print("Opción 1 seleccionada"), 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
        
        menu_cascada.add_command(label="Opción 2", 
                                 command=lambda: print("Opción 2 seleccionada"), 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
        
        menu_cascada.add_command(label="Opción 3", 
                                 command=lambda: print("Opción 3 seleccionada"), 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
        
        # Asigna el menú desplegable al Menubutton
        archivo.config(menu=menu_archivo)
        # Posiciona el Menubutton dentro del Frame
        archivo.pack(side='left')
        
        # Asigna el menú desplegable al Menubutton
        edicion.config(menu=menu_edicion)
        # Posiciona el Menubutton dentro del Frame
        edicion.pack(side='left')
        
        # Asigna el menú desplegable al Menubutton
        cascada.config(menu=menu_cascada)
        
        
        
        # Crea un Frame para contener los botones de la ventana
        frame_botones = ctk.CTkFrame(self.root)
        # Posiciona el Frame debajo del menú
        frame_botones.pack(side='top', fill='x')

        # Contador para la posición de los botones
        contador = 0

        # Valor de elementos por fila
        elementos_fila = 3

        # Crea los botones y establece su texto
        for texto_boton in self.botones:
            boton = ctk.CTkButton(
                master=frame_botones, #Se le indica en que frame aparecer
                text=texto_boton,
                height=25,
                width=200,
                command=self.botones[texto_boton]
            )
            boton.grid(row=contador//elementos_fila, column=contador%elementos_fila, padx=5, pady=5)

            # Incrementa el contador
            contador += 1

        self.root.mainloop()
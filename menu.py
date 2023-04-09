import tkinter as tk

# Creamos ventana del programa
root = tk.Tk()

# Creamos el menu de la ventana
menu_superior = tk.Menu()

# Se crean las opciones principales
menu_archivo = tk.Menu(menu_superior, tearoff=0)
menu_editar = tk.Menu(menu_superior, tearoff=0)
menu_ayuda = tk.Menu(menu_superior, tearoff=0)

# Agregar las opcines principales al menu
menu_superior.add_cascade(label="Archivo", menu=menu_archivo)
menu_superior.add_cascade(label="Editar", menu=menu_editar)
menu_superior.add_cascade(label="Ayuda", menu=menu_ayuda)

# Se crean las subopciones en archivo
menu_archivo.add_command(label="Abrir")
menu_archivo.add_command(label="Guardar")
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=root.quit)

# Se crean las subopciones para "Editar"
menu_editar.add_command(label="Cortar")
menu_editar.add_command(label="Copiar")
menu_editar.add_command(label="Pegar")

# Se crean las subopciones para "archivo > Preferencia"
menu_preferencias = tk.Menu(menu_archivo, tearoff=0)
menu_preferencias.add_command(label="Opcion 1")
menu_preferencias.add_command(label="Opcion 2")
menu_preferencias.add_command(label="Opcion 3")

# Se crea la cascada de "Preferencias" al menu "Archivo"
menu_archivo.add_cascade(label="Preferencias", menu=menu_preferencias)

# Creamos una subopcion en el menu_ayuda que no se puede seleccionar
menu_ayuda.add_command(label="Acerca de...", state=tk.DISABLED)

# Se muestra la barra de menu en la ventana principal
root.config(menu=menu_superior)

root.mainloop()


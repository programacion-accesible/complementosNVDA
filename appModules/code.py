# Addon para el programa visual sctudio code
# Por Gerardo Kessler [gera.ar@yahoo.com]

# Importamos los módulos necesarios
import appModuleHandler
# Módulo con un decorador para simplificar la creación de los gestos 
from scriptHandler import script
# Módulo para obtener los objetos en la interfaz del programa
import api
# Módulo para verbalizar mensajes o mostrar textos en una ventana simple
import ui

# Clase que hereda del módulo y que contiene los métodos, scripts y eventos a utilizar por el complemento
class AppModule(appModuleHandler.AppModule):

	# Decorador en el que se puede añadir el gesto, el título y la descripción para que aparezcan en el diálogo de gestos de entrada
	@script(
		category= 'VSCode',
		description= 'Verbaliza el número de fila y columna de la actual posición del cursor',
		gesture= 'kb:NVDA+l'
	)
	def script_stateView(self, gesture):
		"""Las funciones para scripts deben comenzar con la palabra script y guión bajo como nombre. Reciben los parámetros self y el gesto asociado"""
		# Obtenemos el objeto con el foco
		focus= api.getFocusObject()
		# navegamos desde el foco al elemento padre en navegación simple, a su hermano siguiente y a el penúltimo objeto hijo. Esto puede variar según los elementos de la interfaz
		state_object= focus.simpleParent.simpleNext.getChild(-2)
		# obtenemos el nombre del objeto a través de su atributo name
		state_object_name= state_object.name
		# Reemplazamos las abreviaturas por las palabras completas
		data= state_object_name.replace('Lín.', 'Línea ').replace('col.', 'Columna ')
		# Verbalizamos la cadena formateada
		ui.message(data)

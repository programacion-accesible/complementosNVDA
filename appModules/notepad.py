# Addon para el programa bloc de notas
# Por Gerardo Kessler [gera.ar@yahoo.com]

# Importamos los módulos necesarios
import appModuleHandler
# Módulo con un decorador para simplificar la creación de los gestos 
from scriptHandler import script
# Módulo para obtener los objetos en la interfaz del programa
import api
# Módulo para verbalizar mensajes o mostrar textos en una ventana simple
import ui
# módulo para gestión de pitidos
from tones import beep
# módulo para expresiones regulares
from re import search

# Clase que hereda del módulo y que contiene los métodos, scripts y eventos a utilizar por el complemento
class AppModule(appModuleHandler.AppModule):

	# Variable de clase que contendrá el objeto con la información de línea y columna
	state_object= None
	# Variable de clase para elemento de control
	toggle= False

	# Función que recupera el objeto con los datos de fila y columna
	def getStatusObject(self):
		# Obtenemos el objeto padre de la ventana
		foreground= api.getForegroundObject()
		# navegamos desde el foreground hasta el objeto con los datos deseados
		self.state_object= foreground.getChild(6).getChild(0).getChild(0)

	# Función que captura los eventos de teclado pulsados en un cuadro de texto
	def event_typedCharacter(self, obj, nextHandler):
		# Si la variable no tiene asignado el objeto con el estado se llama a la función que lo obtiene
		if not self.state_object:
			self.getStatusObject()
		# si la variable de control está activada se obtiene el texto del objeto con el estado, y con una regex se recupera el número de columna
		if self.toggle:
			column= search(r'Columna\s(\d+)', self.state_object.name)[1]
			# si el número de columna es mayor a 79, beep
			if int(column) > 79:
				beep(880, 150)
		# función para propagar el evento
		nextHandler()

	# Decorador en el que se puede añadir el gesto, el título y la descripción para que aparezcan en el diálogo de gestos de entrada
	@script(
		category= 'Bloc de notas',
		description= 'Verbaliza el número de fila y columna de la actual posición del cursor',
		gesture= 'kb:NVDA+l'
	)
	def script_stateView(self, gesture):
		"""Las funciones para scripts deben comenzar con la palabra script y guión bajo como nombre. Reciben los parámetros self y el gesto asociado"""
		if not self.state_object: self.getStatusObject()
		# obtenemos el nombre del objeto a través de su atributo name
		state_object_name= self.state_object.name
		# Reemplazamos el salto de línea por un espacio en blanco
		data= state_object_name.replace('\\n', ' ')
		# Verbalizamos la cadena formateada
		ui.message(data)

	@script(
		category= 'Bloc de notas',
		description= 'Activa y desactiva el aviso de 80 caracteres por línea',
		gesture= 'kb:NVDA+control+l'
	)
	def script_toggle(self, gesture):
		# Si la variable de control está activada, la desactivamos, de lo contrario realizamos el proceso inverso. Al finalizar verbalizamos el estado del control
		if self.toggle:
			self.toggle= False
			ui.message('desactivado')
		else:
			self.toggle= True
			ui.message('Activado')

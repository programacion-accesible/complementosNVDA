# Módulo que captura los caracteres pulsados
# Gerardo Kessler (http://gera.ar)

# Importamos los módulos necesarios
import globalPluginHandler
# Decorador para crear los gestos
from scriptHandler import script
# módulo para la verbalización y la activación de ventanas simples
import ui

# Clase que define métodos de eventos y scripts, asociaciones de gestos y otro código
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	
	# Variable de clase que aloja un diccionario vacío donde se almacenan las teclas capturadas
	keys= {}
	# Variable de control para activar o desactivar la captura
	toggle= False

	# Método que recibe todos los eventos de teclado
	def getScript(self, gesture):
		# Obtenemos el nombre de la tecla pulsada
		name= _(gesture.mainKeyName)
		# Si la variable de control está activa se verifica si la tecla capturada existe en el diccionario para sumar el valor, o agregarla como nuevo elemento
		if self.toggle:
			if name in self.keys:
				self.keys[name] += 1
			# Solo guardamos si es número o letra
			elif len(name) == 1 and name.isalpha() or name.isdigit():
				self.keys[name]= 1
		# Retornamos el evento de teclado para que se ejecute
		return globalPluginHandler.GlobalPlugin.getScript(self, gesture)

	# Decorador donde se define la categoría en los gestos de entrada, la descripción y el atajo de teclado
	@script(
		category= 'keylogger',
		description= 'Conmuta la activación de la captura de teclas',
		gesture= None
	)
	def script_toggle(self, gesture):
		if not self.toggle:
			self.toggle= True
			# Enviamos el mensaje para que sea verbalizado por el sintetizador
			ui.message('Capturando las teclas')
		else:
			self.toggle= False
			ui.message('Captura de teclas pausada')

	@script(
		category= 'keylogger',
		description= 'Muestra una ventana con los resultados temporales de la captura',
		gesture= None
	)
	def script_show(self, gesture):
		# Obtenemos una lista de tuplas ordenadas de mayor a menor por los valores del diccionario
		sorted_items= sorted(
			self.keys.items(),
			key=lambda x: x[1],
			reverse=True
		)
		# Concatenamos los elementos de la lista utilizando el salto de línea como delimitador
		string= '\n'.join([
			'{}: {}'.format(
				i[0], i[1]
			) for i in sorted_items
		])
		# Obtenemos la suma de los valores y concatenamos con la cadena anterior
		string= 'Total de letras y números capturados: {}\n{}'.format(
			sum(e[1] for e in self.keys.items()),
			string
		)
		# Ventana de diálogo propia de NVDA para mostrar los resultados
		ui.browseableMessage(string, 'Resultados de captura')

	@script(
		category= 'keylogger',
		description= 'Resetea el historial de capturas',
		gesture= None
	)
	def script_resetList(self, gesture):
		# Vaciamos el diccionario
		self.keys.clear()
		ui.message('Lista de teclas reseteada')

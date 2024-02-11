# Módulo que captura el texto seleccionado y busca en google
# Gerardo Kessler (http://gera.ar)

# Importamos los módulos necesarios
import globalPluginHandler
# Decorador para crear los gestos
from scriptHandler import script
# módulo para la verbalización y la activación de ventanas simples
import ui
# módulo para abrir el navegador por defecto
import webbrowser
# Módulo para obtener el objeto con el foco
import api

# Clase que define métodos de eventos y scripts, asociaciones de gestos y otro código
class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# Función tomada del complemento DLEChecker de Antonio Pascales, que captura el texto seleccionado
	def getSelectedText(self):
		obj = api.getFocusObject()
		
		if hasattr(obj.treeInterceptor, 'TextInfo') and not obj.treeInterceptor.passThrough:
			try:
				info = obj.treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
			except (RuntimeError, NotImplementedError):
				info = None
			
			if not info or info.isCollapsed:
				return None
			else:
				return info.text.lower()
		else:
			try:
				return obj.selection.text.lower()
			except (RuntimeError, NotImplementedError):
				return None

	def script_googleSearch(self, gesture):
		text= self.getSelectedText()
		if text:
			webbrowser.open('https://www.google.com/search?q={}'.format(text))
		else:
			ui.message('Imposible capturar el texto seleccionado')

	script_googleSearch.category= 'googleSearch'
	script_googleSearch.__doc__= 'Captura el texto seleccionado y activa la página de búsqueda de google con los resultados en el navegador por defecto'

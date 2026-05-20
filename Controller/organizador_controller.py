import os
import shutil
import threading

class OrganizadorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # Definimos la ruta de descargas de forma dinámica
        self.view.establecer_evento_organizar(self.iniciar_hilo_organizacion)

    def ejecutar(self):
        """Arranca la aplicación mostrando la ventana de la interfaz gráfica."""
        self.view.arrancar_interfaz()

    def iniciar_hilo_organizacion(self):
        """Crea y arranca un hilo secundario para que la GUI no se congele."""
        # Creamos un hilo que apunta directamente a nuestra función lógica pesada
        hilo = threading.Thread(target=self.procesar_organizacion)
        hilo.start()

    def procesar_organizacion(self):
        """Flujo de ejecución principal gatillado por el botón de la interfaz."""
        # Obtenemos dinámicamente la ruta que el usuario eligió en la pantalla
        ruta_a_organizar = self.view.obtener_ruta_actual()
        
        # Guardamos la ruta temporalmente para que los demás métodos la usen
        self.ruta_actual = ruta_a_organizar

        # Bloqueamos el botón en la vista para evitar accidentes
        self.view.bloquear_controles()

        # Ejecutamos la organización pasando por la barra de progreso
        self.organizar_archivos_con_progreso()
        
        # Al finalizar, limpiamos la vista y notificamos
        self.view.desbloquear_controles()
        self.view.mostrar_exito("La carpeta ha sido organizada correctamente según sus extensiones.")

    def asegurar_carpeta_destino(self, nombre_carpeta):
        """Asegura la existencia de una carpeta específica antes de mover un archivo."""
        # Si nombre_carpeta es "Documentos/Word", os.path.join creará la ruta completa correctamente
        ruta_completa = os.path.join(self.ruta_actual, nombre_carpeta)

        # os.makedirs crea carpetas anidadas (ej. Documentos y luego Word) de golpe.
        # exist_ok=True evita que lance un error si la carpeta ya existe.
        os.makedirs(ruta_completa, exist_ok=True)
        return ruta_completa
    
    def organizar_archivos_con_progreso(self):
        """Filtra los elementos, calcula el progreso y los procesa uno por uno."""
        # 1. Obtenemos solo los archivos reales del directorio (ignorando carpetas)
        todos_los_elementos = os.listdir(self.ruta_actual)
        archivos_a_procesar = [e for e in todos_los_elementos if os.path.isfile(os.path.join(self.ruta_actual, e))]
        
        total_archivos = len(archivos_a_procesar)
        
        # Si no hay archivos que mover, salimos de inmediato
        if total_archivos == 0:
            return

        # 2. Le decimos a la vista cuál es el 100% de la barra
        self.view.configurar_limites_progreso(total_archivos)
        
        # 3. Recorremos e incrementamos el contador paso a paso
        for indice, archivo in enumerate(archivos_a_procesar, start=1):
            ruta_elemento = os.path.join(self.ruta_actual, archivo)
            
            # Avisamos a la vista en qué archivo va y actualizamos la barra
            self.view.actualizar_progreso(indice, f"Organizando: {archivo}")
            
            # Procesamos el archivo en el sistema operativo
            self.procesar_archivo(archivo, ruta_elemento)

    def procesar_archivo(self, nombre_archivo, ruta_origen):
        """Determina el destino del archivo y realiza el traslado."""
        extension = os.path.splitext(nombre_archivo)[1].lower()
        
        # Le pedimos al modelo que decida a dónde pertenece el archivo
        carpeta_destino = self.model.obtener_carpeta_por_extension(extension)
        
        # Aseguramos que la carpeta destino exista (por si es una subcarpeta dinámica)
        ruta_destino_carpeta = self.asegurar_carpeta_destino(carpeta_destino)
        ruta_destino_completa = os.path.join(ruta_destino_carpeta, nombre_archivo)
        
        # Operación en el sistema operativo
        shutil.move(ruta_origen, ruta_destino_completa)
        

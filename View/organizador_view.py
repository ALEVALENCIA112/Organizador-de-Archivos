import tkinter as tk
from tkinter import messagebox, filedialog, ttk


class OrganizadorView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Organizador de Archivos")
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        self.ruta_seleccionada = ""

        self._crear_componentes()

    def _crear_componentes(self):
        # Etiqueta de título
        lbl_titulo = tk.Label(self.root, text="Organizador Personal de Carpetas", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=15)
        
        # Cuadro de texto para mostrar la ruta elegida (deshabilitado para que no escriban a mano)
        self.txt_ruta = tk.Entry(self.root, width=50, font=("Arial", 10))
        self.txt_ruta.insert(0, "Ninguna carpeta seleccionada...")
        self.txt_ruta.config(state="disabled")
        self.txt_ruta.pack(pady=5)
        
        # Botón para abrir el explorador de archivos
        btn_seleccionar = tk.Button(self.root, text="Seleccionar Carpeta", command=self._seleccionar_carpeta, bg="#e1e1e1")
        btn_seleccionar.pack(pady=5)

        # Etiqueta para indicar el estado o archivo actual
        self.lbl_estado = tk.Label(self.root, text="", font=("Arial", 9, "italic"), fg="#555555")
        self.lbl_estado.pack(pady=(10, 0))

        # La barra de progreso. 'determinate' significa que sabemos cuántos archivos hay en total
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)
        
        # Botón para iniciar la organización (El controlador le asignará la función después)
        self.btn_ejecutar = tk.Button(self.root, text="Empezar Organización", state="disabled", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_ejecutar.pack(pady=20)

    def _seleccionar_carpeta(self):
        """Abre el diálogo nativo para elegir una carpeta del sistema."""
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta que deseas organizar")
        
        if carpeta: # Si el usuario no canceló el diálogo
            self.ruta_seleccionada = carpeta
            
            # Actualizamos el cuadro de texto visual
            self.txt_ruta.config(state="normal")
            self.txt_ruta.delete(0, tk.END)
            self.txt_ruta.insert(0, carpeta)
            self.txt_ruta.config(state="disabled")
            
            # Habilitamos el botón de ejecución ya que hay una ruta válida
            self.btn_ejecutar.config(state="normal")

    def establecer_evento_organizar(self, funcion_controlador):
        """Permite al controlador inyectar la función que se ejecutará al pulsar el botón."""
        self.btn_ejecutar.config(command=funcion_controlador)

    def obtener_ruta_actual(self):
        """Devuelve la ruta que el usuario seleccionó en la interfaz."""
        return self.ruta_seleccionada
    
    def configurar_limites_progreso(self, maximo):
        """Define el valor máximo de la barra (el número total de archivos)."""
        self.progress["maximum"] = maximo
        self.progress["value"] = 0
    
    def actualizar_progreso(self, valor_actual, texto_estado):
        """Actualiza numéricamente la barra y cambia el texto informativo."""
        self.progress["value"] = valor_actual
        self.lbl_estado.config(text=texto_estado)
        # Fuerza a Tkinter a redibujar los cambios en la pantalla inmediatamente
        self.root.update_idletasks()
    
    def bloquear_controles(self):
        """Deshabilita el botón mientras se organiza para evitar doble clics."""
        self.btn_ejecutar.config(state="disabled")
    
    def desbloquear_controles(self):
        """Vuelve a habilitar el botón al terminar."""
        self.btn_ejecutar.config(state="normal")
        
    def mostrar_exito(self, mensaje):
        """Muestra una ventana emergente informativa de éxito."""
        messagebox.showinfo("Completado", mensaje)

    def arrancar_interfaz(self):
        """Inicia el bucle principal de la interfaz gráfica (Mantiene la ventana abierta)."""
        self.root.mainloop()
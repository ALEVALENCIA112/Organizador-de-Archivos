import tkinter as tk
from tkinter import messagebox, filedialog, ttk


class OrganizadorView:

    VERSION = "1.0.1"
    COPYRIGHT = "© 2026 CRAV - Todos los derechos reservados"
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Organizador de Archivos")
        self.root.geometry("480x320")
        self.root.resizable(False, False)

        # --- PALETA DE COLORES (Flat Design) ---
        self.COLOR_FONDO = "#eae4d2"       # Gris casi blanco, muy limpio
        self.COLOR_TEXTO = "#212529"       # Gris oscuro (evita el negro puro para mitigar la fatiga visual)
        self.COLOR_SECUNDARIO = "#6C757D"  # Gris sutil para estados y textos secundarios
        self.COLOR_BOTON_SEL = "#E9ECEF"   # Gris claro para botones secundarios
        self.COLOR_BOTON_ACT = "#2A9D8F"   # Verde esmeralda plano para la acción principal
        self.COLOR_BOTON_DIS = "#474747"   # Gris apagado para estados deshabilitados

        # Configuración del color de fondo de la ventana raíz
        self.root.config(bg=self.COLOR_FONDO)

        # Configurar estilos de los componentes TTK (como la barra de progreso)
        self._configurar_estilos_ttk()

        self.ruta_seleccionada = ""

        self._crear_componentes()

        self.version_y_copyright()

    def _configurar_estilos_ttk(self):
        """Define el aspecto visual para los widgets de la librería ttk."""
        style = ttk.Style()
        style.theme_use('clam')  # Usamos 'clam' como base porque permite personalizar colores planos
        
        # Estilo personalizado para la barra de progreso (sin bordes ruidosos, color plano)
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor="#E9ECEF",
            background=self.COLOR_BOTON_ACT,
            thickness=10,
            borderwidth=0
        )

    def version_y_copyright(self):
        """Agrega un label con la versión y el copyright en la parte inferior de la ventana."""
        lbl = tk.Label(
            self.root,
            text=f"Versión {self.VERSION}\t{self.COPYRIGHT}",
            font=("Segoe UI", 8),
            fg=self.COLOR_SECUNDARIO,
            bg=self.COLOR_FONDO
        )
        lbl.pack(side="bottom", anchor="center", padx=10, pady=5)

    def _crear_componentes(self):

        # 1. Contenedor principal para añadir márgenes internos globales (Padding)
        contenedor = tk.Frame(self.root, bg=self.COLOR_FONDO)
        contenedor.pack(fill="both", expand=True, padx=25, pady=15)

        # 2. Etiqueta de título principal
        lbl_titulo = tk.Label(contenedor, text="Organizador Personal de Carpetas",
                            font=("Arial", 14, "bold"),
                            bg=self.COLOR_FONDO,
                            fg=self.COLOR_TEXTO)
        lbl_titulo.pack(pady=(0, 10))
        
        # 3. Cuadro de texto para mostrar la ruta elegida (deshabilitado para que no escriban a mano)
        self.txt_ruta = tk.Entry(contenedor,
                                width=50,
                                font=("Segoe UI", 9),
                                bg="#FFFFFF",
                                fg=self.COLOR_TEXTO,
                                bd=1,
                                relief="solid",
                                disabledbackground="#F1F3F5",
                                disabledforeground=self.COLOR_SECUNDARIO)
        self.txt_ruta.insert(0, "Ninguna carpeta seleccionada...")
        self.txt_ruta.config(state="disabled")
        self.txt_ruta.pack(pady=5, ipady=3)
        
        # 4. Botón para abrir el explorador de archivos
        self.btn_seleccionar = tk.Button(contenedor,
                                    text="Seleccionar Carpeta",
                                    command=self._seleccionar_carpeta,
                                    bg=self.COLOR_BOTON_SEL,
                                    fg=self.COLOR_TEXTO,
                                    font=("Segoe UI", 9, "bold"),
                                    bd=0,
                                    cursor="hand2",
                                    activebackground="#DDE2E6",
                                    activeforeground=self.COLOR_TEXTO)
        self.btn_seleccionar.pack(pady=5, ipadx=10, ipady=4)

        # 5. Etiqueta para indicar el estado o archivo actual
        self.lbl_estado = tk.Label(contenedor,
                                text="",
                                font=("Segoe UI", 9, "italic"),
                                fg=self.COLOR_SECUNDARIO,
                                bg=self.COLOR_FONDO)
        self.lbl_estado.pack(pady=(8, 2))

        # 6. La barra de progreso. 'determinate' significa que sabemos cuántos archivos hay en total
        self.progress = ttk.Progressbar(contenedor,
                                        orient="horizontal",
                                        length=380,
                                        mode="determinate",
                                        style="Horizontal.TProgressbar")
        self.progress.pack(pady=2)

        # --- MEJORA: AGREGAR CONTADOR DE PORCENTAJE ---
        self.lbl_porcentaje = tk.Label(
            contenedor,
            text="0% (0/0 archivos)",
            font=("Segoe UI", 9, "bold"),
            fg=self.COLOR_TEXTO,
            bg=self.COLOR_FONDO
        )
        self.lbl_porcentaje.pack(pady=(2, 5))
        
        # 7. Botón para iniciar la organización (El controlador le asignará la función después)
        self.btn_ejecutar = tk.Button(contenedor,
                                    text="Empezar Organización",
                                    state="disabled",
                                    bg=self.COLOR_BOTON_DIS,
                                    fg="#FFFFFF",
                                    font=("Segoe UI", 10, "bold"),
                                    bd=0,
                                    cursor="arrow",
                                    activebackground="#21867A",
                                    activeforeground="#FFFFFF")
        self.btn_ejecutar.pack(pady=(5,0), ipadx=15, ipady=6)

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
            self.btn_ejecutar.config(state="normal",
                                    bg=self.COLOR_BOTON_ACT,
                                    cursor="hand2",)

    def establecer_evento_organizar(self, funcion_controlador):
        """Permite al controlador inyectar la función que se ejecutará al pulsar el botón."""
        self.btn_ejecutar.config(command=funcion_controlador)

    def obtener_ruta_actual(self):
        """Devuelve la ruta que el usuario seleccionó en la interfaz."""
        return self.ruta_seleccionada
    
    def configurar_limites_progreso(self, maximo):
        """Define el valor máximo de la barra (el número total de archivos)."""
        self.total_archivos = maximo
        self.progress["maximum"] = maximo
        self.progress["value"] = 0
        self.lbl_porcentaje.config(text=f"0% (0/{maximo} archivos)")
    
    def actualizar_progreso(self, valor_actual, texto_estado):
        """Actualiza numéricamente la barra y cambia el texto informativo."""
        self.progress["value"] = valor_actual
        self.lbl_estado.config(text=texto_estado)

        # Calcular el porcentaje en tiempo real
        if self.total_archivos > 0:
            porcentaje = int((valor_actual / self.total_archivos) * 100)
            self.lbl_porcentaje.config(text=f"{porcentaje}% ({valor_actual}/{self.total_archivos} archivos)")

        # Fuerza a Tkinter a redibujar los cambios en la pantalla inmediatamente
        self.root.update_idletasks()
    
    def bloquear_controles(self):
        """Deshabilita el botón mientras se organiza para evitar doble clics."""
        self.btn_ejecutar.config(state="disabled",
                                bg=self.COLOR_BOTON_DIS,
                                cursor="arrow")
        self.btn_seleccionar.config(state="disabled",
                                    cursor="arrow")
    
    def desbloquear_controles(self):
        """Vuelve a habilitar el botón al terminar."""
        self.btn_ejecutar.config(state="normal",
                                bg=self.COLOR_BOTON_ACT,
                                cursor="hand2")
        self.btn_seleccionar.config(state="normal",
                                    cursor="hand2")

    def mostrar_exito(self, mensaje):
        """Muestra una ventana emergente informativa de éxito."""
        messagebox.showinfo("Completado", mensaje)

    def arrancar_interfaz(self):
        """Inicia el bucle principal de la interfaz gráfica (Mantiene la ventana abierta)."""
        self.root.mainloop()

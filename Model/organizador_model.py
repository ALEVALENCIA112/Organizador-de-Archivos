class OrganizadorModel:

    def __init__(self):
        # Mapeo de extensiones a su respectiva carpeta de destino
        self.tipos_extensiones = {
            "Imagenes": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            "Documentos/Word": ['.docx', '.doc', '.odt', '.dot', '.docm', '.xml'],
            "Documentos/Excel": ['.xlsx', '.xls', '.csv'],
            "Documentos/PowerPoint": ['.pptx', '.ppt'],
            "Documentos/Texto": ['.txt', '.rtf', '.odt', '.md'],
            "Documentos/PDF": ['.pdf'],
            "Videos": ['.mp4', '.avi', '.mkv', '.mov', '.flv'],
            "Audio": ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
            "Programas": ['.exe', '.msi', '.dmg', '.deb', '.rpm'],
            "Comprimidos": ['.zip', '.rar', '.7z', '.tar', '.gz'],
            "Bases de Datos": ['.sql', '.db', '.sqlite', '.mdb', '.accdb'],
            "Otros": []
            }
        
    def obtener_carpeta_por_extension(self, extension):
        """
        Analiza la extensión (en minúsculas) y devuelve la carpeta correspondiente.
        Si no la encuentra, devuelve 'Otros'.
        """
        for carpeta, extensiones in self.tipos_extensiones.items():
            if extension in extensiones:
                return carpeta
        return "Otros"
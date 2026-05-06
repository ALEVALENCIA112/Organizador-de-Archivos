# interactuar con el sistema operativo en general
import os
#Sirve para la manipulación de archivos y directorios
import shutil

# ruta de la carpeta de descargas del usuario
ruta = os.path.expanduser('~') + '/Downloads'

# carpetas a crear para organizar los archivos
carpetas = ["Imagenes",
            "Docs Word",
            "Docs Excel",
            "Docs PowerPoint",
            "Docs de Texto",
            "Docs PDF",
            "Videos",
            "Audio",
            "Programas",
            "Otros",
            "Comprimidos",
            "Bases de Datos"]

# crear carpetas en la ruta
# si la carpeta ya existe, no se crea de nuevo
# se toma los archivos/carpetas y los compara con la lista de carpetas
for carpeta in carpetas:

    # se crea la ruta completa de la carpeta a crear
                    # analiza la ruta y el nombre del archivo/carpeta
    ruta_completa = os.path.join(ruta, carpeta)

    # si la carpeta no existe la crea, si ya existe no hace nada
    if not os.path.exists(ruta_completa):
        #crea la carpeta en la ruta especificada
        os.mkdir(ruta_completa)


# tipos de archivos a organizar
tipos = {

    "Imagenes": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    "Docs Word": ['.docx', '.doc', '.odt', '.dot', '.docm', 'xml'],
    "Docs Excel": ['.xlsx', '.xls', '.csv'],
    "Docs PowerPoint": ['.pptx', '.ppt'],
    "Docs de Texto": ['.txt', '.rtf', '.odt'],
    "Docs PDF": ['.pdf'],
    "Videos": ['.mp4', '.avi', '.mkv', '.mov', '.flv'],
    "Audio": ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    "Programas": ['.exe', '.msi', '.dmg', '.deb', '.rpm'],
    "Comprimidos": ['.zip', '.rar', '.7z', '.tar', '.gz'],
    "Bases de Datos": ['.sql', '.db', '.sqlite', '.mdb', '.accdb'],
    "Otros": []

}


# recorre los archivos en la ruta de descargas
for archivo in os.listdir(ruta):
    # se crea la ruta completa del archivo a organizar
                    # ~/Downloads/(name).txt - (name).zip - (name).docx - etc
    archivo_path = os.path.join(ruta, archivo)

    # si el archivo es un archivo (no una carpeta), se obtiene su extensión
    if os.path.isfile(archivo_path):

        # se obtiene la extension del archivo y se convierte a minúscula para evitar problemas
                            # separa el nombre del archivo de su extensión, y se toma la extensión (incluyendo el punto) y se convierte a minúscula
        extension = os.path.splitext(archivo)[1].lower()

        # anteriormente comprobaba la pertenencia de la extensión y de no haber encontrado ninguna se movia a otros, se realizaba ese proceso al comprobar cada carpeta
        # por lo que daba un error ya que intentaba moverlo en cada iteracion

        # Creación de una bandera para verificar si el archivo se movio
        # Resuelve el problema de comprobar el archivo y si no existe entonces enviarlo a otros en cada iteracion 
        movido = False
        

        # se recorre el diccionario de tipos
        # Carpeta corresponde al nombre declarado del arreglo, y extensiones corresponde a la lista de extensiones declarada en el arreglo (.jpg, .png, etc)
        # tipos.items() devuelve una lista de tuplas (carpeta, extensiones) para cada elemento del diccionario ("Imagenes", ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']), ("Documentos", ['.pdf', '.docx', '.txt', '.xlsx', '.pptx']), etc)
        for carpeta, extensiones in tipos.items():
            # se verifica si la extensión del archivo coincide con alguna de las extensiones de la carpeta actual
            if extension in extensiones:
                # se crea la ruta completa de la carpeta a mover el archivo
                                        # ~/Downloads , Imagenes - Documentos - Videos - etc 
                carpeta_path = os.path.join(ruta, carpeta)

                # si la carpeta no existe, se crea
                if not os.path.exists(carpeta_path):
                    os.mkdir(carpeta_path)

                # se mueve el archivo a la carpeta correspondiente
                            # archivo   ,             (-------carpeta-------)
                                                    # toma la ruta del archivo a mover
                shutil.move(archivo_path, os.path.join(carpeta_path, archivo))

                # se imprime el archivo movido y la carpeta a la que fue movido
                print(f"Movido: {archivo} -> {carpeta}")

                movido = True
                break

            # si la extensión del archivo no coincide con ninguna de las extensiones de las carpetas, se mueve a la carpeta "Otros"
        if not movido:

            # se crea la ruta completa de la carpeta "Otros"
            carpeta_path = os.path.join(ruta, "Otros")

            # se mueve el archivo a la carpeta "Otros"
            shutil.move(archivo_path, os.path.join(carpeta_path, archivo))

            # se imprime el archivo movido y la carpeta a la que fue movido
            print(f"Movido: {archivo} -> Otros")
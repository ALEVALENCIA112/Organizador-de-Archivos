from Model.organizador_model import OrganizadorModel
from View.organizador_view import OrganizadorView
from Controller.organizador_controller import OrganizadorController

def main():
    # Inicialización de componentes
    modelo = OrganizadorModel()
    vista = OrganizadorView()
    
    # Inyección de dependencias en el controlador
    controlador = OrganizadorController(modelo, vista)
    
    # Ejecución del flujo
    controlador.ejecutar()

if __name__ == "__main__":
    main()


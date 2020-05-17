import os
from .usuarios.controllers import *
from .mcatalogo.controllers import *
from .pedido.controllers import *
from .operaciones.controllers import *
from .mayudaventas.controllers import *
from .main.controllers import Index
from tornado.web import StaticFileHandler
from .mcatalogo.servicio import *
from .configuracion.controllers import *

def get_handlers():
    """Retorna una lista con las rutas, sus manejadores y datos extras."""
    handlers = list()
    # Login
    handlers.append((r'/login', LoginController))
    handlers.append((r'/logout', LogoutController))
    handlers.append((r'/manual', ManualController))

    # Principal
    handlers.append((r'/', Index))

    # Usuario
    handlers.extend(get_routes(UsuarioController))
    handlers.extend(get_routes(RolController))

    # Bitacora
    handlers.extend(get_routes(BitacoraController))

    # MCatalogo
    handlers.extend(get_routes(ProductoController))
    handlers.extend(get_routes(NivelController))
    handlers.extend(get_routes(PromocionController))
    handlers.extend(get_routes(OfertaController))
    handlers.extend(get_routes(OfertaWebController))
    handlers.extend(get_routes(CatalogoController))
    handlers.extend(get_routes(ApiProductoController))
    handlers.extend(get_routes(PaginaController))

    # Pedido
    handlers.extend(get_routes(PedidoController))

    # AyudaVentas
    handlers.extend(get_routes(AyudaVentasController))
    handlers.extend(get_routes(ApiAyudaVentasController))

    # Bitacora
    handlers.extend(get_routes(BitacoraController))

    #Servicio
    handlers.extend(get_routes(ApiProductoController))

    # Configuracion
    handlers.extend(get_routes(ConfiguracionController))
    handlers.extend(get_routes(FinancieroController))




    handlers.append((r'/resources/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'resources')}))
    return handlers


def get_routes(handler):
    routes = list()
    for route in handler.routes:
        routes.append((route, handler))
    return routes

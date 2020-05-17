from matplotlib.style.core import update_nested_dict

from server.database.connection import transaction
from .models import *
from .managers import *
from ..usuarios.models import *

import schedule


def insertions():

    with transaction() as session:

        ###Modulo de Operaciones

        mcatalogo_m = session.query(Modulo).filter(Modulo.name == 'mcatalogo').first()
        if mcatalogo_m is None:
            mcatalogo_m = Modulo(title='Modulo Catalogos', name='mcatalogo', icon='book')

        producto_m = session.query(Modulo).filter(Modulo.name == 'centro_costo').first()
        if producto_m is None:
            producto_m = Modulo(title='Producto', route='/producto', name='producto',
                                    icon='portrait')

        nivel_m = session.query(Modulo).filter(Modulo.name == 'centro_costo').first()
        if nivel_m is None:
            nivel_m = Modulo(title='Nivel', route='/nivel', name='nivel',
                             icon='portrait')

        promocion_m = session.query(Modulo).filter(Modulo.name == 'centro_costo').first()
        if promocion_m is None:
            promocion_m = Modulo(title='Promocion', route='/promocion', name='promocion',
                             icon='portrait')

        oferta_m = session.query(Modulo).filter(Modulo.name == 'centro_costo').first()
        if oferta_m is None:
            oferta_m = Modulo(title='Oferta', route='/oferta', name='oferta',
                                 icon='portrait')
        ofertaweb_m = session.query(Modulo).filter(Modulo.name == 'centro_costo').first()
        if ofertaweb_m is None:
            ofertaweb_m = Modulo(title='OfertaWeb', route='/ofertaweb', name='ofertaweb',
                              icon='portrait')

        catalogo_m = session.query(Modulo).filter(Modulo.name == 'catalogo').first()
        if catalogo_m is None:
            catalogo_m = Modulo(title='Catalogo', route='/catalogo', name='catalogo', icon='portrait')

        pagina_m = session.query(Modulo).filter(Modulo.name == 'pagina').first()
        if pagina_m is None:
            pagina_m = Modulo(title='Pagina', route='/pagina', name='pagina', icon='portrait')


        ayudaventas_m = session.query(Modulo).filter(Modulo.name == 'ayudaventas_m').first()
        if ayudaventas_m is None:
            ayudaventas_m = Modulo(title='Ayuda Ventas', route='/ayudaventas', name='ayudaventas',
                                   icon='portrait')

        mcatalogo_m.children.append(catalogo_m)
        mcatalogo_m.children.append(pagina_m)
        mcatalogo_m.children.append(producto_m)
        mcatalogo_m.children.append(nivel_m)
        mcatalogo_m.children.append(promocion_m)
        mcatalogo_m.children.append(oferta_m)
        mcatalogo_m.children.append(ofertaweb_m)
        mcatalogo_m.children.append(ayudaventas_m)

        query_producto = session.query(Modulo).filter(Modulo.name == 'producto_query').first()
        if query_producto is None:
            query_producto = Modulo(title='Consultar', route='',
                                    name='producto_query',
                                    menu=False)

        insert_producto = session.query(Modulo).filter(Modulo.name == 'producto_insert').first()
        if insert_producto is None:
            insert_producto = Modulo(title='Adicionar', route='/producto_insert',
                                     name='producto_insert',
                                     menu=False)
        update_producto = session.query(Modulo).filter(Modulo.name == 'producto_update').first()
        if update_producto is None:
            update_producto = Modulo(title='Actualizar', route='/producto_update',
                                     name='producto_update',
                                     menu=False)
        delete_producto = session.query(Modulo).filter(Modulo.name == 'producto_delete').first()
        if delete_producto is None:
            delete_producto = Modulo(title='Dar de Baja', route='/producto_delete',
                                     name='producto_delete',
                                     menu=False)

        imprimir_producto = session.query(Modulo).filter(Modulo.name == 'producto_imprimir').first()
        if imprimir_producto is None:
            imprimir_producto = Modulo(title='Imprimir', route='/producto_imprimir',
                                       name='producto_imprimir',
                                       menu=False)

            producto_m.children.append(query_producto)
            producto_m.children.append(insert_producto)
            producto_m.children.append(update_producto)
            producto_m.children.append(delete_producto)
            producto_m.children.append(imprimir_producto)

        query_catalogo = session.query(Modulo).filter(Modulo.name == 'catalogo_query').first()
        if query_catalogo is None:
            query_catalogo = Modulo(title='Consultar', route='',
                                    name='catalogo_query',
                                    menu=False)

        insert_catalogo = session.query(Modulo).filter(Modulo.name == 'catalogo_insert').first()
        if insert_catalogo is None:
            insert_catalogo = Modulo(title='Adicionar', route='/catalogo_insert',
                                     name='catalogo_insert',
                                     menu=False)
        update_catalogo = session.query(Modulo).filter(Modulo.name == 'catalogo_update').first()
        if update_catalogo is None:
            update_catalogo = Modulo(title='Actualizar', route='/catalogo_update',
                                     name='catalogo_update',
                                     menu=False)
        delete_catalogo = session.query(Modulo).filter(Modulo.name == 'catalogo_delete').first()
        if delete_catalogo is None:
            delete_catalogo = Modulo(title='Dar de Baja', route='/catalogo_delete',
                                     name='catalogo_delete',
                                     menu=False)

        imprimir_catalogo = session.query(Modulo).filter(Modulo.name == 'catalogo_imprimir').first()
        if imprimir_catalogo is None:
            imprimir_catalogo = Modulo(title='Imprimir', route='/catalogo_imprimir',
                                       name='catalogo_imprimir',
                                       menu=False)

            catalogo_m.children.append(query_catalogo)
            catalogo_m.children.append(insert_catalogo)
            catalogo_m.children.append(update_catalogo)
            catalogo_m.children.append(delete_catalogo)
            catalogo_m.children.append(imprimir_catalogo)

        query_pagina = session.query(Modulo).filter(Modulo.name == 'pagina_query').first()
        if query_pagina is None:
            query_pagina = Modulo(title='Consultar', route='',
                                  name='pagina_query',
                                  menu=False)

        insert_pagina = session.query(Modulo).filter(Modulo.name == 'pagina_insert').first()
        if insert_pagina is None:
            insert_pagina = Modulo(title='Adicionar', route='/pagina_insert',
                                   name='pagina_insert',
                                   menu=False)
        update_pagina = session.query(Modulo).filter(Modulo.name == 'pagina_update').first()
        if update_pagina is None:
            update_pagina = Modulo(title='Actualizar', route='/pagina_update',
                                   name='pagina_update',
                                   menu=False)
        delete_pagina = session.query(Modulo).filter(Modulo.name == 'pagina_delete').first()
        if delete_pagina is None:
            delete_pagina = Modulo(title='Dar de Baja', route='/pagina_delete',
                                   name='pagina_delete',
                                   menu=False)

        imprimir_pagina = session.query(Modulo).filter(Modulo.name == 'pagina_imprimir').first()
        if imprimir_pagina is None:
            imprimir_pagina = Modulo(title='Imprimir', route='/pagina_imprimir',
                                     name='pagina_imprimir',
                                     menu=False)

            pagina_m.children.append(query_pagina)
            pagina_m.children.append(insert_pagina)
            pagina_m.children.append(update_pagina)
            pagina_m.children.append(delete_pagina)
            pagina_m.children.append(imprimir_pagina)

        query_nivel = session.query(Modulo).filter(Modulo.name == 'nivel_query').first()
        if query_nivel is None:
            query_nivel = Modulo(title='Consultar', route='',
                                 name='nivel_query',
                                 menu=False)

        insert_nivel = session.query(Modulo).filter(Modulo.name == 'nivel_insert').first()
        if insert_nivel is None:
            insert_nivel = Modulo(title='Adicionar', route='/nivel_insert',
                                  name='nivel_insert',
                                  menu=False)

        uodate_nivel = session.query(Modulo).filter(Modulo.name == 'nivel_update').first()
        if uodate_nivel is None:
            update_nivel = Modulo(title='Actualizar', route='/nivel_update',
                                  name='nivel_update',
                                  menu=False)
        delete_nivel = session.query(Modulo).filter(Modulo.name == 'nivel_delete').first()
        if delete_nivel is None:
            delete_nivel = Modulo(title='Dar de Baja', route='/nivel_delete',
                                  name='nivel_delete',
                                  menu=False)

        imprimir_nivel = session.query(Modulo).filter(Modulo.name == 'nivel_imprimir').first()
        if imprimir_nivel is None:
            imprimir_nivel = Modulo(title='Imprimir', route='/nivel_imprimir',
                                    name='nivel_imprimir',
                                    menu=False)

            nivel_m.children.append(query_nivel)
            nivel_m.children.append(insert_nivel)
            nivel_m.children.append(update_nivel)
            nivel_m.children.append(delete_nivel)
            nivel_m.children.append(imprimir_nivel)

        query_promocion = session.query(Modulo).filter(Modulo.name == 'promocion_query').first()
        if query_promocion is None:
            query_promocion = Modulo(title='Consultar', route='',
                                     name='promocion_query',
                                     menu=False)

        insert_promocion = session.query(Modulo).filter(Modulo.name == 'promocion_insert').first()
        if insert_promocion is None:
            insert_promocion = Modulo(title='Adicionar', route='/promocion_insert',
                                      name='promocion_insert',
                                      menu=False)
        update_promocion = session.query(Modulo).filter(Modulo.name == 'promocion_update').first()
        if update_promocion is None:
            update_promocion = Modulo(title='Actualizar', route='/promocion_update',
                                      name='promocion_update',
                                      menu=False)

        delete_promocion = session.query(Modulo).filter(Modulo.name == 'promocion_delete').first()
        if delete_promocion is None:
            delete_promocion = Modulo(title='Dar de Baja', route='/promocion_delete',
                                      name='promocion_delete',
                                      menu=False)

        imprimir_promocion = session.query(Modulo).filter(Modulo.name == 'promocion_imprimir').first()
        if imprimir_promocion is None:
            imprimir_promocion = Modulo(title='Imprimir', route='/promocion_imprimir',
                                        name='promocion_imprimir',
                                        menu=False)

            promocion_m.children.append(query_promocion)
            promocion_m.children.append(insert_promocion)
            promocion_m.children.append(update_promocion)
            promocion_m.children.append(delete_promocion)
            promocion_m.children.append(imprimir_promocion)

        query_oferta = session.query(Modulo).filter(Modulo.name == 'oferta_query').first()
        if query_oferta is None:
            query_oferta = Modulo(title='Consultar', route='',
                                  name='oferta_query',
                                  menu=False)

        insert_oferta = session.query(Modulo).filter(Modulo.name == 'oferta_insert').first()
        if insert_oferta is None:
            insert_oferta = Modulo(title='Adicionar', route='/oferta_insert',
                                   name='oferta_insert',
                                   menu=False)

        update_oferta = session.query(Modulo).filter(Modulo.name == 'oferta_update').first()
        if update_oferta is None:
            update_oferta = Modulo(title='Actualizar', route='/oferta_update',
                                   name='oferta_update',
                                   menu=False)

        delete_oferta = session.query(Modulo).filter(Modulo.name == 'oferta_delete').first()
        if delete_oferta is None:
            delete_oferta = Modulo(title='Dar de Baja', route='/oferta_delete',
                                   name='oferta_delete',
                                   menu=False)

        imprimir_oferta = session.query(Modulo).filter(Modulo.name == 'oferta_imprimir').first()
        if imprimir_oferta is None:
            imprimir_oferta = Modulo(title='Imprimir', route='/oferta_imprimir',
                                     name='oferta_imprimir',
                                     menu=False)

            oferta_m.children.append(query_oferta)
            oferta_m.children.append(insert_oferta)
            oferta_m.children.append(update_oferta)
            oferta_m.children.append(delete_oferta)
            oferta_m.children.append(imprimir_oferta)

        query_ofertaweb = session.query(Modulo).filter(Modulo.name == 'ofertaweb_query').first()
        if query_ofertaweb is None:
            query_ofertaweb = Modulo(title='Consultar', route='',
                                  name='ofertaweb_query',
                                  menu=False)

        insert_ofertaweb = session.query(Modulo).filter(Modulo.name == 'ofertaweb_insert').first()
        if insert_ofertaweb is None:
            insert_ofertaweb = Modulo(title='Adicionar', route='/ofertaweb_insert',
                                   name='ofertaweb_insert',
                                   menu=False)

        update_ofertaweb = session.query(Modulo).filter(Modulo.name == 'ofertaweb_update').first()
        if update_ofertaweb is None:
            update_ofertaweb = Modulo(title='Actualizar', route='/ofertaweb_update',
                                   name='ofertaweb_update',
                                   menu=False)

        delete_ofertaweb = session.query(Modulo).filter(Modulo.name == 'ofertaweb_delete').first()
        if delete_ofertaweb is None:
            delete_ofertaweb = Modulo(title='Dar de Baja', route='/ofertaweb_delete',
                                   name='ofertaweb_delete',
                                   menu=False)

        imprimir_ofertaweb = session.query(Modulo).filter(Modulo.name == 'ofertaweb_imprimir').first()
        if imprimir_ofertaweb is None:
            imprimir_ofertaweb = Modulo(title='Imprimir', route='/ofertaweb_imprimir',
                                     name='ofertaweb_imprimir',
                                     menu=False)

            ofertaweb_m.children.append(query_ofertaweb)
            ofertaweb_m.children.append(insert_ofertaweb)
            ofertaweb_m.children.append(update_ofertaweb)
            ofertaweb_m.children.append(delete_ofertaweb)
            ofertaweb_m.children.append(imprimir_ofertaweb)

        query_ayudaventas = session.query(Modulo).filter(Modulo.name == 'ayudaventas_query').first()
        if query_ayudaventas is None:
            query_ayudaventas = Modulo(title='Consultar', route='',
                                       name='ayudaventas_query',
                                       menu=False)

        insert_ayudaventas = session.query(Modulo).filter(Modulo.name == 'ayudaventas_insert').first()
        if insert_ayudaventas is None:
            insert_ayudaventas = Modulo(title='Adicionar', route='/ayudaventas_insert',
                                        name='ayudaventas_insert',
                                        menu=False)
        update_ayudaventas = session.query(Modulo).filter(Modulo.name == 'ayudaventas_update').first()
        if update_ayudaventas is None:
            update_ayudaventas = Modulo(title='Actualizar', route='/ayudaventas_update',
                                        name='ayudaventas_update',
                                        menu=False)
        delete_ayudaventas = session.query(Modulo).filter(Modulo.name == 'ayudaventas_delete').first()
        if delete_ayudaventas is None:
            delete_ayudaventas = Modulo(title='Dar de Baja', route='/ayudaventas_delete',
                                        name='ayudaventas_delete',
                                        menu=False)

        imprimir_ayudaventas = session.query(Modulo).filter(Modulo.name == 'ayudaventas_imprimir').first()
        if imprimir_ayudaventas is None:
            imprimir_ayudaventas = Modulo(title='Imprimir', route='/ayudaventas_imprimir',
                                          name='ayudaventas_imprimir',
                                          menu=False)

            ayudaventas_m.children.append(query_ayudaventas)
            ayudaventas_m.children.append(insert_ayudaventas)
            ayudaventas_m.children.append(update_ayudaventas)
            ayudaventas_m.children.append(delete_ayudaventas)
            ayudaventas_m.children.append(imprimir_ayudaventas)


        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(mcatalogo_m)
        admin_role.modulos.append(producto_m)
        admin_role.modulos.append(catalogo_m)
        admin_role.modulos.append(pagina_m)
        admin_role.modulos.append(promocion_m)
        admin_role.modulos.append(nivel_m)
        admin_role.modulos.append(oferta_m)
        admin_role.modulos.append(ofertaweb_m)
        admin_role.modulos.append(ayudaventas_m)

        admin_role.modulos.append(query_producto)
        admin_role.modulos.append(insert_producto)
        admin_role.modulos.append(update_producto)
        admin_role.modulos.append(delete_producto)
        admin_role.modulos.append(imprimir_producto)

        admin_role.modulos.append(query_catalogo)
        admin_role.modulos.append(insert_catalogo)
        admin_role.modulos.append(update_catalogo)
        admin_role.modulos.append(delete_catalogo)
        admin_role.modulos.append(imprimir_catalogo)

        admin_role.modulos.append(query_pagina)
        admin_role.modulos.append(insert_pagina)
        admin_role.modulos.append(update_pagina)
        admin_role.modulos.append(delete_pagina)
        admin_role.modulos.append(imprimir_pagina)

        admin_role.modulos.append(query_nivel)
        admin_role.modulos.append(insert_nivel)
        admin_role.modulos.append(update_nivel)
        admin_role.modulos.append(delete_nivel)
        admin_role.modulos.append(imprimir_pagina)

        admin_role.modulos.append(query_promocion)
        admin_role.modulos.append(insert_promocion)
        admin_role.modulos.append(update_promocion)
        admin_role.modulos.append(delete_promocion)
        admin_role.modulos.append(imprimir_promocion)

        admin_role.modulos.append(query_oferta)
        admin_role.modulos.append(insert_oferta)
        admin_role.modulos.append(update_oferta)
        admin_role.modulos.append(delete_oferta)
        admin_role.modulos.append(imprimir_oferta)

        admin_role.modulos.append(query_ofertaweb)
        admin_role.modulos.append(insert_ofertaweb)
        admin_role.modulos.append(update_ofertaweb)
        admin_role.modulos.append(delete_ofertaweb)
        admin_role.modulos.append(imprimir_ofertaweb)

        admin_role.modulos.append(query_ayudaventas)
        admin_role.modulos.append(insert_ayudaventas)
        admin_role.modulos.append(update_ayudaventas)
        admin_role.modulos.append(delete_ayudaventas)
        admin_role.modulos.append(imprimir_ayudaventas)

        session.commit()




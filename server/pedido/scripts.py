from sqlalchemy.sql.functions import percent_rank

from server.database.connection import transaction
from .models import *
from .managers import *
from ..usuarios.models import *

import schedule

def insertions():

    with transaction() as session:
        ###Modulo de Pedido
        mpedido_m = session.query(Modulo).filter(Modulo.name == 'mpedido_m').first()
        if mpedido_m is None:
            mpedido_m = Modulo(title='Modulo Pedido', name='mpedido_m', icon='dvr')

        pedido_m = session.query(Modulo).filter(Modulo.name == 'pedido_m').first()
        if pedido_m is None:
            pedido_m = Modulo(title='Pedido', route='/pedido', name='pedido',
                                    icon='portrait')

        mpedido_m.children.append(pedido_m)


        query_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_query').first()
        if query_pedido is None:
            query_pedido = Modulo(title='Consultar', route='',
                                    name='pedido_query',
                                    menu=False)

        insert_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_insert').first()
        if insert_pedido is None:
            insert_pedido = Modulo(title='Adicionar', route='/pedido_insert',
                                     name='pedido_insert',
                                     menu=False)
        update_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_update').first()
        if update_pedido is None:
            update_pedido = Modulo(title='Actualizar', route='/pedido_update',
                                     name='pedido_update',
                                     menu=False)
        delete_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_delete').first()
        if delete_pedido is None:
            delete_pedido = Modulo(title='Dar de Baja', route='/pedido_delete',
                                     name='pedido_delete',
                                     menu=False)

        imprimir_pedido = session.query(Modulo).filter(Modulo.name == 'pedido_imprimir').first()
        if imprimir_pedido is None:
            imprimir_pedido = Modulo(title='Imprimir', route='/pedido_imprimir',
                                       name='pedido_imprimir',
                                       menu=False)

            pedido_m.children.append(query_pedido)
            pedido_m.children.append(insert_pedido)
            pedido_m.children.append(update_pedido)
            pedido_m.children.append(delete_pedido)
            pedido_m.children.append(imprimir_pedido)

        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()

        ###Modulos de Operaciones

        admin_role.modulos.append(mpedido_m)
        admin_role.modulos.append(pedido_m)

        admin_role.modulos.append(query_pedido)
        admin_role.modulos.append(insert_pedido)
        admin_role.modulos.append(update_pedido)
        admin_role.modulos.append(delete_pedido)
        admin_role.modulos.append(imprimir_pedido)
        session.commit()
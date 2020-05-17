
from server.database.connection import transaction
from ..usuarios.models import *
from ..configuracion.models import *


def insertions():

    with transaction() as session:
        ###Modulo de Operaciones
        mconfiguracion_m = session.query(Modulo).filter(Modulo.name == 'mconfiguracion').first()
        if mconfiguracion_m is None:
            mconfiguracion_m = Modulo(title='Modulo Configuracion', name='mconfiguracion', icon='book')


        configuracion_m = session.query(Modulo).filter(Modulo.name == 'configuracion_m').first()
        if configuracion_m is None:
            configuracion_m = Modulo(title='Configuracion', route='/configuracion', name='Configuracion',
                                    icon='portrait')
        financiero_m = session.query(Modulo).filter(Modulo.name == 'financiero_m').first()
        if financiero_m is None:
            financiero_m = Modulo(title='financiero', route='/financiero', name='financiero',
                                     icon='portrait')

        mconfiguracion_m.children.append(configuracion_m)
        mconfiguracion_m.children.append(financiero_m)

        query_configuracion = session.query(Modulo).filter(Modulo.name == 'configuracion_query').first()
        if query_configuracion is None:
            query_configuracion = Modulo(title='Consultar', route='',
                                    name='configuracion_query',
                                    menu=False)

        insert_configuracion = session.query(Modulo).filter(Modulo.name == 'configuracion_insert').first()
        if insert_configuracion is None:
            insert_configuracion = Modulo(title='Adicionar', route='/configuracion_insert',
                                     name='configuracion_insert',
                                     menu=False)

        update_configuracion = session.query(Modulo).filter(Modulo.name == 'configuracion_update').first()
        if update_configuracion is None:
            update_configuracion = Modulo(title='Actualizar', route='/configuracion_update',
                                     name='configuracion_update',
                                     menu=False)

        delete_configuracion = session.query(Modulo).filter(Modulo.name == 'configuracion_delete').first()
        if delete_configuracion is None:
            delete_configuracion = Modulo(title='Dar de Baja', route='/configuracion_delete',
                                     name='configuracion_delete',
                                     menu=False)

        imprimir_configuracion = session.query(Modulo).filter(Modulo.name == 'configuracion_imprimir').first()
        if imprimir_configuracion is None:
            imprimir_configuracion = Modulo(title='Imprimir', route='/configuracion_imprimir',
                                       name='configuracion_imprimir',
                                       menu=False)

            configuracion_m.children.append(query_configuracion)
            configuracion_m.children.append(insert_configuracion)
            configuracion_m.children.append(update_configuracion)
            configuracion_m.children.append(delete_configuracion)
            configuracion_m.children.append(imprimir_configuracion)

        query_financiero = session.query(Modulo).filter(Modulo.name == 'financiero_query').first()
        if query_financiero is None:
            query_financiero = Modulo(title='Consultar', route='',
                                         name='financiero_query',
                                         menu=False)

        insert_financiero = session.query(Modulo).filter(Modulo.name == 'financiero_insert').first()
        if insert_financiero is None:
            insert_financiero = Modulo(title='Adicionar', route='/financiero_insert',
                                          name='financiero_insert',
                                          menu=False)

        update_financiero = session.query(Modulo).filter(Modulo.name == 'financiero_update').first()
        if update_financiero is None:
            update_financiero = Modulo(title='Actualizar', route='/financiero_update',
                                          name='financiero_update',
                                          menu=False)

        delete_financiero = session.query(Modulo).filter(Modulo.name == 'financiero_delete').first()
        if delete_financiero is None:
            delete_financiero = Modulo(title='Dar de Baja', route='/financiero_delete',
                                          name='financiero_delete',
                                          menu=False)

        imprimir_financiero = session.query(Modulo).filter(Modulo.name == 'financiero_imprimir').first()
        if imprimir_financiero is None:
            imprimir_financiero = Modulo(title='Imprimir', route='/financiero_imprimir',
                                            name='financiero_imprimir',
                                            menu=False)

            financiero_m.children.append(query_financiero)
            financiero_m.children.append(insert_financiero)
            financiero_m.children.append(update_financiero)
            financiero_m.children.append(delete_financiero)
            financiero_m.children.append(imprimir_financiero)

        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()

        ###Modulos de Operaciones
        admin_role.modulos.append(mconfiguracion_m)
        admin_role.modulos.append(configuracion_m)
        admin_role.modulos.append(query_configuracion)
        admin_role.modulos.append(insert_configuracion)
        admin_role.modulos.append(update_configuracion)
        admin_role.modulos.append(delete_configuracion)
        admin_role.modulos.append(imprimir_configuracion)

        admin_role.modulos.append(financiero_m)
        admin_role.modulos.append(query_financiero)
        admin_role.modulos.append(insert_financiero)
        admin_role.modulos.append(update_financiero)
        admin_role.modulos.append(delete_financiero)
        admin_role.modulos.append(imprimir_financiero)

        configuracion = Configuracion(video="", facebook="", pagina ="", twitter="", otro="")
        session.merge(configuracion)
        session.commit()
        session.commit()




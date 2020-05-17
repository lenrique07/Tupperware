
def insertions():

    import hashlib
    from server.database.connection import transaction
    from .models import Modulo, Usuario, Rol

    with transaction() as session:
        user_m = session.query(Modulo).filter(Modulo.name == 'user_Modulo').first()
        if user_m is None:
            user_m = Modulo(title='Usuarios', name='user_Modulo', icon='person')

        roles_m = session.query(Modulo).filter(Modulo.name == 'roles').first()
        if roles_m is None:
            roles_m = Modulo(title='Rol', route='/rol', name='roles', icon='dashboard')

        usuarios_m = session.query(Modulo).filter(Modulo.name == 'usuario').first()
        if usuarios_m is None:
            usuarios_m = Modulo(title='Usuario', route='/usuario', name='usuario', icon='account_box')

        perfil_m = session.query(Modulo).filter(Modulo.name == 'perfil').first()
        if perfil_m is None:
            perfil_m = Modulo(title='Perfil Usuario', route='/usuario_profile', name='perfil', icon='dvr')

        bitacora_m = session.query(Modulo).filter(Modulo.name == 'bitacora').first()
        if bitacora_m is None:
            bitacora_m = Modulo(title='Bitacora', route='/bitacora', name='bitacora', icon='dvr')

        user_m.children.append(roles_m)
        user_m.children.append(usuarios_m)
        user_m.children.append(perfil_m)
        user_m.children.append(bitacora_m)

        query_rol = session.query(Modulo).filter(Modulo.name == 'rol_query').first()
        if query_rol is None:
            query_rol = Modulo(title='Consultar', route='', name='rol_query', menu=False)
        insert_rol = session.query(Modulo).filter(Modulo.name == 'rol_insert').first()
        if insert_rol is None:
            insert_rol = Modulo(title='Adicionar', route='/rol_insert', name='rol_insert', menu=False)
        update_rol = session.query(Modulo).filter(Modulo.name == 'rol_update').first()
        if update_rol is None:
            update_rol = Modulo(title='Actualizar', route='/rol_update', name='rol_update', menu=False)
        delete_rol = session.query(Modulo).filter(Modulo.name == 'rol_delete').first()
        if delete_rol is None:
            delete_rol = Modulo(title='Dar de Baja', route='/rol_delete', name='rol_delete', menu=False)

        roles_m.children.append(query_rol)
        roles_m.children.append(insert_rol)
        roles_m.children.append(update_rol)
        roles_m.children.append(delete_rol)

        query_usuario = session.query(Modulo).filter(Modulo.name == 'usuario_query').first()
        if query_usuario is None:
            query_usuario = Modulo(title='Consultar', route='', name='usuario_query', menu=False)
        insert_usuario = session.query(Modulo).filter(Modulo.name == 'usuario_insert').first()
        if insert_usuario is None:
            insert_usuario = Modulo(title='Adicionar', route='/usuario_insert', name='usuario_insert', menu=False)
        update_usuario = session.query(Modulo).filter(Modulo.name == 'usuario_update').first()
        if update_usuario is None:
            update_usuario = Modulo(title='Actualizar', route='/usuario_update', name='usuario_update', menu=False)
        delete_usuario = session.query(Modulo).filter(Modulo.name == 'usuario_delete').first()
        if delete_usuario is None:
            delete_usuario = Modulo(title='Dar de Baja', route='/usuario_delete', name='usuario_delete', menu=False)

        usuarios_m.children.append(query_usuario)
        usuarios_m.children.append(insert_usuario)
        usuarios_m.children.append(update_usuario)
        usuarios_m.children.append(delete_usuario)

        query_bitacora = session.query(Modulo).filter(Modulo.name == 'bitacora_query').first()
        if query_bitacora is None:
            query_bitacora = Modulo(title='Consultar', route='', name='bitacora_query', menu=False)

        bitacora_m.children.append(query_bitacora)

        admin_role = session.query(Rol).filter(Rol.nombre == 'Administrador').first()
        if admin_role is None:
            admin_role = Rol(nombre='ADMINISTRADOR', descripcion='Todos los permisos')

        ###Modulo de Usuarios

        admin_role.modulos.append(user_m)
        admin_role.modulos.append(roles_m)
        admin_role.modulos.append(usuarios_m)
        admin_role.modulos.append(perfil_m)
        admin_role.modulos.append(bitacora_m)
        admin_role.modulos.append(query_usuario)
        admin_role.modulos.append(insert_usuario)
        admin_role.modulos.append(update_usuario)
        admin_role.modulos.append(delete_usuario)
        admin_role.modulos.append(query_rol)
        admin_role.modulos.append(insert_rol)
        admin_role.modulos.append(update_rol)
        admin_role.modulos.append(delete_rol)
        admin_role.modulos.append(query_bitacora)

        super_user = session.query(Usuario).filter(Usuario.nombre == 'admin').first()
        if super_user is None:
            hex_dig = hashlib.sha512(b'admin').hexdigest()
            super_user = Usuario( nombre='Administrador', apellido='principal', correo='admin@host.com', username='admin',
                                 password=hex_dig)
            super_user.rol = admin_role

        session.add(super_user)
        session.add(admin_role)
        session.commit()

# django_permissions

Trabajando con el usuario por defecto de Django
- Crear superuser
- Crear usuario staff para entrar en el admin pero sin ser super usuario
user = User.objects.create_user('normal', 'normal@test.com', 'normal1234.')
user.is_staff = True
user.save()
- comprobar que no tiene permisos por el momento
API https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User
user.get_user_permissions()
- Imagenes del admin como user y como superuser

- Crear modelos con relaciones
    -Cuidado con el modelo user, no string porque es el de Django
- Modelos con imagenes:
    - Hace falta pillow
- Hacer migraciones
- Añadir al admin los otros modelos
    admin.site.register(UserProfile)

- Imagen añadir un perfil
    puedo elegir cualquiera de los usuarios como super user, veo los dos, como normal no se ve nada
- Crear datos
- Permisos
https://docs.djangoproject.com/en/3.1/topics/auth/default/
- comprobar los permisos, emeplo add
    usuario normal = user.has_perm('learning.add_company') 
    super usuario = superuser.has_perm('learning.add_company') 

- Los permisos los damos por grupo porque si se dan por permiso concreto
a un usuario hay que darle los permisos detalladamente, por ejemplo sólo le añadimos el permiso de ver en bot pero no puede hacer más y admeás, tiene acceso a ver TODOS los bots, no sólo el suyo, por ejemplo puede ver el bot del super usuario.

- Grupos:
podemos agrupar permisos pero se sigue viendo lo que no es tuyo, ahí entra Django-guardian.
Por ejemplo metemos al usuario normal en el grupo bot_read y ya puede ver los bots.
Creamos el grupo bot_write, ahí se tienen los permisos de añadir, cambiar y borrar y si metemos al usuario normal prodrá tanto ver como editar bots pero incluso bots que NO son suyos.
Si tiene el write ya tiene el view --ejemplo company

- crear nuevo permiso Django
se añade el permiso al meta del modelo, se crea la migraciOn y aparece el
nuevo permiso.

DJANGO GUARDIAN
- Permisos a nivel de instacia
- AUTHENTICATION_BACKENDS
    'guardian.backends.ObjectPermissionBackend'
- Deshabilitar el usuario anónimo
    ANONYMOUS_USER_NAME = None --> Todo usuario tiene que estar registrado y logeado para usar la app.
- Ejecutar la migración
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from dev_sistema_escolar_api.views import bootstrap
from dev_sistema_escolar_api.views import users
from dev_sistema_escolar_api.views import alumnos
from dev_sistema_escolar_api.views import maestros
from dev_sistema_escolar_api.views import auth
from dev_sistema_escolar_api.views import eventos

urlpatterns = [
   #Create Admina
        path('admins/', users.AdminView.as_view()),
    #Render
        path('admin/', admin.site.urls),
    #Admin Data
        path('lista-admins/', users.AdminAll.as_view()),
    #Edit Admin
        #path('admins-edit/', users.AdminsViewEdit.as_view())
    #Create Alumno
        path('alumnos/', alumnos.AlumnosView.as_view()),
    #Create Maestro
        path('maestros/', maestros.MaestrosView.as_view()),
    #Maestro Data
        path('lista-maestros/', maestros.MaestrosAll.as_view()),
    #Alumnos Data
        path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    #Total Users
        path('total-usuarios/', users.TotalUsers.as_view()),
    #Login
        path('login/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view()),
    #Crear evento
        path('eventos-academicos/', eventos.EventosView.as_view()),
    #Lista de eventos
        path('total-eventos/', eventos.EventosAll.as_view()),
    #Editar
        path('eventos-academicos', eventos.EventosView.as_view()),
    #Total de Eventos
        path('eventos-totales/', eventos.TotalEventos.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
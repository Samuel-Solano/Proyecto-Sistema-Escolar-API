import os
import django
from django.contrib.auth import get_user_model

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dev_sistema_escolar_api.settings")
django.setup()

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    print(f"Creando superusuario: {username}")
    User.objects.create_superuser(username, email, password)
    print("¡Superusuario creado con éxito!")
else:
    print("El superusuario ya existe. No se hizo nada.")
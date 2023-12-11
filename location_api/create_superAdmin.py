from django.contrib.auth import get_user_model
from location_api.models import Manager

def create_Manager_user(**kwargs):
    User = get_user_model()
    email = 'superadmin@example.com'
    password = 'superadmin@1234'
    first_name = 'Superadmin'
    last_name = 'Superadmin'
    role = 'SUPERADMIN'
    if not User.objects.filter(email=email).exists():
        Manager.objects.create(email=email, password=password, first_name=first_name, last_name=last_name, role=role)
()
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class LocationApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'location_api'
    
    def ready(self):
        from .create_superAdmin import create_Manager_user
        post_migrate.connect(create_Manager_user, sender=self)  

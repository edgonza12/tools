from django.conf import settings
from django.db import models

class InvestigationHistory(models.Model):
    SEARCH_TYPE_CHOICES = [
        ('username', 'Nombre de Usuario'),
        ('email', 'Correo Electrónico'),
        ('name', 'Nombre Completo'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    search_type = models.CharField(max_length=20, choices=SEARCH_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.query} ({self.search_type})"
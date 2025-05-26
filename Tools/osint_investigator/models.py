from django.conf import settings
from django.db import models

class InvestigationHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target = models.CharField(max_length=150)
    query_type = models.CharField(max_length=50, choices=[('username', 'Username'), ('email', 'Email'), ('full', 'Full Investigation')])
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query_type} - {self.target}"
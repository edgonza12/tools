from django.db import models
from django.conf import settings

class InvestigationHistory(models.Model):
    SEARCH_TYPES = [
        ('username', 'Nombre de usuario'),
        ('email', 'Correo electrónico'),
        ('fullname', 'Nombre completo'),
        # Puedes añadir más tipos como 'photo', etc.
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_type = models.CharField(
        max_length=20,
        choices=SEARCH_TYPES,
        null=True,
        blank=True
    )
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    result_count = models.PositiveIntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.search_type} - {self.searched_at.strftime('%Y-%m-%d %H:%M:%S')}"

class SherlockResult(models.Model):
    history = models.ForeignKey(InvestigationHistory, on_delete=models.CASCADE, related_name='sherlock_results')
    platform = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform}: {self.url}"
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ScanHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_network = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    # Resumen general
    total_hosts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.target_network} - {self.date.strftime('%Y-%m-%d %H:%M')}"


class ScanHostResult(models.Model):
    history = models.ForeignKey(ScanHistory, related_name='hosts', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=255, blank=True)
    mac = models.CharField(max_length=50, blank=True)
    vendor = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.ip


class OpenPort(models.Model):
    host = models.ForeignKey(ScanHostResult, related_name='ports', on_delete=models.CASCADE)
    port = models.PositiveIntegerField()
    protocol = models.CharField(max_length=10)
    service = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.port}/{self.protocol} - {self.service}"
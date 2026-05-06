# Create your models here.
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.CharField(max_length=100, blank=True, help_text="ex: Sur devis, 100$")
    
    def __str__(self):
        return self.name
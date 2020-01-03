from django.db import models

# Create your models here.
class Token(models.Model):
    registration_token = models.CharField(max_length = 150, null = True, unique = True)